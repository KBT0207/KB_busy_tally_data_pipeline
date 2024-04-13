import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
from utils.email import YagmailDailyHandler  # Import YagmailDailyHandler from email module
import yagmail
import os

# Import Yagmail and configure email sender
yag = yagmail.SMTP('jovokb@gmail.com',  os.getenv('SENDER_EMAIL_PASSWORD'))

email_recipients = ['sharmagaurav4510@gmail.com']

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s'
        }
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/app.log',
            'when': 'midnight',
            'interval': 7, 
            'backupCount': 0, 
            'formatter': 'standard'
        },
        'daily_email_handler': {
            'class': 'utils.email.YagmailDailyHandler',  # Specify correct import path
            'to': email_recipients,
            'subject': 'Daily Log from Python Application',
            'formatter': 'standard'
        },
        'critical_email_handler': {
            'class': 'logging.handlers.MemoryHandler',
            'target': 'yagmail_handler',
            'level': 'CRITICAL',  # Only process critical messages
            'formatter': 'standard',
            'capacity': 100  # Specify the capacity (number of records to buffer)
        },
        'yagmail_handler': {
            'class': 'utils.email.YagmailHandler',
            'to': email_recipients,
            'subject': 'Log from Python Application',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file_handler', 'daily_email_handler', 'critical_email_handler'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

