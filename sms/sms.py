from sms import SUCCESS, DOESNOT_EXIST_ERROR
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

