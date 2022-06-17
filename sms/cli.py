from typing import Optional
import os

import typer

from sms import SUCCESS, __app_name__, __version__, config,  ERROR, database
from sms.config import Config
from sms.sms import authenticate, display_records

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        "-V",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return

@app.command()
def greeting(name:str) -> str:
    print(f"Hello {name}!")

@app.command()
def init(
    db_path : Optional[str] = typer.Option(
        str(database.DEFAULT_DATABASE_FOLDER),
        '--db_path',
        '-db',
        # callback=database.create_databse,
        prompt='Give folder path for database : ',
        help="Give database folder path: "
    ) ) -> None:
    # init config file 
    print("db_path: ", db_path)
    db_obj = database.Database()
    db_create_error = db_obj.create_database(db_folder=db_path)
    if db_create_error:
        typer.secho(
            f"Error while initializing database file: {ERROR[db_create_error]}",
            fg = typer.colors.RED
        )
        raise typer.Exit(1)
    app_init_error = Config().create_init_config(db_path)
    if app_init_error:
        typer.secho(
            f"Config file initialization error: {ERROR[app_init_error]}",
            fg=typer.colors.RED
        )
        raise typer.EXIT(1)
    
    typer.secho(
        f"The sms app successfully initialized with db folder: {db_path}",
        fg = typer.colors.GREEN
    )
    

@app.command()
def login():
    status = typer.prompt("student or admin ? ")
    if status != 'student' and status != 'admin':
        typer.secho(
            "Invalid choice selected, please try again.",
            fg = typer.colors.RED
        )
        raise typer.Exit(1)
    username = typer.prompt("Username: ")
    password = typer.prompt("Password: ", hide_input=True, confirmation_prompt=True)
    auth_status = authenticate(status,username, password)
    if auth_status != SUCCESS:
        typer.secho(
            f"Auth Failed: {ERROR[auth_status]}",
            fg = typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            "authentication successful.",
            fg = typer.colors.GREEN
        )
        raise typer.Exit(1)


@app.command()
def read():
    all_data = display_records()
    typer.secho(
        f"{all_data}"
    )
    raise typer.Exit(1)


        