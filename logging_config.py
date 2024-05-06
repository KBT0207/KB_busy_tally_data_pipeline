import logging
import logging.config
from logging.handlers import RotatingFileHandler
from utils.email import  YagmailHandler
import yagmail
import os
from datetime import datetime
from logtail import LogtailHandler



yag = yagmail.SMTP('Jovo@kaybeebio.com', os.getenv('SENDER_EMAIL_PASSWORD'))

email_recipients = ['s.gaurav@kaybeeexports.com', 'danish@kaybeeexports.com']
#email_recipients = ['s.gaurav@kaybeeexports.com']


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
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'logs/main_{today_date}.log',
            'maxBytes': 10485760,  # 10 mb
            'backupCount': 30,
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
            'subject': 'Critical Log',
            'formatter': 'standard'
        },
        'better_stack_handler':{
            'class': 'logtail.LogtailHandler',
            'formatter': 'standard',
            'level': 'INFO',
            'source_token': os.getenv('SOURCE_TOKEN')
        }

    },
    'loggers': {
        '': {
            'handlers': ['file_handler',  'critical_email_handler', 'better_stack_handler'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("main")
#logger_db = logging.getLogger("db")
