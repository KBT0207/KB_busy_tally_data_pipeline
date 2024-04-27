import time
from busy import main_busy
import schedule
import pyautogui as pg
from utils.email import  send_daily_logs
from datetime import datetime
from database import main_sql
from busy import email_busy_reports


def data_busy_to_sql():
    main_busy.exporting_and_emailing()  #Exports data and emails it from busy
    time.sleep(5)
    main_sql.delete_then_import_to_sql()  #Imports data into Database


if __name__ == "__main__":

    schedule.every().day.at("23:00").do(send_daily_logs)
    schedule.every().day.at("21:00").do(data_busy_to_sql)

    while True:
        schedule.run_pending()
        time.sleep(1)  