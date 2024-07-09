import time
import schedule
import pandas as pd
from datetime import date, datetime, timedelta
from database import main_db
from busy import main_busy
from tally import main_tally
from utils.common_utils import tally_comp_codes, balance_comp_codes, receivables_comp_codes
from main_reports.reports import Reports
from database.sql_connector import db_connector


def tally_to_sql():
    current_date = datetime.today().strftime("%d-%b-%Y")
    # current_date = '29-Jun-24'
    # startdate = (datetime.today().date() - timedelta(days=2)).strftime("%Y-%m-%d")
    startdate = '2024-06-25'
    endate = (datetime.today().date() - timedelta(days=1)).strftime("%Y-%m-%d")
    # endate = '2024-06-29'
    companies = sorted(list(tally_comp_codes.keys()))
    
    main_tally.exporting_data(company=companies, fromdate= startdate, todate= endate, filename= current_date)
    main_db.delete_tally_data(start_date= startdate, end_date= endate, commit=True)
    main_db.import_tally_data(date= current_date)


def busy_sales():
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


def busy_material_masters():
    main_busy.exporting_master_and_material()
    time.sleep(1)
    main_db.delete_busy_material()
    main_db.truncate_busy_masters()
    main_db.import_busy_masters_material()


def export_import_outstanding_tallydata():
    
    first_day_of_current_month = datetime.today().replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

    fromdate = first_day_of_previous_month.strftime('%Y-%m-%d')
    todate = last_day_of_previous_month.strftime('%Y-%m-%d')
    date_list = pd.date_range(start=fromdate, end=todate).to_list()
    date_list_str = [date.strftime('%d-%m-%Y') for date in date_list]
    yesterday = [(datetime.today().date() - timedelta(days=1)).strftime("%d-%m-%Y")]

    companies = sorted(list(balance_comp_codes.keys()))
    
    if datetime.today().day == 10:
        monthly = True
        dates = date_list_str
    else:
        monthly = False
        dates = yesterday
    main_tally.exporting_outstanding_balance(company=companies, dates=dates, monthly=monthly)
    main_db.import_outstanding_tallydata(dates=dates, monthly = monthly)


def scheduled_outstanding_balance():
    if datetime.today().day != 10:
        schedule.every().day.at("03:15").do(export_import_outstanding_tallydata)
    else:
        schedule.every().day.at("10:30").do(export_import_outstanding_tallydata)



def export_import_receivables_tallydata():
    dates = [(datetime.today().date()- timedelta(days=1)).strftime("%d-%m-%Y"),
             (datetime.today().date()- timedelta(days=2)).strftime("%d-%m-%Y"),
             (datetime.today().date()- timedelta(days=3)).strftime("%d-%m-%Y"),
             (datetime.today().date()- timedelta(days=4)).strftime("%d-%m-%Y"),
             (datetime.today().date()- timedelta(days=5)).strftime("%d-%m-%Y"),
             ]                    #yesterday
    companies = sorted(list(receivables_comp_codes.keys()))
    main_tally.exporting_receivables(company= companies, dates= dates)
    main_db.import_receivables_tallydata(dates=dates)


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


if __name__ == "__main__":

    schedule.every().day.at("21:00").do(busy_sales)

    scheduled_outstanding_balance()
        
    schedule.every().day.at("00:05").do(busy_material_masters)

    # # schedule.every().day.at("10:00").do(reports)
    
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


