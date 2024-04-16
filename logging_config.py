import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
from utils.email import YagmailDailyHandler, YagmailHandler
import yagmail
import os
from datetime import datetime


# Import Yagmail and configure email sender
yag = yagmail.SMTP('jovokb@gmail.com', os.getenv('SENDER_EMAIL_PASSWORD'))

email_recipients = ['s.gaurav@kaybeeexports.com', 'sharmagaurav4510@gmail.com', 'danish@kaybeeexports.com']

today_date = datetime.now().strftime('%d-%b-%Y')

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
            'filename': f'logs/main_{today_date}.log',
            'when': 'S',
            'interval': 86400, 
            'atTime': '22:30', 
            'backupCount': 0,
            'formatter': 'standard'
        },
        'daily_email_handler': {
            'class': 'utils.email.YagmailDailyHandler',
            'to': email_recipients,
            'subject': 'Daily Log from Python Application',
            'formatter': 'standard'
        },
        'critical_email_handler': {
            'class': 'logging.handlers.MemoryHandler',
            'target': 'yagmail_handler',
            'level': 'CRITICAL',
            'formatter': 'standard',
            'capacity': 100
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
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("main")
