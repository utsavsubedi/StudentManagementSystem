from sms import __app_name__
import typer
from pathlib import Path
import json
from cryptography.fernet import Fernet

SESSION_PATH = Path(typer.get_app_dir(__app_name__)).joinpath('session', 'session.json')

class Session:
    def __init__(self):
        self.username = None
        self.password = None
        self.status = None
        self.session_path = SESSION_PATH
        self.key = Fernet.generate_key()

    def create_session(self):
        try:
            self.session_path = SESSION_PATH
            session_folder = self.session_path.parent
            if not session_folder.exists():
                session_folder.mkdir(parents=True, exist_ok=True)
            self.session_path.touch(exist_ok=True)
            session = {
                "username": self.encrypt(self.username),
                "password": self.encrypt(self.password),
                "status": self.encrypt(self.status),
                "key": self.key.decode("utf-8")
            }
            with self.session_path.open('w') as session_file:
                session_file.write(json.dumps(session, indent=4))
        except:
            typer.secho(
                "There was a failure while creating current session.",
                fg = typer.colors.RED
            )
            raise typer.Exit(1)

    def get_current_user_status(self):
        with self.session_path.open('r') as session_file:
            session = json.loads(session_file.read())
            status = self.decrypt(session['status'])
            return status

    def get_current_user_info(self):
        with self.session_path.open('r') as session_file:
            session = json.loads(session_file.read())
            status = self.decrypt(session['status'])
            username = self.decrypt(session['username'])
            password = self.decrypt(session['password'])
            return username, status, password

        

    def encrypt(self, message):
        fernet = Fernet(self.key)
        encoded = fernet.encrypt(message.encode())
        return encoded.decode("utf-8")


    def decrypt(self, message):
        message = bytes(message, 'utf-8')
        with self.session_path.open('r') as session_file:
            session_file = json.loads(session_file.read())
            self.key = bytes(session_file["key"], 'utf-8')
        fernet = Fernet(self.key)
        return fernet.decrypt(message).decode()