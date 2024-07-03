import pyautogui as pg
import time
from tally import tally_utils
from utils.common_utils import tally_reports
from datetime import datetime, timedelta
from logging_config import logger



def exporting_data(company, fromdate:str, todate:str, filename:str):
    pg.hotkey("win", "d")
    # todays_date = datetime.today().strftime("%d-%b-%Y")
    # todays_date = "29-Jun-24"
    # # from_date = (datetime.today() - timedelta(days=8)).strftime("%d-%m-%Y")
    from_date_str = datetime.strptime(fromdate, '%Y-%m-%d').strftime('%d-%m-%Y')
    to_date_str = datetime.strptime(todate, '%Y-%m-%d').strftime('%d-%m-%Y')

    tally_utils.start_tally()
    logger.info("Tally started...")

    for comp in company:
        tally_utils.select_company(company_code= comp)
        logger.info(f"{comp} selected...")
        for rep in list(tally_reports.keys()):
            
            tally_utils.exporting_reports(report= rep, 
                        from_date= from_date_str, to_date= to_date_str,
                        path= fr"D:\automated_tally_downloads\{comp}\{tally_reports[rep]}",
                        filename= f"{comp}_{tally_reports[rep]}_{filename}.xlsx", 
                        esc= 4)
            logger.info(f"Exported {tally_reports[rep]} of {comp} of {filename}")
                
        tally_utils.accounts()
        tally_utils.export_accounts_data(path= fr"D:\automated_tally_downloads\{comp}\accounts",
                        filename= f"{comp}_accounts_{filename}.xlsx")    

        time.sleep(2)
        pg.press('esc')
        time.sleep(2)
        pg.press('esc')
        logger.info(f"Exported accounts of {comp} of {filename}")

        tally_utils.change_company()
    
    time.sleep(2)
    pg.press('esc')
    time.sleep(2)
    pg.press('y')
    logger.info("Tally closed ...")




def exporting_outstanding_balance(company:list, dates:list):
    pg.hotkey("win", "d")
    
    tally_utils.start_tally()
    logger.info("Tally started...")

    for comp in company:
        tally_utils.select_company(company_code= comp)
        logger.info(f"{comp} selected...")
        
        tally_utils.outstanding_balance()
        
        for date in dates:
            tally_utils.change_period_balance(from_date= '01-04-2024', to_date= date)
            tally_utils.export_balance_data(path= fr"D:\automated_tally_downloads\{comp}\outstanding",
                            filename= f"{comp}_outstanding_{date}.xlsx")
            time.sleep(1.5)

        tally_utils.back_to_tally_home(times= 3)
        logger.info(f"Exported outstanding balance of {comp} of {date}")

        tally_utils.change_company()
    
    time.sleep(2)
    pg.press('esc')
    time.sleep(2)
    pg.press('y')
    logger.info("Tally closed ...")



def exporting_receivables(company:list, dates:list):
    pg.hotkey("win", "d")
    
    tally_utils.start_tally()
    logger.info("Tally started...")

    for comp in company:
        tally_utils.select_company(company_code= comp)
        logger.info(f"{comp} selected...")
        
        tally_utils.receivables()
        
        for date in dates:
            tally_utils.change_receivables_period(from_date= '01-04-2024', to_date= date)
            tally_utils.export_balance_data(path= fr"D:\automated_tally_downloads\{comp}\receivables",
                            filename= f"{comp}_receivables_{date}.xlsx")
            time.sleep(1)

        tally_utils.back_to_tally_home(times= 6)
        logger.info(f"Exported receivables of {comp} of {date}")

        tally_utils.change_company()
    
    time.sleep(2)
    pg.press('esc')
    time.sleep(2)
    pg.press('y')
    logger.info("Tally closed ...")
