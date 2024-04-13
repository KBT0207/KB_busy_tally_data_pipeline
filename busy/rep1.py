import pyautogui as pg
import time
from utils import busy_utils
import logging
import os
from logging_config import LOGGING_CONFIG 
from dotenv import load_dotenv
from datetime import datetime, timedelta


load_dotenv()

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("rep1")

pg.PAUSE = 0.8



def select_transaction():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/busy_transactions.png', confidence= 0.9)
            pg.click(location)    
        except Exception:
            try:
                pg.locateOnScreen('busy/images/busy_sel_transactions.png', confidence= 0.9)
            except Exception:
                pass



def select_sales_list():
    try:
        sales = pg.locateOnScreen('busy/images/busy_sales.PNG', confidence=0.95)
        pg.moveTo(sales)
        pg.click() 
        pg.press('l')
    except:
        try:
            pg.locateOnScreen('busy/images/busy_sel_sales.png', confidence=0.95)
            pg.press('enter')
            time.sleep(0.2)
            pg.press('l')
        except:
            try:
                down = pg.locateOnScreen('busy/images/busy_down_sales.png',confidence=0.95)
                pg.doubleClick(down)
                time.sleep(0.4)
                pg.press("l")
            except:
                pass



def sales_list_format(standard_format, start_date, end_date):
    busy_utils.find_img('busy/images/busy_list.png')
    pg.typewrite(standard_format)     #format name
    pg.press('enter')

    pg.typewrite("a")
    pg.press("backspace")               #select branch
    time.sleep(0.3)
    pg.press('enter')

    pg.typewrite("a")
    pg.press("backspace")              #voucher series
    time.sleep(0.3)
    pg.press('enter')

    pg.typewrite("all")               #salesman range
    time.sleep(0.3)
    pg.press('enter')

    pg.typewrite(start_date)          #start date
    pg.press('enter')

    pg.typewrite(end_date)            #end date
    pg.press('enter')

    pg.typewrite('name')             #account to be shown
    pg.press('enter')

    pg.typewrite('both')            #report to be shown in
    pg.press('enter')

    pg.typewrite('name')           #item to be shown in 
    pg.press('enter')
    
    pg.typewrite('y')           #show material centre namne 
    pg.press('enter')

    pg.typewrite('y')           #show value of items 
    pg.press('enter')

    pg.typewrite('n')           #show batch items 
    pg.press('enter')

    pg.typewrite('y')           #show party TIN/GSTIN no 
    pg.press('enter')

    pg.typewrite('n')           #show report notes in column 
    pg.press('enter')

    pg.press('enter')




def transaction_sales_report_selection():
    time.sleep(4)
    select_transaction()
    select_sales_list()
    


def sales_report():
    busy_utils.preparing_envs(rdc_password= os.getenv('BUSY_RDC_PASSWORD'),
                              company= 'COMP0005', 
                              username= os.getenv('BUSY_USERNAME'),
                              password= os.getenv('BUSY_PASSWORD'))
    transaction_sales_report_selection()

    endate = datetime.today()
    startdate = endate - timedelta(days=0)

    endate_str = endate.strftime("%d-%m-%Y")
    startdate_str = startdate.strftime("%d-%m-%Y")
    sales_list_format(standard_format='new', 
                      start_date= startdate_str, 
                      end_date= endate_str)
    
    busy_utils.export_format(report_type = 'sales', company = 'comp0005', 
                             filename= datetime.today().strftime("%d-%b-%Y"))
    busy_utils.return_to_busy_home(esc=3)
    busy_utils.close_rdc()



def local_sales_report():
    busy_utils.open_busy()
    busy_utils.company_selection(comp_code='comp0005')
    busy_utils.busy_login(username= os.getenv('BUSY_USERNAME'),
                          password= os.getenv('BUSY_PASSWORD'))
    transaction_sales_report_selection()

    endate = datetime.today()
    startdate = endate - timedelta(days=1)

    endate_str = endate.strftime("%d-%m-%Y")
    startdate_str = startdate.strftime("%d-%m-%Y")
    sales_list_format(standard_format='new', 
                      start_date= startdate_str, 
                      end_date= endate_str)
    
    busy_utils.export_format(report_type = 'sales', company = 'comp0005', 
                             filename= datetime.today().strftime("%d-%b-%Y"))
    busy_utils.return_to_busy_home(esc=3)
  

