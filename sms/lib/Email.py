import os 
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

from sms import EMAIL_ERROR, SUCCESS



def send_email(to_email, name):
    load_dotenv()
    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'Registration Confirmation'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(f'Hi {name}!\n\n You have been registered for workshop.')

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return EMAIL_ERROR

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)
    return SUCCESS
