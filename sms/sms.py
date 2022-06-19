from sms import DB_UPDATE_ERROR, LOGIN_ERROR, SUCCESS, DOESNOT_EXIST_ERROR, ADMIN_DELETE_ERROR
from sms.config import Config
from functools import wraps
from sms.database import Database
import typer
from sms.lib.security import Security
from sms.lib.session import Session

DATABASE_PATH = Config().get_database_path()
try:
    ALL_DATA = Database(DATABASE_PATH).get_all_data()
except:
    pass

def admin_check(original_function):
    # @wraps
    def wrapper(*args, **kwargs):
        session = Session()
        username, status, password = session.get_current_user_info()
        if status == 'admin':
            return original_function(*args, **kwargs)
        else:
            typer.secho(
                "The user must be authenticated as admin to do this operation.",
                fg = typer.colors.RED
            )
            raise typer.Exit(1)
    return wrapper


def authenticate(status, username, password):
    # admin login
    session = Session()
    session.username = username
    session.password = password
    session.status = status
    security = Security()
    if status == 'admin':
        dec_password = security.decrypt(ALL_DATA['admin']['password'],ALL_DATA['admin']['key'])
        if username == ALL_DATA['admin']['username'] and password == dec_password:
            # os.environ['sms_admin'] = "True"
            session.create_session()
            return SUCCESS
        else:
            return DOESNOT_EXIST_ERROR
    if status == 'student':
        for record in ALL_DATA['students']:
            if username == record['username']:
                dec_password = security.decrypt(record['password'],record['key'])
                if password == dec_password:
                    # os.environ['sms_admin'] = "False"
                    session.create_session()
                    return SUCCESS
        return DOESNOT_EXIST_ERROR
    return DOESNOT_EXIST_ERROR
        
def display_records():
    session = Session()
    username, status, password = session.get_current_user_info()
    if status == 'admin':
        for student in  ALL_DATA["students"]:
            del student["key"]
        return ALL_DATA["students"] 
    elif status == 'student':
        security = Security()
        for record in ALL_DATA['students']:
            if username == record['username']:
                dec_password = security.decrypt(record['password'],record['key'])
                if password == dec_password:
                    return record


def create_record(**kwargs):
    database = Database(DATABASE_PATH)
    creation_status = database.create_record(kwargs)
    return creation_status

def get_record_by_username(username):
    try:
        session = Session()
        session_user, status, password = session.get_current_user_info()
    except:
        return LOGIN_ERROR, None
    if status == "admin":
        try:
            data = ALL_DATA["admin"][username]
            return data, None
        except:
            for record in ALL_DATA["students"]:
                if record['username']  == username:
                    return record, "students"
            return DOESNOT_EXIST_ERROR, None
    elif status == "student":
        for record in ALL_DATA["students"]:
                if record['username'] == session_user and session_user==username:
                    return record, "students"
        return DOESNOT_EXIST_ERROR, None
    else:
        return DOESNOT_EXIST_ERROR, None

def update_record(old_record, new_record, status):
    try:
        if status == "admin":
            ALL_DATA["admin"]  = new_record
            update_status = Database(DATABASE_PATH).update_database(ALL_DATA)
            return update_status
        elif status == "students":
            ALL_DATA["students"].remove(old_record)
            ALL_DATA["students"].append(new_record)
            update_status = Database(DATABASE_PATH).update_database(ALL_DATA)
            return update_status
        else:
            return DB_UPDATE_ERROR
    except:
        return DB_UPDATE_ERROR

def delete_record(record, status):
    try:
        if status == "admin":
            return ADMIN_DELETE_ERROR
        elif status == "students":
            ALL_DATA["students"].remove(record)
            delete_status = Database(DATABASE_PATH).update_database(ALL_DATA)
            return delete_status
        else:
            return DB_UPDATE_ERROR
    except:
        return DB_UPDATE_ERROR
