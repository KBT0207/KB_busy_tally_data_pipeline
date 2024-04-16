import pyautogui as pg
import time
from utils import busy_utils
import logging
import os
from logging_config import logger
from dotenv import load_dotenv
from datetime import datetime, timedelta
from utils import email


load_dotenv()




pg.PAUSE = 0.8


def select_transaction():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/busy_transactions.png', confidence= 0.9)
            pg.click(location)    
        except Exception:
            try:
                location = pg.locateOnScreen('busy/images/busy_sel_transactions.png', confidence= 0.9)
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



def select_salesreturn_list():
    try:
        sales = pg.locateOnScreen('busy/images/salesreturn.PNG')
        pg.moveTo(sales)
        pg.click() 
        pg.press('l')
        print("not down")
    except:
        try:
            pg.locateOnScreen('busy/images/sel_salesreturn.png', confidence=0.95)
            pg.press('enter')
            time.sleep(0.2)
            pg.press('l')
            pg.press("enter")
            print('selected not down')
        except:
            try:
                down = pg.locateOnScreen('busy/images/down_salesreturn.png',confidence=0.95)
                pg.click(down)
                pg.click()
                time.sleep(0.4)
                pg.press("l")
                print("down")
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




def transaction_report_selection(report):
    time.sleep(10)
    select_transaction()
    rep = report()
    


def sales_report():
    busy_utils.preparing_envs(rdc_password= os.getenv('BUSY_RDC_PASSWORD'),
                              company= 'COMP0005', 
                              username= os.getenv('BUSY_USERNAME'),
                              password= os.getenv('BUSY_PASSWORD'))
    transaction_report_selection()

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
    
    try:
        busy_utils.busy_login(username= os.getenv('BUSY_USERNAME'),
                          password= os.getenv('BUSY_PASSWORD'))
        logger.info("Logged into Busy successfully...")
    except Exception as e:
        logger.critical(f"Logging into Busy Failed! : {e}")
    
    transaction_report_selection(report= select_sales_list)

    endate = datetime.today()
    startdate = endate - timedelta(days=2)

    endate_str = endate.strftime("%d-%m-%Y")
    startdate_str = startdate.strftime("%d-%m-%Y")
    
    try:
        sales_list_format(standard_format='new', 
                        start_date= startdate_str, 
                        end_date= endate_str)
        logger.info("Generated data to export successfully...")
    except Exception as e:
        logger.critical(f"Data Generation Failed! : {e}")

    try:
        rep_type = "sales"
        comp_code = "comp0005"
        busy_utils.export_format(report_type = rep_type, company = comp_code, 
                                filename= datetime.today().strftime("%d-%b-%Y"))
        logger.info("Exported data successfully...")
    except Exception as e:
        logger.critical(f"Exporting Data Failed! : {e}")

    try:    
        busy_utils.return_to_busy_home(esc=3)
        logger.info("Report Generated Successfully and Quit Busy...")
    except Exception as e:
        logger.critical(f"Failed to Quit Busy! : {e}")

    time.sleep(5)
    try:
        today_date = datetime.today().strftime("%d-%b-%Y")
        receivers = ['shivprasad@kaybeebio.com', 'danish@kaybeeexports.com']
        subj = f"{comp_code} {rep_type} data of {endate_str}"
        attachment_path = rf"D:\automated_busy_downloads\{comp_code}\{rep_type}\{today_date}.xlsx"
        email.email_send(reciever=receivers, cc = "s.gaurav@kaybeeexports.com", 
                         subject= subj, 
                         contents= f"Kindly find the attached {rep_type} data of {comp_code} from {startdate_str} to {endate_str}", 
                         attachemnts= attachment_path)
        logger.info("Attachment emailed successfully... ")
    except Exception as e:
        logger.critical(f"Failed to email the attachment! : {e}")




