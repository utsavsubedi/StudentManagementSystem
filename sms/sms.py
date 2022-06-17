from sms import SUCCESS, DOESNOT_EXIST_ERROR
from sms.config import Config
from functools import wraps
from sms.database import Database
import typer
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
        status = session.get_current_user_status()
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
    if status == 'admin':
        if username == ALL_DATA['admin']['username'] and password == ALL_DATA['admin']['password']:
            # os.environ['sms_admin'] = "True"
            session.create_session()
            return SUCCESS
        else:
            return DOESNOT_EXIST_ERROR
    if status == 'students':
        for record in ALL_DATA['students']:
            if username == record['username']:
                if password == record['password']:
                    # os.environ['sms_admin'] = "False"
                    session.create_session()
                    return SUCCESS
        return DOESNOT_EXIST_ERROR
    return DOESNOT_EXIST_ERROR
        
@admin_check
def display_records():
    return ALL_DATA["students"]        

def create_record(**kwargs):
    database = Database(DATABASE_PATH)
    creation_status = database.create_record(kwargs)
    return creation_status
