import time
from busy import rep1
import schedule
import pyautogui as pg
from utils.email import  send_daily_logs, email_send
from datetime import datetime


if __name__ == "__main__":
    # pg.hotkey("alt", "tab")
    # time.sleep(0.5)
    rep1.test()
    #rep1.local_sales_report()
# Schedule the send_logs method to run every minute
    # schedule.every().day.at("23:30").do(send_daily_logs)
    # schedule.every().day.at("21:00").do(rep1.local_sales_report)
    # # schedule.every(2).minutes.do(rep1.test)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)  