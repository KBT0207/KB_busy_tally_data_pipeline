import pyautogui as pg
import time
from utils import busy_utils
import logging
import os
from logging_config import logger
from dotenv import load_dotenv
from datetime import datetime, timedelta
from utils import email
import glob


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



def select_mitp_list():
    try:
        sales = pg.locateOnScreen('busy/images/mitp.PNG', confidence=0.99)
        pg.moveTo(sales)
        pg.click() 
        pg.press('down')
        pg.press('down')
        pg.press('enter')
    except:
        try:
            pg.locateOnScreen('busy/images/sel_mitp.png', confidence=0.95)
            pg.press('enter')
            time.sleep(0.2)
            pg.press('l')
            pg.press("enter")
        except:
            try:
                down = pg.locateOnScreen('busy/images/down_mitp.png', confidence=0.95)
                pg.click(down)
                pg.click()
                time.sleep(0.4)
                pg.press("l")
            except:
                pass



def select_salesreturn_list():
    try:
        sales = pg.locateOnScreen('busy/images/salesreturn.PNG', confidence=0.99)
        pg.moveTo(sales)
        pg.click() 
        pg.press('down')
        pg.press('down')
        pg.press('enter')
    except:
        try:
            pg.locateOnScreen('busy/images/sel_salesreturn.png', confidence=0.95)
            pg.press('enter')
            time.sleep(0.2)
            pg.press('l')
            pg.press("enter")
        except:
            try:
                down = pg.locateOnScreen('busy/images/down_salesreturn.png', confidence=0.95)
                pg.click(down)
                pg.click()
                time.sleep(0.4)
                pg.press("l")
            except:
                pass



def select_mrfp_list():
    try:
        sales = pg.locateOnScreen('busy/images/mrfp.PNG', confidence=0.99)
        pg.moveTo(sales)
        pg.click() 
        pg.press('down')
        pg.press('down')
        pg.press('enter')
    except:
        try:
            pg.locateOnScreen('busy/images/sel_mrfp.png', confidence=0.95)
            pg.press('enter')
            time.sleep(0.2)
            pg.press('l')
            pg.press("enter")
        except:
            try:
                down = pg.locateOnScreen('busy/images/down_mrfp.png', confidence=0.95)
                pg.click(down)
                pg.click()
                time.sleep(0.4)
                pg.press("l")
            except:
                pass



def select_salesorder_list():
    try:
        sales = pg.locateOnScreen('busy/images/salesorder.png', confidence=0.99)
        pg.moveTo(sales)
        pg.click() 
        pg.press('down')
        pg.press('down')
        pg.press('enter')
    except:
        try:
            pg.locateOnScreen('busy/images/sel_salesorder.png', confidence=0.95)
            pg.press('enter')
            time.sleep(0.2)
            pg.press('l')
            pg.press("enter")
        except:
            try:
                down = pg.locateOnScreen('busy/images/down_salesorder.png', confidence=0.95)
                pg.click(down)
                pg.click()
                time.sleep(0.4)
                pg.press("l")
            except:
                pass



def list_format(report_type, start_date, end_date):
    busy_utils.find_img('busy/images/busy_list.png', timeout=20)
    time.sleep(1)
    
    #format name
    if report_type == "sales" or report_type == "sales_return":  
        pg.typewrite('new')
    if report_type == "material_received_from_party" or report_type == "material_issued_to_party":
        pg.typewrite('new')
    if report_type == "sales_order":
        pg.typewrite('order value')    
    
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

    if report_type != "sales_order":
        pg.typewrite('n')           #show batch details 
        pg.press('enter')
    else:
        pass

    if report_type == "sales" or report_type == "sales_return":
        pg.typewrite('y')           #show party TIN/GSTIN no 
        pg.press('enter')
    if report_type == "material_received_from_party" or report_type == "material_issued_to_party" or report_type == "sales_order":
        pass

    pg.typewrite('n')           #show report notes in column 
    pg.press('enter')

    pg.press('enter')  



def transaction_report_selection(report):
    time.sleep(15)
    select_transaction()
    report()
    



