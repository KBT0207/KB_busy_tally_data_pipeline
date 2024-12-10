import sys
import time
from datetime import date, datetime, timedelta
import pandas as pd
from busy import main_busy
from Database import main_db
from Database.db_crud import DatabaseCrud
from Database.sql_connector import kbbio_connector
from logging_config import logger
from main_reports.reports import Reports
from tally import main_tally
from utils.common_utils import (balance_comp_codes, batch_date,
                                receivables_comp_codes, tally_comp_codes, 
                                kbe_outstanding_comp_codes, )
from Database.models.base import KBBIOBase, KBEBase
from Database.sql_connector import kbbio_engine, kbbio_connector, kbe_engine, kbe_connector
from utils.common_utils import kbe_outstanding_comp_codes
from glob import glob 
from Database.tally_data_processor import TallyDataProcessor



def tally_to_sql():
    if datetime.today().day not in [4, 19]:
        # current_date = '29-Jun-24'
        startdate = (datetime.today().date() - timedelta(days=3)).strftime("%Y-%m-%d")
        # startdate = '2024-10-01'
        endate = (datetime.today().date() - timedelta(days=1)).strftime("%Y-%m-%d")
        # endate = '2024-06-29'
        
    else:
        first_day_of_current_month = datetime.today().replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
        # current_date = '29-Jun-24'

        startdate = first_day_of_previous_month.strftime("%Y-%m-%d")
        # startdate = '2024-06-25'
        endate = (datetime.today().date() - timedelta(days=2)).strftime("%Y-%m-%d")
        # endate = '2024-06-29'
    companies = sorted(list(tally_comp_codes.keys()))
    file_name = f'{startdate} to {endate}'
    
    main_tally.exporting_data(company=companies, fromdate= startdate, todate= endate, filename= file_name)
    main_db.delete_tally_data(start_date= startdate, end_date= endate, commit=True)
    main_db.import_tally_data(date= file_name)



def daily_busy_sales():
    # todate_str = (datetime.today().date()-timedelta(days=1)).strftime('%d-%m-%Y')
    date1 = (datetime.today().date()-timedelta(days=2)).strftime('%Y-%m-%d')
    # date1= "2024-11-11"
    date2 = datetime.today().date().strftime('%Y-%m-%d')
    # date2= "2024-11-13"
    file_name = f'{date1} to {date2}'
    main_busy.exporting_sales(start_date= date1, end_date= date2, 
                              filename= file_name, send_email= True)
    time.sleep(1)
    main_db.delete_busy_sales(startdate= date1, enddate= date2, commit= True)
    main_db.import_busy_sales(filename= file_name)



def daily_busy_purchase():
    # todate_str = (datetime.today().date()-timedelta(days=1)).strftime('%d-%m-%Y')
    date1 = (datetime.today().date()-timedelta(days=2)).strftime('%Y-%m-%d')
    # date1= "2024-11-11"
    date2 = datetime.today().date().strftime('%Y-%m-%d')
    # date2= "2024-11-13"
    file_name = f'{date1} to {date2}'
    main_busy.exporting_purchase(start_date= date1, end_date= date2, 
                              filename= file_name)
    time.sleep(1)
    main_db.delete_busy_purchase(startdate= date1, enddate= date2, commit= True)
    main_db.import_busy_purchase(filename= file_name)



def daily_busy_stock():
    # todate_str = (datetime.today().date()-timedelta(days=1)).strftime('%d-%m-%Y')
    date1 = (datetime.today().date()-timedelta(days=2)).strftime('%Y-%m-%d')
    # date1= "2024-11-20"
    date2 = datetime.today().date().strftime('%Y-%m-%d')
    # date2= "2024-12-03"
    file_name = f'{date1} to {date2}'
    main_busy.exporting_stock(start_date= date1, end_date= date2, 
                              filename= file_name)
    time.sleep(1)
    main_db.delete_busy_stock(startdate= date1, enddate= date2, commit= True)
    main_db.import_busy_stock(filename= file_name)



# def monthly_busy_sales():
#     previous_month_number = datetime.today().month - 1
#     first_batch = batch_date(month=  previous_month_number, batch= 1)
#     second_batch = batch_date(month=  previous_month_number, batch= 2)
#     third_batch = batch_date(month= previous_month_number, batch= 3)

#     if datetime.today().day in [1,10,20]:
#         dates = first_batch
#     elif datetime.today().day in [2,11,21]:
#         dates = second_batch
#     elif datetime.today().day in [3,12,22]:
#         dates = third_batch

#     # dates = second_batch
#     dates_str = [datetime.strptime(d,('%d-%m-%Y')).strftime('%Y-%m-%d') for d in dates]
#     filename = f'{dates_str[0]} to {dates_str[-1]}'

#     main_busy.exporting_sales(start_date= dates_str[0], end_date= dates_str[-1], 
#                             filename= filename, send_email= False)
#     time.sleep(1)
#     main_db.delete_busy_sales(startdate= dates_str[0], enddate= dates_str[-1], commit= True)
#     time.sleep(1)
#     main_db.import_busy_sales(filename= filename)
#     time.sleep(1)



