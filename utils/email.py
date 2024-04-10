import logging
import os
from logging_config import LOGGING_CONFIG 
from redmail import EmailSender
import schedule
import time
from dotenv import load_dotenv

load_dotenv()

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("email")


# Change these variables with your email settings
email = EmailSender(host='smtp.google.com',
                    port='537',
                    username='s.gaurav@kaybeeexports.com',
                    password=os.getenv('SENDER_EMAIL_PASSWORD'))


receivers_list = ['sharmagaurav4510@gmail.com']

# Define a function to send logs via email
def send_logs_email():
    email.send(
        subject="important email",
        receivers=receivers_list,
        text="Today's logs",
    )
    logging.info("Logs sent via email.")



def schedule_email_task():
    # Schedule email sending every day at 8:00 AM
    schedule.every().day.at("08:00").do(send_logs_email)