def local_sales_report():

    companies = ['comp0005', 'comp0010', 'comp0011', 'comp0014', 'comp0015' ]

    transaction_dict = {'trans_list': [select_sales_list, select_salesreturn_list, 
                                       select_mrfp_list, select_mitp_list, 
                                       select_salesorder_list], 
                        'reports': ['sales', 'sales_return', 
                                    "material_received_from_party", "material_issued_to_party", 
                                    "sales_order"] }

    busy_utils.open_busy()
    
    for comp in companies:

        busy_utils.company_selection(comp_code = comp)
        
        try:
            busy_utils.busy_login(username= os.getenv('BUSY_USERNAME'),
                            password= os.getenv('BUSY_PASSWORD'))
            logger.info(f"Logged into Busy of {comp} successfully...")
        except Exception as e:
            logger.critical(f"Logging into Busy of {comp} Failed! : {e}")
        

        for rep_func, report in zip(transaction_dict['trans_list'], transaction_dict['reports']):
            if comp != "comp0005" and report == "sales_order" and rep_func == select_salesorder_list:
                continue
            else:
                transaction_report_selection(report= rep_func)

                endate = datetime.today()
                startdate = endate - timedelta(days=2)

                endate_str = endate.strftime("%d-%m-%Y")
                startdate_str = startdate.strftime("%d-%m-%Y")
                
                try:
                    list_format(report_type= report, 
                                    start_date= startdate_str, 
                                    end_date= endate_str)
                    logger.info(f"Generated data for {comp} and {report} to export successfully...")
                except Exception as e:
                    logger.critical(f"Data Generation for {comp} and {report} Failed! : {e}")

                try:
                    curr_date = datetime.today().strftime("%d-%b-%Y")
                    busy_utils.export_format(report_type = report, company = comp, 
                                            filename= f"{comp}_{report}_{curr_date}")
                    logger.info(f"Exported data for {comp} and {report} successfully...")
                except Exception as e:
                    logger.critical(f"Exporting Data for {comp} and {report} Failed! : {e}")

                try:    
                    busy_utils.return_to_busy_home(esc=3)
                    time.sleep(5)

                    logger.info(f"Report Generated for {comp} and {report} successfully and back to busy home...")
                except Exception as e:
                    logger.critical(f"Failed to go back busy home! : {e}")

        try:    
            busy_utils.change_company()
            time.sleep(5)
            pg.press('enter')
            logger.info(f"Successfully came to company page after {comp} page...")
        except Exception as e:
            logger.critical(f"Failed to go to company page! : {e}")

    time.sleep(2)

    busy_utils.find_img(img='busy/images/quit_at_login.png', timeout= 300)
    pg.click()
    pg.press("e")
    pg.press('enter')
    logger.info("Quit Busy Successfully!")

    today_date = datetime.today().strftime("%d-%b-%Y")
    receivers = ['shivprasad@kaybeebio.com', 'danish@kaybeeexports.com']
    #receivers = ['s.gaurav@kaybeeexports.com']
    reps = [r for r in transaction_dict['reports']]
    body = f"Kindly find the attached [{', '.join(reps)} data of {companies} from {startdate_str} to {endate_str}"
    attachment_path = glob.glob("D:\\automated_busy_downloads\\" + f"**\\*{today_date}.xlsx", recursive=True)

    subj_material = f"KB Companies ['MITP & MRFP'] data of {endate_str}"
    attachment_path_material = []
    for file in attachment_path:
        if 'material' in file:
            attachment_path_material.append(file) 
    if len(attachment_path_material) != 0:
        try:
            email.email_send(reciever=receivers, cc = "s.gaurav@kaybeeexports.com", 
                            subject= subj_material, 
                            contents= body, 
                            attachemnts= attachment_path_material)
            logger.info("Attachments (MITP & MRFP) emailed successfully... ")
        except Exception as e:
            logger.critical(f"Failed to email the attachment for (MITP & MRFP)! : {e}")
    else:
        logger.critical("No data for (MITP & MRFP) exported today")

    subj_sales = f"KB Companies ['Sales, Sales Voucher and Sales Order'] data of {endate_str}"
    attachment_path_sales = []
    for file in attachment_path:
        if 'sale' in file:
            attachment_path_sales.append(file) 
    if len(attachment_path_sales) != 0:
        try:
            email.email_send(reciever=receivers, cc = "s.gaurav@kaybeeexports.com", 
                            subject= subj_sales, 
                            contents= body, 
                            attachemnts= attachment_path_sales)
            logger.info("Attachments (All Sales) emailed successfully... ")
        except Exception as e:
            logger.critical(f"Failed to email the attachment for (All Sales)! : {e}")
    else:
        logger.critical("No data for (All Sales) exported today")



#def test():
#     try:
#         1/1
#         logger.info("Testing_Info")
#         print('test..')
#     except:
#         logger.critical("Testing_critical")







