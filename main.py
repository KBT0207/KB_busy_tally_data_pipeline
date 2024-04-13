import time
from busy import rep1
from utils import email
import schedule
import logging 
from logging_config import LOGGING_CONFIG 
import yagmail


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("main")


if __name__ == "__main__":
    rep1.local_sales_report()

    
