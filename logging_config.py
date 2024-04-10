import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
import time

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
            'filename': 'logs/main.log',
            'formatter': 'standard'
        },
        'email_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/daily_logs.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'standard'
        },
        'critical_email_handler': {
            'class': 'logging_config.CriticalEmailHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file_handler', 'email_handler', 'critical_email_handler'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

class CriticalEmailHandler(logging.Handler):
    def emit(self, record):
        if record.levelno >= logging.CRITICAL:
            # Import email here to avoid circular import
            from utils import email
            email.send_logs_email()

# Define a function to send logs via email
def send_logs_email():
    # Import email here to avoid circular import
    from utils import email
    email.send(
        subject="important email",
        receivers=['sharmagaurav4510@gmail.com'],
        text="Today's logs",
    )
    logging.info("Logs sent via email.")
