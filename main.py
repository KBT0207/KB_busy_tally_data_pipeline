import time
from busy import rep1
import schedule
from logging_config import LOGGING_CONFIG , logger



if __name__ == "__main__":
    
    schedule.every().day.at("21:00").do(rep1.local_sales_report)

    while True:
        schedule.run_pending()
        time.sleep(1)  
       
