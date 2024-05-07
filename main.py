import time
import schedule
from utils.email import send_daily_logs
from database import main_db
from busy import main_busy
from tally import main_tally
from utils.common_utils import tally_comp_codes




def tally_to_sql():
    companies = sorted(list(tally_comp_codes.keys()))
    main_tally.exporting_data(company=companies)

    main_db.delete_tally_data()
    main_db.import_tally_data()


def busy_to_sql():

    main_busy.exporting_and_emailing()
    time.sleep(2)
    main_db.delete_busy_data()
    
    main_db.import_busy_data()

def main():
    busy_to_sql()
    tally_to_sql()    



if __name__ == "__main__":
    #main_db.test()
    companies = sorted(list(tally_comp_codes.keys()))

    schedule.every().day.at("20:30").do(busy_to_sql)

    schedule.every().day.at("07:10").do(tally_to_sql)

    schedule.every().day.at("23:55").do(send_daily_logs)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

    
