import pyautogui as pg
import time
from tally import tally_utils
from utils.common_utils import tally_reports
from datetime import datetime, timedelta
from logging_config import logger



def exporting_data(company):
    pg.hotkey("win", "d")
    todays_date = datetime.today().strftime("%d-%b-%Y")
    # todays_date = "Apr-17-May-24"
    from_date = (datetime.today() - timedelta(days=2)).strftime("%d-%m-%Y")
    # from_date = "1-4-2017"
    to_date = datetime.today().strftime("%d-%m-%Y")
    # to_date = "15-5-2024"

    tally_utils.start_tally()
    logger.info("Tally started...")

    for comp in company:
        tally_utils.select_company(company_code= comp)
        logger.info(f"{comp} selected...")
        for rep in list(tally_reports.keys()):
            
            tally_utils.exporting_reports(report= rep, 
                        from_date= from_date, to_date= to_date,
                        path= fr"D:\automated_tally_downloads\{comp}\{tally_reports[rep]}",
                        filename= f"{comp}_{tally_reports[rep]}_{todays_date}.xlsx", 
                        esc= 4)
            logger.info(f"Exported {tally_reports[rep]} of {comp} of {todays_date}")

        tally_utils.accounts()
        tally_utils.export_accounts_data(path= fr"D:\automated_tally_downloads\{comp}\accounts",
                        filename= f"{comp}_accounts_{todays_date}.xlsx")
        time.sleep(2)
        pg.press('esc')
        time.sleep(2)
        pg.press('esc')
        logger.info(f"Exported accounts of {comp} of {todays_date}")

        tally_utils.change_company()
    
    time.sleep(2)
    pg.press('esc')
    time.sleep(2)
    pg.press('y')
    logger.info("Tally closed ...")



def exporting_tally_items():
    pg.hotkey("win", "d")
    todays_date = datetime.today().strftime("%d-%b-%Y")

    tally_utils.start_tally()
    logger.info("Tally started...")

    tally_utils.select_company(company_code= 20001)
    tally_utils.items()
    tally_utils.export_accounts_data(path= fr"D:\automated_tally_downloads\items",
                    filename= f"tally_items_{todays_date}.xlsx")   
    
    logger.info(f"Exported items data of {todays_date}")
    
    time.sleep(1)
    pg.press('esc')
    time.sleep(1)
    pg.press('esc')
    time.sleep(1)
    pg.press('esc')
    pg.press('y')
    logger.info("Tally closed ...")

