from pathlib import Path
import json
from sms.config import Config
from sms.lib.security import Security

import typer 
from sms import DB_UPDATE_ERROR, DB_WRITE_ERROR, DB_READ_ERROR, DIR_ERROR, FILE_ERROR, SUCCESS, __app_name__

DEFAULT_DATABASE_FOLDER = Path(typer.get_app_dir(__app_name__)).joinpath('database')
DEFAULT_DATABASE_PATH = Path(DEFAULT_DATABASE_FOLDER, str(__app_name__)+'_database.json')

class Database:
    def __init__(self, db_path: str = None):
        if db_path:
            self.db_path = Path(db_path)
        else:
            self.db_path = None
        if self.db_path:
            self.db_folder = self.db_path.parent
        else:
            self.db_folder = None

    def create_database(self, db_folder: str):
        self.db_path = Path(f"{db_folder}").joinpath('sms_db.json')
        self.db_folder = self.db_path.parent
        if not self.db_folder.exists():
            self.db_folder.mkdir(parents=True, exist_ok=True)
        try:
            self.db_path.touch(exist_ok=True)
        except OSError:
            return FILE_ERROR
        try:
            default_pass = "admin"
            enc_pass, enc_key = Security().encrypt(default_pass)
            with self.db_path.open('w') as db_file:
                data = {
                    "admin": {
                        "username": "admin",
                        "password": enc_pass,
                        "key": enc_key
                    },
                    "students": list()
                }
                db_file.write(json.dumps(data, indent=4))
        except OSError:
            return FILE_ERROR
        return SUCCESS

    def create_record(self, *args, **kwargs):
        try:
            new_record = dict()
            status = 'students'
            for key, value in args[0].items():
                if key == 'password':
                    value, enc_key = Security().encrypt(value)
                    new_record["key"] = enc_key
                new_record[key] = value
            with self.db_path.open('r') as old_records:
                data = json.loads(old_records.read())
                data[status].append(new_record) 
                with self.db_path.open('w') as updated_record:
                    updated_record.write(json.dumps(data, indent=4))
            return SUCCESS
        except OSError:
            return DB_WRITE_ERROR

    def update_database(self, new_record):
        try:
            with  self.db_path.open('w') as db_file:
                db_file.write(json.dumps(new_record, indent=4))
        except Exception as e:
            print(e)
            return DB_UPDATE_ERROR
        return SUCCESS

        
    def get_all_data(self):
        try:
            with self.db_path.open('r') as db_file:
                data = db_file.read()
                data = json.loads(data)
                return data 
        except OSError:
            return DB_READ_ERROR
