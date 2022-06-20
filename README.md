# Student Management System

A console app to support **CRUD** operation, **Authentication**, **Session**, and **Access Control** between as single admin and students.

### Getting Started

First clone the repository from Github and switch to the new directory:
```
$ git clone https://github.com/utsavsubedi/StudentManagementSystem.git
$ cd StudentManagement
 ```  
Activate the virtualenv for your project.
    
Install project dependencies:
```
$ pip install -r requirements.txt
```

#### Set up your enviroment
create a .env file with in project directory for sending registration confimation mail as:
EMAIL_USER=*your gmail*
EMAIL_PASS=*your app pass/pass for gmail*

### Commands 

#### 1. To initialize the application 
```
$ python -m sms init
```
This command initialize the application with config file and database file. The app asks for a path to database, if not given then default path is used. The config file then records the path to the database. The default credentials for admin is set in initialization. User can log in as admin with 
```
$ username : admin
$ password : admin
```

#### 2. To register into application
```
$ python -m sms registration
```
This command allows user to register into the app. The user is asked for a no of fields, the registration is confirmed through sending mail to a valid email address throught smtp server.

#### 3. To login into application 
```
$ python -m sms login
```
The user is asked for username and password previously entered on registration. The passwords stored in database are encrypted using python cryptography module.

#### 4. To read records
```
$ python -m sms read
```
This operation reads data from database. Returns a single record for Student and all students record for admin.

#### 5. To update record
```
$ python -m sms update
```
User can update only their records and admin can access all students record. Leave blank if old data is to be used and enter new value if it needs to be modified.

#### 6. To delete record
```
$ python -m sms delete
```
User can delete only their records and admin can delete all other students records.
The record is deleted by unique username previously entered by user.

#### 7. To see app version
```
$ python -m sms --version 
$ python -m sms -v
```
Displays current version of the application.

### My References:
- https://realpython.com/python-typer-cli/
- https://typer.tiangolo.com/
- https://docs.python.org/3/library/smtplib.html


