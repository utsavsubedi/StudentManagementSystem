from typing import Optional
import typer
from sms import EMAIL_ERROR, LOGIN_ERROR, SESSION_DELETE_ERROR, SUCCESS, __app_name__, __version__, config, \
     ERROR, database, DOESNOT_EXIST_ERROR, DB_UPDATE_ERROR, ADMIN_DELETE_ERROR
from sms.config import Config
from sms.lib.session import Session
from sms.sms import create_record, delete_record, logout_user
from sms.lib.security import Security
from sms.sms import authenticate, display_records, update_record, get_record_by_username
from sms.lib.Email import send_email

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
    try:
        if len(all_data) == 0:
            typer.secho(
                "Currently there are no records. Please add some to display.",
                fg =  typer.colors.RED
            )
            raise typer.Exit(1)
    except:
        typer.secho(
            "Currently there are no records. Please add some to display.",
            fg =  typer.colors.RED
        )
        raise typer.Exit(1)
    try:
        headers = [ key for key, value in all_data[0].items() ]
    except Exception as e:
        headers = [ key for key, value in all_data.items() ]
        headers.remove('key')
    headers = '       |'.join(headers)
    headers = headers.replace('email', 'email'+' '*15)+'       |'
    typer.secho(
        headers, fg =  typer.colors.RED
    )
    try:
        for data in all_data:
            string = ''
            for key, values in data.items():
                total_length = len(key)+7
                if key == 'key':
                    continue
                if key == 'email':
                    total_length = total_length +15
                if len(values) > total_length:
                    values = values[:total_length-3]+'...'
                    string += values+'|'
                    continue
                side_length = int((total_length - len(values)))
                string += values+(side_length*' ')+'|'
            typer.secho(
                string,
                fg=typer.colors.BLUE
            )
    except:
        string = ''
        for key, values in all_data.items():
            total_length = len(key)+7
            if key == 'key':
                continue
            if key == 'email':
                total_length = total_length +15
            if len(values) > total_length:
                values = values[:total_length-3]+'...'
                string += values+'|'
                continue
            side_length = int((total_length - len(values)))
            string += values+(side_length*' ')+'|'
        typer.secho(
            string,
            fg=typer.colors.BLUE
        )
    # typer.secho(
    #     f"{all_data}"
    # )
    raise typer.Exit(1)


@app.command()
def registration():
    username = typer.prompt("username")
    password = typer.prompt("Create a password ", hide_input=True, confirmation_prompt=True)
    name = typer.prompt("Enter your name: ")
    email = typer.prompt("Enter a valid email")
    location = typer.prompt("Enter your current address")
    creation_status = create_record(
        username = username,
        password = password,
        name = name,
        email = email,
        location = location
    )
    if creation_status != SUCCESS:
        typer.secho(
            f"Error while creating new record: {ERROR[creation_status]}",
            fg = typer.colors.RED
        )
        raise typer.Exit(1)
    email_status = send_email(email, name)
    if email_status != SUCCESS:
        typer.secho(
            f"Error: {ERROR[EMAIL_ERROR]}",
            fg= typer.colors.RED
        )
        raise typer.Exit(1)
    typer.secho(
        "Your registration was successful. Check email for confirmation and use the username and password to authenticate. \
        \n command: python -m sms login",
        fg = typer.colors.GREEN
    )
    raise typer.Exit(1)


@app.command()
def update():
    username = typer.prompt("Enter the username that you want to edit ")
    record, status = get_record_by_username(username)
    if record == DOESNOT_EXIST_ERROR:
        typer.secho(
            f"Please enter a valid username: {ERROR[DOESNOT_EXIST_ERROR]}",
            fg = typer.colors.RED
        )
        raise typer.Exit(1)
    if record == LOGIN_ERROR:
        typer.secho(
            f"Error in data fetch. {ERROR[LOGIN_ERROR]}",
            fg= typer.colors.RED
        )
        raise typer.Exit(1)
    new_record = dict()
    typer.secho(
        "Please enter the fields you want to update and leave blank to store previous data.",
        fg = typer.colors.RED
    )
    for key in record:
        if key == "key":
            continue
        if key == "password":
            new_record[key] = typer.prompt(f"Enter new {key}", hide_input=True, confirmation_prompt=True, default="")
            if new_record[key] == '' or new_record[key] == None:
                new_record[key] = record[key]
                new_record["key"] = record["key"]
            else:
                new_record[key], enc_key = Security().encrypt(new_record[key])
                new_record["key"] = enc_key
            continue
        new_record[key] = typer.prompt(f"Enter new {key}", default="")
        if new_record[key] == '' or new_record[key] == None:
                new_record[key] = record[key]
    
    updata_status = update_record(record, new_record, status)
    if updata_status != SUCCESS:
        typer.secho(
            f"Error on update: {ERROR[DB_UPDATE_ERROR]}. Make sure you are logined with admin or corresponding user credentials.",
            fg = typer.colors.RED
        )
        raise typer.Exit(1)
    
    typer.secho(
        "Record updated successfully. ",
        fg=typer.colors.GREEN
    )
    raise typer.Exit(1)

@app.command()
def delete():
    username = typer.prompt("Enter the username that you want to edit ")
    record, status = get_record_by_username(username)
    if record == DOESNOT_EXIST_ERROR:
        typer.secho(
            f"Please enter a valid username: {ERROR[DOESNOT_EXIST_ERROR]}",
            fg = typer.colors.RED
        )
        raise typer.Exit(1)
    if record == LOGIN_ERROR:
        typer.secho(
            f"Error in data fetch. {ERROR[LOGIN_ERROR]}",
            fg= typer.colors.RED
        )
        raise typer.Exit(1) 

    delete_status = delete_record(record, status)
    if delete_status == ADMIN_DELETE_ERROR:
        typer.secho(
            f"Error on delete: {ERROR[ADMIN_DELETE_ERROR]}.",
            fg = typer.colors.RED
        )
        raise typer.Exit(1)
    elif delete_status != SUCCESS:
        typer.secho(
            f"Error on delete: {ERROR[DB_UPDATE_ERROR]}. Make sure you are logined with admin or corresponding user credentials.",
            fg = typer.colors.RED
        )
        raise typer.Exit(1)
    
    typer.secho(
        "Record deleted successfully. ",
        fg=typer.colors.GREEN
    )
    raise typer.Exit(1)


@app.command()
def logout():
    confirmation = typer.confirm("Are you sure you want to logout?")
    if confirmation:
        session_status = logout_user()
        if session_status != SUCCESS:
            typer.secho(
                f"Error: {ERROR[SESSION_DELETE_ERROR]}",
                fg = typer.colors.RED
            )
            raise typer.Exit(1)
        typer.secho(
            "You have been logged out of the system."
        )
        typer.Exit(1)
    else:
        typer.secho("Aborting operation")
        raise typer.Abort()
