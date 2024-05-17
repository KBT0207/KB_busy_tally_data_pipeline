import time
import schedule
from database import main_db
from busy import main_busy
from tally import main_tally
from utils.common_utils import tally_comp_codes



def tally_to_sql():
    companies = sorted(list(tally_comp_codes.keys()))
    main_tally.exporting_data(company=companies)
    main_db.delete_tally_data()
    main_db.import_tally_data()


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




if __name__ == "__main__":

    from database.tally_data_processor import TallyDataProcessor 
    path = r"D:\automated_tally_downloads\items\tally_items_17-May-2024.xlsx"
    xl = TallyDataProcessor(path)
    df = xl.clean_and_transform()
    # schedule.every().day.at("21:00").do(busy_sales)

    # schedule.every().day.at("00:05").do(busy_material_masters)

    # schedule.every().day.at("05:00").do(tally_to_sql)
    
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)    
