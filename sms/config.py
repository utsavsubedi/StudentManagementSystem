import configparser
from genericpath import exists
from pathlib import Path
import typer

from sms import (
    SUCCESS, DIR_ERROR,  FILE_ERROR, __app_name__
)

CONFIG_FOLDER = Path(typer.get_app_dir(__app_name__))
CONFIG_PATH = CONFIG_FOLDER.joinpath(CONFIG_FOLDER, 'config.ini')

class Config:
    def __init__(self):
        self.config_path = None
        self.config_folder = None

    def create_init_config(self, db_path: str) -> int:
        try:
            CONFIG_FOLDER.mkdir(parents=True,exist_ok=True)
        except OSError:
            return DIR_ERROR
        try:
            CONFIG_PATH.touch(exist_ok=True)
        except OSError:
            return FILE_ERROR
        
        cfg_file = configparser.ConfigParser()
        cfg_file['General'] = {'database':db_path}
        try:
            with CONFIG_PATH.open("w") as file:
                cfg_file.write(file)
        except OSError:
            return FILE_ERROR
        return SUCCESS

    