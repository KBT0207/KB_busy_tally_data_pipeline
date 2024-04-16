import time
from busy import rep1
import schedule
import pyautogui as pg



if __name__ == "__main__":
    # pg.hotkey("alt", "tab")
    # time.sleep(0.5)
    # rep1.test()
    #rep1.transaction_report_selection(report= rep1.select_sales_list())

    schedule.every().day.at("21:00").do(rep1.local_sales_report)

    while True:
        schedule.run_pending()
        time.sleep(1)  
       
