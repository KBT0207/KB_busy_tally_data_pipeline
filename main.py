import time
import schedule
import pyautogui as pg
from utils.email import send_daily_logs
from database import main_db
from busy import main_busy
from tally import tally_utils


def data_busy_to_sql_async():
    main_busy.exporting_and_emailing()
    time.sleep(2)
    main_db.delete_busy_data()
    main_db.import_busy_data()


if __name__ == "__main__":
    tally_utils.start()
    # pg.hotkey("alt", "tab")
    # tally_utils.export_data(path= r"D:\automatic_tally_downloads\10009\sales", 
    #                         filename= "sales.xlsx")
    # main_busy.exporting_and_emailing()
    # main_db.delete_busy_data()
    # main_db.import_busy_data()
    # main_db.test()
    # schedule.every().day.at("23:26").do(data_busy_to_sql_async)
    # schedule.every().day.at("23:20").do(send_daily_logs)
    
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

