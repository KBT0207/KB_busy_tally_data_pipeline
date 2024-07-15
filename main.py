import time
import schedule
import pandas as pd
from datetime import date, datetime, timedelta
from Database import main_db
from busy import main_busy
from tally import main_tally
from utils.common_utils import tally_comp_codes, balance_comp_codes, receivables_comp_codes
from utils.common_utils import batch_date
from main_reports.reports import Reports
from Database.sql_connector import db_connector
from Database.db_crud import DatabaseCrud
import sys
from logging_config import logger



def tally_to_sql():
    if datetime.today().day not in [4, 19]:
        current_date = datetime.today().strftime("%d-%b-%Y")
        # current_date = '29-Jun-24'
        startdate = (datetime.today().date() - timedelta(days=2)).strftime("%Y-%m-%d")
        # startdate = '2024-06-25'
        endate = (datetime.today().date() - timedelta(days=1)).strftime("%Y-%m-%d")
        # endate = '2024-06-29'
    else:
        first_day_of_current_month = datetime.today().replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
        current_date = f'{startdate}-{endate}'
        # current_date = '29-Jun-24'

        startdate = first_day_of_previous_month.strftime("%Y-%m-%d")
        # startdate = '2024-06-25'
        endate = (datetime.today().date() - timedelta(days=1)).strftime("%Y-%m-%d")
        # endate = '2024-06-29'
    companies = sorted(list(tally_comp_codes.keys()))
    
    main_tally.exporting_data(company=companies, fromdate= startdate, todate= endate, filename= current_date)
    main_db.delete_tally_data(start_date= startdate, end_date= endate, commit=True)
    main_db.import_tally_data(date= current_date)



def daily_busy_sales():
    # fromdate_str = '25-06-2024'
    # todate_str = (datetime.today().date()-timedelta(days=1)).strftime('%d-%m-%Y')
    file_name = datetime.today().date().strftime('%d-%b-%Y')
    date1 = (datetime.today().date()-timedelta(days=2)).strftime('%Y-%m-%d')
    # date1= "2024-06-25"
    date2 = datetime.today().date().strftime('%Y-%m-%d')
    # date2= "2024-06-29"

    main_busy.exporting_sales(start_date= date1, end_date= date2, 
                              filename= file_name, send_email= True)
    time.sleep(1)
    main_db.delete_busy_sales(startdate= date1, enddate= date2, commit= True)
    main_db.import_busy_sales(filename= file_name)



def monthly_busy_sales():
    first_batch = batch_date(month= datetime.today().month - 1, batch= 1)
    second_batch = batch_date(month= datetime.today().month - 1, batch= 2)
    third_batch = batch_date(month= datetime.today().month - 1, batch= 3)
    
    if datetime.today().day == 1:
        dates = first_batch
    elif datetime.today().day == 2:
        dates = second_batch
    elif datetime.today().day == 3:
        dates = third_batch

    filename = f'{dates[0]}-{dates[-1]}'

    main_busy.exporting_sales(start_date= dates[0], end_date= dates[-1], 
                              filename= filename, send_email= True)
    time.sleep(1)
    main_db.delete_busy_sales(startdate= dates[0], enddate= dates[-1], commit= True)
    main_db.import_busy_sales(filename= filename)



def busy_material_masters():
    fromdate = datetime.now().replace(day=1).strftime("%d-%m-%Y")
    todate = datetime.today().strftime("%d-%m-%Y")

    filename = datetime.today().strftime("%d-%b-%Y")
    main_busy.exporting_master_and_material(from_date= fromdate, to_date=todate)
    time.sleep(1)
    main_db.delete_busy_material(from_date= fromdate, to_date= todate)
    main_db.truncate_busy_masters()
    main_db.import_busy_masters_material(file_name= filename)



def daily_outstanding_tallydata():
 
    yesterday = [(datetime.today().date() - timedelta(days=1)).strftime("%d-%m-%Y")]
    companies = sorted(list(balance_comp_codes.keys()))
    dates = yesterday
    main_tally.exporting_outstanding_balance(company=companies, dates=dates, monthly=False)
    main_db.import_outstanding_tallydata(dates=dates, monthly = False)



