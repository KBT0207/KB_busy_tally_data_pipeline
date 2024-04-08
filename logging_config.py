# logging_config.py

import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
from redmail import EmailSender

# Change these variables with your email settings
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'your_email@example.com'
EMAIL_PASSWORD = 'your_email_password'
RECIPIENT_EMAIL = 'recipient@example.com'



email = EmailSender(host= 'host',
                    port= 537,
                    username= 'emailsender',
                    password= 'use .env variable' )


# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'standard'
        },
        'email_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'daily_logs.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file_handler', 'email_handler'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)


recievers_list = []


    # Create an attachment
email.send(
    subject="important email",
    receivers= recievers_list,
    text= "Today's logs",

)
