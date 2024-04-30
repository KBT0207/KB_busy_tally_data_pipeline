import time
import schedule
from utils.email import send_daily_logs
from database import main_db
from busy import main_busy



def data_busy_to_sql_async():
    main_busy.exporting_and_emailing()
    time.sleep(5)
    main_db.delete_then_import_to_sql()

if __name__ == "__main__":
    schedule.every().day.at("21:00").do(data_busy_to_sql_async)
    schedule.every().day.at("23:10").do(send_daily_logs)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