def busy_material_masters():
    fromdate = datetime.now().replace(day=1).strftime("%d-%m-%Y")

    todate = datetime.today().strftime("%d-%m-%Y")

    fromdate_str = datetime.strptime(fromdate, "%d-%m-%Y").strftime("%Y-%m-%d")
    todate_str = datetime.strptime(todate, "%d-%m-%Y").strftime("%Y-%m-%d")
    
    file_name = f'{fromdate_str} to {todate_str}-{datetime.today().strftime("%Y-%m-%d")}'
    
    main_busy.exporting_master_and_material(from_date= fromdate, to_date=todate, filename= file_name, send_email= True)
    time.sleep(1)
    main_db.delete_busy_material(from_date= fromdate_str, to_date= todate_str)
    main_db.truncate_busy_masters()
    main_db.import_busy_masters_material(file_name= file_name)



def monthly_material_masters():
    # Get the first day of the current month
    first_day_of_current_month = datetime.today().replace(day=1)
    # Get the last day of the previous month
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    # Get the first day of the previous month
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
    # Format the dates as dd-mm-yyyy
    fromdate = first_day_of_previous_month.strftime("%d-%m-%Y")
    # fromdate = '01-05-2023'
    todate = last_day_of_previous_month.strftime("%d-%m-%Y")
    # todate = '31-05-2023'

    fromdate_str = first_day_of_previous_month.strftime("%Y-%m-%d")
    todate_str = last_day_of_previous_month.strftime("%Y-%m-%d")
    file_name = f'{fromdate_str} to {todate_str}'
    main_busy.exporting_master_and_material(from_date= fromdate, to_date=todate, filename = file_name, send_email= False)
    time.sleep(1)
    main_db.delete_busy_material(from_date= fromdate_str, to_date= todate_str)
    main_db.truncate_busy_masters()
    main_db.import_busy_masters_material(file_name= file_name)



def daily_outstanding_tallydata():
    current_day = datetime.now().strftime('%A')
    if current_day == 'Tuesday':
        yesterday = [(datetime.today().date() - timedelta(days=2)).strftime("%d-%m-%Y"), (datetime.today().date() - timedelta(days=1)).strftime("%d-%m-%Y")]
    else:
        yesterday = [(datetime.today().date() - timedelta(days=1)).strftime("%d-%m-%Y")]
        # yesterday = ['18-08-2024', '19-08-2024', '20-08-2024']

    companies = sorted(list(balance_comp_codes.keys()))
    dates = yesterday
    # dates = ['01-12-2024']
    main_tally.exporting_outstanding_balance(company=companies, dates=dates, monthly=False)
    importer = DatabaseCrud(kbbio_connector)
    
    #imp
    dates_str = [datetime.strptime(date, "%d-%m-%Y") for date in yesterday]  

    importer.delete_date_range_query('outstanding_balance', start_date=dates_str[0].strftime("%Y-%m-%d"), end_date= dates_str[-1].strftime("%Y-%m-%d"), commit=True)
    main_db.import_outstanding_tallydata(dates=dates, monthly = False)



def monthly_outstanding_tallydata():
    previous_month_number = datetime.today().month - 1
    first_batch = batch_date(month= previous_month_number, batch= 1)
    second_batch = batch_date(month= previous_month_number, batch= 2)
    third_batch = batch_date(month= previous_month_number, batch= 3)

    companies = sorted(list(balance_comp_codes.keys()))
    
    if datetime.today().day in [1,23]:
        monthly = True
        dates = first_batch
    elif datetime.today().day in [2,24]:
        monthly = True
        dates = second_batch
    elif datetime.today().day in [3,25]:
        monthly = True
        dates = third_batch
    # dates = ['22-07-2024']
    dates_str = [datetime.strptime(d,('%d-%m-%Y')).strftime('%Y-%m-%d') for d in dates]
    monthly = True
    main_tally.exporting_outstanding_balance(company=companies, dates=dates, monthly=monthly)
    db = DatabaseCrud(kbbio_connector)
    db.delete_date_range_query(table_name= 'outstanding_balance', start_date= dates_str[0], end_date= dates_str[-1], commit= True)
    main_db.import_outstanding_tallydata(dates=dates, monthly = monthly)



def daily_receivables_tallydata():
    current_day = datetime.now().strftime('%A')
    if current_day == 'Tuesday':
        yesterday = [(datetime.today().date() - timedelta(days=2)).strftime("%d-%m-%Y"), (datetime.today().date() - timedelta(days=1)).strftime("%d-%m-%Y")]
    else:
        yesterday = [(datetime.today().date() - timedelta(days=1)).strftime("%d-%m-%Y")]
    # dates_list = pd.date_range(start= '2024-07-13', end= '2024-07-17')
    # date_list_str = [d.strftime('%d-%m-%Y') for d in dates_list]
    yesterday = [(datetime.today().date() - timedelta(days=1)).strftime("%d-%m-%Y")]
    companies = sorted(list(receivables_comp_codes.keys()))
    main_tally.exporting_receivables(company= companies, dates= yesterday, monthly= False)
    main_db.import_receivables_tallydata(dates= yesterday, monthly= False)



