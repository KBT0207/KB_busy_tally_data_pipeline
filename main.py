import time
import schedule
from utils.email import send_daily_logs
from database import main_db
from busy import main_busy
from tally import main_tally
from database.tally_data_processor import TallyDataProcessor
from database.db_crud import DatabaseCrud
from database.busy_data_processor import BusyDataProcessor
from utils.common_utils import tally_comp_codes




def data_busy_to_sql_async():

    main_busy.exporting_and_emailing()
    time.sleep(2)
    main_db.delete_busy_data()
    
    main_db.import_busy_data()


if __name__ == "__main__":

    companies = list(tally_comp_codes.keys())
    
    #main_tally.exporting_data(company=companies)
    main_db.delete_tally_data()
    #main_db.import_tally_data()
    
    # main_busy.exporting_and_emailing()
    # main_db.test()
    # schedule.every().day.at("20:30").do(data_busy_to_sql_async)
    # schedule.every().day.at("23:20").do(send_daily_logs)
    
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    
