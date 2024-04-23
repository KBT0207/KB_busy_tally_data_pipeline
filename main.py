import time
from busy import rep1
import schedule
import pyautogui as pg
from utils.email import  send_daily_logs
from datetime import datetime
from database import main_sql



if __name__ == "__main__":
    
    #main_sql.main_sql()
    
    schedule.every().day.at("23:30").do(send_daily_logs)
    schedule.every().day.at("21:00").do(rep1.local_sales_report)

    while True:
        schedule.run_pending()
        time.sleep(1)  