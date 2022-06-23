from textwrap import wrap
from sms import DB_UPDATE_ERROR, LOGIN_ERROR, SESSION_DELETE_ERROR, SUCCESS, DOESNOT_EXIST_ERROR, ADMIN_DELETE_ERROR
from sms.config import Config
from functools import wraps
from sms.database import Database
import typer
from sms.lib.security import Security
from sms.lib.session import Session
import logging
from sms import __app_name__
from pathlib import Path

DATABASE_PATH = Config().get_database_path()
try:
    ALL_DATA = Database(DATABASE_PATH).get_all_data()
except:
    pass

# decorator to check if current user is admin
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


# decorator to keep log of all functions called with args and kwargs
def user_process_log(original_function):

    @wraps(original_function)
    def wrapper(*args, **kwargs):
        LOG_PATH = Path(typer.get_app_dir(__app_name__), 'logs')
        if not LOG_PATH.exists():
            LOG_PATH.mkdir(parents=True, exist_ok=True)
        session = Session()
        try:
            username, _, _ = session.get_current_user_info()
        except:
            username = 'Anonymous'
        LOG_FILE = LOG_PATH.joinpath(f'{username}.log')
        if not LOG_FILE.exists():
            LOG_FILE.touch(exist_ok=True)
        
        logger = logging.getLogger(__name__)
        file_handler = logging.FileHandler(filename = LOG_FILE, mode='a+')
        file_handler.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        logger.addHandler(file_handler)
        logger.critical(f'User: {username} called {original_function.__name__} with args: {args} and kwargs: {kwargs}')
        return original_function(*args, **kwargs)

    return wrapper
            

@user_process_log
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
        

@user_process_log        
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

@user_process_log
def create_record(**kwargs):
    database = Database(DATABASE_PATH)
    creation_status = database.create_record(kwargs)
    return creation_status

@user_process_log
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

@user_process_log
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

@user_process_log
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

@user_process_log
def logout_user():
    session = Session()
    session_status = session.destroy_session()
    return session_status