def monthly_receivables_tallydata():
    previous_month_number = datetime.today().month - 1
    first_batch = batch_date(month= previous_month_number, batch= 1)
    second_batch = batch_date(month= previous_month_number, batch= 2)
    third_batch = batch_date(month= previous_month_number, batch= 3)

    companies = sorted(list(receivables_comp_codes.keys()))
    
    if datetime.today().day in [1,23]:
        monthly = True
        dates = first_batch
    elif datetime.today().day in [2,24]:
        monthly = True
        dates = second_batch
    elif datetime.today().day in [3,25]:
        monthly = True
        dates = third_batch
    main_tally.exporting_receivables(company=companies, dates=dates, monthly=monthly)
    db = DatabaseCrud(kbbio_connector)
    db.delete_date_range_query(table_name= 'tally_receivables', start_date= dates[0], end_date= dates[-1], commit= True)
    main_db.import_receivables_tallydata(dates=dates, monthly = monthly)



def basic_reports():
    fromdate = datetime.today().date().replace(day=1).strftime('%Y-%m-%d')
    # fromdate = '2024-09-09'
    todate = (datetime.today().date() - timedelta(days=1)).strftime('%Y-%m-%d')
    # todate = '2024-08-22'

    main_db.dealer_price_validation_report(from_date= fromdate, 
                                           to_date= todate, send_email= True, effective_date= '2024-08-01',
                                        #    exceptions= salesprice_excluded_invoices,
                                           )

    main_db.salesorder_salesman_report(from_date= fromdate, 
                                       to_date=todate, send_email= True,
                                       exceptions= None,
                                       )

    from_date_str = datetime.strptime(fromdate, '%Y-%m-%d')
    to_date_str = datetime.strptime(todate, '%Y-%m-%d')
    dates_list = pd.date_range(start= from_date_str, end= to_date_str)
    date_list_str = [d.strftime('%Y-%m-%d') for d in dates_list]

    # date_list_str = [todate]
    main_db.volume_discount_report(dates= date_list_str, send_email=False, 
                                   exceptions= ['KAYBEE/001 A'])

    main_db.cash_discount_report(dates= date_list_str, send_email=False, 
                                   exceptions= ['KAYBEE/001 A'])
    

    report = Reports(kbbio_connector)
    ref_date = '2024-04-01'
    report.populate_debtor_balances(fromdate= ref_date, todate= todate, 
                                    filename= f'Debtors_Balance_{ref_date}-{todate}', 
                                    to_import= True, to_export= True, commit= True,
                                    )



def exchange_rate_updation():
    main_db.update_exchange_rate(dates= [datetime.today().strftime('%Y-%m-%d')])



def export_import_kbe_outstanding():
    today = [(datetime.today().date()).strftime("%d-%m-%Y")]
    # yesterday = ['18-08-2024', '19-08-2024', '20-08-2024']

    companies = sorted(list(kbe_outstanding_comp_codes.keys()))
    dates = today
    # dates = ['14-11-2024']
    
    main_tally.exporting_kbe_outstanding(company=companies, dates=dates)
    importer = DatabaseCrud(kbe_connector)
    KBEBase.metadata.create_all(kbe_engine)
    importer.truncate_table('outstanding_balance', commit=True)

    main_db.import_kbe_outstanding_tallydata(dates=dates)



def kbe_accounts_operations():
    today = datetime.today().strftime('%Y-%m-%d')
    # today = '2024-11-11'
    main_tally.exporting_kbe_accounts(company= kbe_outstanding_comp_codes.keys(), filename= today)

    db_crud = DatabaseCrud(kbe_connector)
    accounts_file = glob(rf"D:\automated_kbe_downloads\**\*kbe_accounts_{today}.xlsx", recursive= True)
    if accounts_file:
        for acc_file in accounts_file:
            clean_df = TallyDataProcessor(excel_file_path= acc_file)
            db_crud.import_kbe_accounts_data(df= clean_df.clean_and_transform(), commit= True)
            db_crud.clean_kbe_accounts_data(df= clean_df.clean_and_transform(), commit= True)
    else:
        logger.info(f"No files for account exported/found for {today}")






if __name__ == "__main__":


    function_name = sys.argv[1] if len(sys.argv) > 1 else None
    if function_name:
        if function_name in globals() and callable(globals()[function_name]):
            try:
                logger.info(f"Running function: {function_name}")
                globals()[function_name]()
            except Exception as e:
                logger.error(f"Error running function {function_name}: {e}")
        else:
            logger.error(f"Function '{function_name}' does not exist.")




