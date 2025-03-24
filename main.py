import sys
import time
from datetime import date, datetime, timedelta
import pandas as pd
from busy import main_busy
from database import main_db, tally_data_processor
from database.db_crud import DatabaseCrud
from logging_config import logger
from tally import main_tally, tally_utils
from utils.common_utils import (company_dict_kaybee_exports, fcy_company)
from database.sql_connector import kbe_engine
from database.models.base import KBEBase

def daily_busy_purchase():
    date1 = "2024-04-01"
    # date2 = "2024-03-31"
    
    # date1 = (datetime.today().date()-timedelta(days=180)).strftime('%Y-%m-%d')
    date2 = datetime.today().date().strftime('%Y-%m-%d')
    
    file_name = f'{date1} to {date2}'
    main_busy.exporting_purchase(start_date= date1, end_date= date2, 
                            filename= file_name)
    time.sleep(1)
    main_db.delete_busy_purchase(startdate= date1, enddate= date2, commit= True)
    main_db.import_busyrm_purchase(filename= file_name)
    
def daily_busy_stock():
    date1 = "2024-04-01"
    # date2 = "2024-03-31"
    
    # date1 = (datetime.today().date()-timedelta(days=180)).strftime('%Y-%m-%d')
    date2 = datetime.today().date().strftime('%Y-%m-%d')
    
    file_name = f'{date1} to {date2}'
    main_busy.exporting_stock(start_date= date1, end_date= date2, 
                            filename= file_name)
    time.sleep(1)
    main_db.delete_busy_stock(startdate= date1, enddate= date2, commit= True)
    main_db.import_busy_stock(filename= file_name)
    
def busy_material_masters():
    # if manual download kindly reffer this
    fromdate = "01-04-2024"
    # todate = "31-03-2024"
    # end_date = '2024-02-17'

    
    # fromdate = datetime.now().replace(day=180).strftime("%d-%m-%Y")

    todate = datetime.today().strftime("%d-%m-%Y")

    fromdate_str = datetime.strptime(fromdate, "%d-%m-%Y").strftime("%Y-%m-%d")
    todate_str = datetime.strptime(todate, "%d-%m-%Y").strftime("%Y-%m-%d")
    
    file_name = f'{fromdate_str} to {todate_str}-{datetime.today().strftime("%Y-%m-%d")}'
    
    # file_name = f'{fromdate_str} to {todate_str}-{end_date}'
    
    main_busy.exporting_master_and_material(from_date= fromdate, to_date=todate, filename= file_name, send_email= False)
    # time.sleep(1)
    main_db.delete_busy_material(from_date= fromdate_str, to_date= todate_str)
    main_db.truncate_busy_masters()
    main_db.import_busy_masters_material(file_name= file_name)


def tally_kbexports():
    # fromdate = '2024-04-01'
    fromdate = (datetime.today().date()-timedelta(days=180)).strftime('%Y-%m-%d')
    today = datetime.today().date().strftime('%Y-%m-%d')
    # today = '2025-03-23'

    main_tally.exporting_data(company=list(company_dict_kaybee_exports.keys()), 
                                fromdate=fromdate, 
                                todate=today, 
                                filename=today)
    
    main_db.delete_tally_data(start_date=fromdate,end_date=today, file_date=today, commit=True)
    main_db.import_tally_data(date=today)

def fcy_tally_kbexports():
    # fromdate = '2024-04-01'
    fromdate = (datetime.today().date()-timedelta(days=180)).strftime('%Y-%m-%d')
    today = datetime.today().date().strftime('%Y-%m-%d')
    # today = '2024-04-02'
    main_tally.fcy_exporting_data(fromdate=fromdate, todate=today,
                                company=list(fcy_company.keys()),
                                filename=today)
    main_db.delete_tally_data(start_date=fromdate,end_date=today, file_date=today, commit=True)
    main_db.import_tally_data(date=today)

if __name__ == "__main__":
    daily_busy_purchase()
    daily_busy_stock()
    busy_material_masters()
    tally_kbexports()
    fcy_tally_kbexports()

    # function_name = sys.argv[1] if len(sys.argv) > 1 else None
    # if function_name:
    #     if function_name in globals() and callable(globals()[function_name]):
    #         try:
    #             logger.info(f"Running function: {function_name}")
    #             globals()[function_name]()
    #         except Exception as e:
    #             logger.error(f"Error running function {function_name}: {e}")
    #     else:
    #         logger.error(f"Function '{function_name}' does not exist.")








