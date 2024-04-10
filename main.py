import time
from busy import rep1
from utils import email
import schedule


if __name__ == "__main__":
    #rep1.report_selection()
    #time.sleep(2)
    rep1.test_1()

    email.schedule_email_task()
    while True:
        # Run pending scheduled tasks
        schedule.run_pending()
        time.sleep(1)
    
    

 

