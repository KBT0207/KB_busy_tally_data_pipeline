import pyautogui as pg
from tally import tally_utils
from utils.common_utils import tally_reports
from datetime import datetime, timedelta
from logging_config import logger




def exporting_data(company):
    pg.hotkey("win", "d")
    todays_date = datetime.today().strftime("%d-%b-%Y")
    # todays_date = "Apr-17-Mar-23"
    from_date = (datetime.today() - timedelta(days=2)).strftime("%d-%m-%Y")
    # from_date = "1-4-2017"
    to_date = datetime.today().strftime("%d-%m-%Y")
    # to_date = "31-3-2023"

    try:
        tally_utils.start_tally()
        logger.info("Tally started...")
    except Exception as e:
        logger.critical(f"Failed to start tally!: {e}")

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
        tally_utils.change_company()