def monthly_outstanding_tallydata():
    first_batch = batch_date(month= datetime.today().month - 1, batch= 1)
    second_batch = batch_date(month= datetime.today().month - 1, batch= 2)
    third_batch = batch_date(month= datetime.today().month - 1, batch= 3)

    companies = sorted(list(balance_comp_codes.keys()))
    
    if datetime.today().day == 1:
        monthly = True
        dates = first_batch
    elif datetime.today().day == 2:
        monthly = True
        dates = second_batch
    elif datetime.today().day == 3:
        monthly = True
        dates = third_batch
    main_tally.exporting_outstanding_balance(company=companies, dates=dates, monthly=monthly)
    db = DatabaseCrud(db_connector)
    db.delete_date_range_query(table_name= 'outstanding_balance', start_date= dates[0], end_date= dates[-1], commit= True)
    main_db.import_outstanding_tallydata(dates=dates, monthly = monthly)



def daily_receivables_tallydata():
    dates_list = pd.date_range(start= '2024-06-06' , end= '2024-06-12')
    date_list_str = [d.strftime('%d-%m-%Y') for d in dates_list]
    # yesterday = [(datetime.today().date() - timedelta(days=1)).strftime("%d-%m-%Y")]
    # dates = yesterday
    companies = sorted(list(receivables_comp_codes.keys()))
    main_tally.exporting_receivables(company= companies, dates= date_list_str)
    main_db.import_receivables_tallydata(dates= date_list_str, monthly= False)



def monthly_receivables_tallydata():
    first_batch = batch_date(month= datetime.today().month - 1, batch= 1)
    second_batch = batch_date(month= datetime.today().month - 1, batch= 2)
    third_batch = batch_date(month= datetime.today().month - 1, batch= 3)

    companies = sorted(list(receivables_comp_codes.keys()))
    
    if datetime.today().day == 1:
        monthly = True
        dates = first_batch
    elif datetime.today().day == 2:
        monthly = True
        dates = second_batch
    elif datetime.today().day == 3:
        monthly = True
        dates = third_batch
    main_tally.exporting_receivables(company=companies, dates=dates, monthly=monthly)
    db = DatabaseCrud(db_connector)
    db.delete_date_range_query(table_name= 'tally_receivables', start_date= dates[0], end_date= dates[-1], commit= True)
    main_db.import_receivables_tallydata(dates=dates, monthly = monthly)



def reports():
    fromdate = datetime.today().date().replace(day=1).strftime('%Y-%m-%d')
    # fromdate = '2024-06-01'
    todate = (datetime.today().date() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    main_db.dealer_price_validation_report(from_date= fromdate, 
                                           to_date= todate, send_email= True, 
                                        #    exceptions= salesprice_excluded_invoices,
                                           )

    main_db.salesorder_salesman_report(from_date= fromdate, 
                                       to_date=todate, send_email= True,
                                       exceptions= None,
                                       )

    # from_date_str = datetime.strptime(fromdate, '%Y-%m-%d')
    # to_date_str = datetime.strptime(todate, '%Y-%m-%d')


    date_list_str = [todate]
    main_db.volume_discount_report(dates= date_list_str, send_email=True, 
                                   exceptions= ['KAYBEE/001 A'])

    main_db.cash_discount_report(dates= date_list_str, send_email=True, 
                                   exceptions= ['KAYBEE/001 A'])
    

    report = Reports(db_connector)
    ref_date = '2024-04-01'
    report.populate_debtor_balances(fromdate= ref_date, todate= todate, 
                                    filename= f'Debtors_Balance_{ref_date}-{todate}', 
                                    to_import= True, to_export= False, commit= True,
                                    )



def reco_reports():
    fromdate = (datetime.today() - timedelta(days= 9)).strftime('%Y-%m-%d')
    todate = (datetime.today() - timedelta(days= 3)).strftime('%Y-%m-%d')
    # date_list = pd.date_range(start= datetime.today() - timedelta(days= 9), 
    #                           end= datetime.today() - timedelta(days= 3), 
    #                           ).to_list()
    # date_list_str = [date.strftime('%Y-%m-%d') for date in date_list]

    main_db.busy_tally_sales_reco(start_date= fromdate, end_date= todate, send_email= True, 
                                #   exceptions= , 
                                  )

    main_db.busy_tally_salesreturn_reco(start_date= fromdate , end_date= todate, send_email= True, 
                                #   exceptions= , 
                                  )    

    # main_db.salesorder_mitp_reco_report(start_date= fromdate , end_date= todate, send_email= True, 
    #                             #   exceptions= , 
    #                               )



def testing_1():
    print('testing func 1')


def testing_2():
    print('testing func 2')



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




