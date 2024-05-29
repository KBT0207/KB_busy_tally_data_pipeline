import time
import schedule
from datetime import datetime, timedelta
from database import main_db
from busy import main_busy
from tally import main_tally
from utils.common_utils import tally_comp_codes



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



def reports():
    fromdate = datetime.today().date().replace(day=1).strftime('%Y-%m-%d')
    todate = (datetime.today().date() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    excluded_invoices = ['KBAKNU/2425/3']
    main_db.dealer_price_validation_report(from_date= fromdate, 
                                           to_date= todate, send_email= True, 
                                           exceptions= excluded_invoices,
                                           )

    


if __name__ == "__main__":
    # main_db.delete_busy_sales()
    # main_db.import_busy_sales()
    # main_db.import_tally_accounts()
    
    # main_db.delete_one(commit=True)
    # main_db.import_tally_data()

    schedule.every().day.at("21:00").do(busy_sales)

    schedule.every().day.at("00:05").do(busy_material_masters)

    schedule.every().day.at("04:30").do(tally_to_sql)

    schedule.every().day.at("10:00").do(reports)
    
    while True:
        schedule.run_pending()
        time.sleep(1)    
