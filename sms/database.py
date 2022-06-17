import configparser, os
from pathlib import Path
import json

import typer 
from sms import DB_WRITE_ERROR, DB_READ_ERROR, DIR_ERROR, FILE_ERROR, SUCCESS, __app_name__

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
            with self.db_path.open('w') as db_file:
                data = {
                    "admin": {
                        "username": "admin",
                        "password": "admin"
                    },
                    "students": list()
                }
                db_file.write(json.dumps(data, indent=4))
        except OSError:
            return FILE_ERROR
        return SUCCESS

    def create_record(self, **kwargs):
        new_record = dict()
        status = os.environ.get('user_status')
        for item in kwargs:
            new_record[item] = kwargs[item]
        with self.db_path.open('r') as old_records:
            data = old_records.read()
            data[status].append(new_record) 
            with self.db_path.open('w') as updated_record:
                updated_record.write(data)
        
    def get_all_data(self):
        try:
            with self.db_path.open('r') as db_file:
                data = db_file.read()
                data = json.loads(data)
                return data 
        except OSError:
            return DB_READ_ERROR
