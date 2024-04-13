import time
from busy import rep1
from utils import email
import schedule
import logging 
from logging_config import LOGGING_CONFIG , logger
import yagmail





def test():
        try:
            1/1
            logger.info("Divided")
        except ZeroDivisionError as e:
            print(e)
            logger.critical("failed") 

if __name__ == "__main__":
    #rep1.local_sales_report()
    
    test()    
