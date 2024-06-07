import time
import schedule
from datetime import date, datetime, timedelta
from database import main_db
from busy import main_busy
from tally import main_tally
from utils.common_utils import tally_comp_codes, balance_comp_codes



def tally_to_sql():
    current_date = datetime.today().strftime("%d-%b-%Y")
    startdate = (datetime.today().date() - timedelta(days=2)).strftime("%Y-%m-%d")
    endate = (datetime.today().date() - timedelta(days=1)).strftime("%Y-%m-%d")
    companies = sorted(list(tally_comp_codes.keys()))
    
    main_tally.exporting_data(company=companies)
    main_db.delete_tally_data(start_date= startdate, end_date= endate, commit=True)
    main_db.import_tally_data(date= current_date)


def busy_sales():
    main_busy.exporting_sales()
    time.sleep(1)
    main_db.delete_busy_sales()
    main_db.import_busy_sales()


def busy_material_masters():
    main_busy.exporting_master_and_material()
    time.sleep(1)
    main_db.delete_busy_material()
    main_db.truncate_busy_masters()
    main_db.import_busy_masters_material()


def export_import_outstanding_tallydata():
    dates = [(datetime.today().date()- timedelta(days=1)).strftime("%d-%m-%Y")]                    #yesterday
    companies = sorted(list(balance_comp_codes.keys()))
    main_tally.exporting_outstanding_balance(company= companies, dates= dates)
    main_db.import_outstanding_tallydata(dates=dates)



def reports():
    fromdate = datetime.today().date().replace(day=1).strftime('%Y-%m-%d')
    todate = (datetime.today().date() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # salesprice_excluded_invoices = ['KBAKNU/2425/3']
    main_db.dealer_price_validation_report(from_date= fromdate, 
                                           to_date= todate, send_email= True, 
                                        #    exceptions= salesprice_excluded_invoices,
                                           )

    main_db.salesorder_salesman_report(from_date= fromdate, 
                                       to_date=todate, send_email= True,
                                    #    exceptions= None,
                                       )

    main_db.volume_discount_report(dates= [todate], send_email=True)


if __name__ == "__main__":
  
    schedule.every().day.at("21:00").do(busy_sales)

    schedule.every().day.at("03:15").do(export_import_outstanding_tallydata)
    
    schedule.every().day.at("00:05").do(busy_material_masters)

    schedule.every().day.at("05:15").do(tally_to_sql)

    schedule.every().day.at("09:46").do(reports)
    
    while True:
        schedule.run_pending()
        time.sleep(1)    

    # current_date = datetime.today().strftime("%d-%b-%Y")
    # main_db.import_tally_data(date= current_date)

    # companies = sorted(list(balance_comp_codes.keys()))
    # main_tally.export_tally_accounts(company= companies)
    # main_db.import_tally_data(date= current_date)
    # import pandas as pd
    # f = r"D:\automated_tally_downloads\10007\accounts\10007_accounts_01-Apr-2024.xlsx"
    # main_db.one(path= f, commit= False)
    # start_date = datetime.date(year= 2024, month= 5, day=1)
    # end_date = datetime.today().date() - timedelta(days=1)
    # exe = ['KAYBEE/001 A']
    # main_db.cash_discount_report(dates= ['2024-06-01', 
    #                                      '2024-06-02', '2024-06-03', '2024-06-04', '2024-06-05',
    #                                      ], send_email= False)

    # todays_date = datetime.today().strftime("%d-%b-%Y")
    # # todays_date = "Apr-17-May-24"
    # from_date = (datetime.today() - timedelta(days=2)).strftime("%d-%m-%Y")
    # # from_date = "1-4-2017"
    # to_date = (datetime.today().date() - timedelta(days=1)).strftime("%d-%m-%Y")
    # # to_date = "15-5-2024"

    
    
