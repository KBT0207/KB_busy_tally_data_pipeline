import sys
import time
from datetime import date, datetime, timedelta
import pandas as pd
from busy import main_busy
from database import main_db
from database.db_crud import DatabaseCrud
from database.sql_connector import kbbio_connector
from logging_config import logger
from main_reports.reports import Reports
from tally import main_tally
from utils.common_utils import (balance_comp_codes, batch_date,
                                receivables_comp_codes, tally_comp_codes, 
                                kbe_outstanding_comp_codes, )
from database.models.base import KBBIOBase
from database.sql_connector import kbbio_engine, kbbio_connector
from glob import glob 
from database.tally_data_processor import TallyDataProcessor


from database.main_db import get_filename, get_compname

from database.busy_data_processor import *



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
    time.sleep(1)
    main_db.delete_busy_material(from_date= fromdate_str, to_date= todate_str)
    main_db.truncate_busy_masters()
    main_db.import_busy_masters_material(file_name= file_name)






if __name__ == "__main__":
    daily_busy_purchase()
    daily_busy_stock()
    busy_material_masters()

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







