from typing import Optional

import typer

from sms import __app_name__, __version__, config, database, ERROR

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
    db_create_error = database.create_databse(db_path)
    if db_create_error:
        typer.secho(
            f"Error while initializing database file: {ERROR[db_create_error]}",
            fg = typer.colors.RED
        )
        raise typer.Exit(1)
    app_init_error = config.init_app(db_path)
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
    
