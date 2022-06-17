from tkinter import ALL
from sms import SUCCESS, DOESNOT_EXIST_ERROR,DB_READ_ERROR
from sms.config import Config
from functools import wraps
from sms.database import Database
import os
import typer


DATABASE_PATH = Config().get_database_path()
ALL_DATA = Database(DATABASE_PATH).get_all_data()

def admin_check(original_function):
    @wraps
    def wrapper(*args, **kwargs):
        session_user = os.environ.get("username")
        session_password = os.environ.get("password")
        admin_username = ALL_DATA['admin']['username']
        admin_password = ALL_DATA['admin']['password']
        if session_user == admin_username and session_password == admin_password:
            return original_function(*args **kwargs)
        else:
            typer.secho(
                "The user must be authenticated as admin to do this operation",
                fg =  typer.colors.RED
            )
            typer.Exit(1)


def authenticate(status, username, password):
    # admin login
    if status == 'admin':
        if username == ALL_DATA['admin']['username'] and password == ALL_DATA['admin']['password']:
            return SUCCESS
        else:
            return DOESNOT_EXIST_ERROR
    if status == 'students':
        for record in ALL_DATA['students']:
            if username == record['username']:
                if password == record['password']:
                    return SUCCESS
        return DOESNOT_EXIST_ERROR
    return DOESNOT_EXIST_ERROR
        
    
