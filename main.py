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
    
    # sheets_to_import = ["Nov"]
    # main_db.importing()
    # main_db.validation()       

    # from database.sql_connector import db_connection
    main_db.test()
    # schedule.every().day.at("21:00").do(busy_sales)

    # schedule.every().day.at("01:00").do(busy_material_masters)

    # schedule.every().day.at("07:03").do(tally_to_sql)
    

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)    
