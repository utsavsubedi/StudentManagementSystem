import configparser
from pathlib import Path

import typer 
from sms import DB_WRITE_ERROR, DB_READ_ERROR, DIR_ERROR, FILE_ERROR, SUCCESS, __app_name__

DEFAULT_DATABASE_FOLDER = Path(typer.get_app_dir(__app_name__)).joinpath('database')
DEFAULT_DATABASE_PATH = Path(DEFAULT_DATABASE_FOLDER, 'sms_database.json')

def _init_database(db_folder: str) -> int:
    db_path = Path(f"{db_folder}").joinpath('sms_db.json')
    db_folder = db_path.parent
    if not db_folder.exists():
        db_folder.mkdir(parents=True, exist_ok=True)
    try:
        db_path.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR
    return SUCCESS

def create_databse(db_path: str) -> int:
    db_creation = _init_database(db_path)
    if db_creation != SUCCESS:
        return db_creation
    return SUCCESS
