import pyautogui as pg
import time
from busy import busy_utils
from dotenv import load_dotenv
from datetime import datetime, timedelta



load_dotenv()



pg.PAUSE = 1.0


def select_transaction():
    transaction = pg.moveTo(250, 30, duration=0.3) 
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/trans_check.png', confidence= 0.9)
        except Exception:
            pg.click(transaction)
            time.sleep(1) 
            pass
    busy_utils.find_img('busy/images/trans_check.png', conf= 0.9)
    time.sleep(2)
    

def select_masters():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/busy_administration.png', confidence= 0.9)
            pg.click(location)    
        except Exception:
            try:
                location = pg.locateOnScreen('busy/images/busy_sel_administration.png', confidence= 0.9)
            except Exception:
                pass


def select_accounts():
    try:
        pg.locateOnScreen('busy/images/busy_sel_masters.png', confidence=0.9)
        pg.press('enter')   #enter to go in open masters
        time.sleep(0.4) 
        pg.press("enter")   #enter to go in accounts
        time.sleep(0.4)
        pg.press("down")   #down for list
        time.sleep(0.4)
        pg.press("enter")  #enter to select list 
        time.sleep(0.4)
    except:
        master = pg.locateOnScreen('busy/images/busy_masters.png', confidence=0.9)
        pg.click(master)
        time.sleep(0.4)
        pg.press("down") #down for accounts
        time.sleep(0.4)
        pg.press("down")   #down for list
        time.sleep(0.4)
        pg.press("enter")  #enter to select list 
        time.sleep(0.4)
        
    busy_utils.find_img('busy/images/standard_format.png')
    pg.click()
    pg.click()
    time.sleep(5)

    pg.typewrite('new')
    pg.press('enter')

    pg.typewrite("a")
    pg.press("backspace")               #select branch
    time.sleep(0.3)
    pg.press('enter')

    pg.press('y')
    pg.press('enter')

    pg.press('enter')



def select_items():
    try:
        pg.locateOnScreen('busy/images/busy_sel_masters.png', confidence=0.9)
        pg.press('enter')   #enter to go in open masters
        time.sleep(0.4)    
    except:
        master = pg.locateOnScreen('busy/images/busy_masters.png', confidence=0.9)
        pg.click(master)
        time.sleep(0.4)
    try:
        item = pg.locateOnScreen('busy/images/busy_item.png', confidence=0.9)
        pg.click(item, duration=0.4)
    except:
        item_sel = pg.locateOnScreen('busy/images/busy_sel_item.png', confidence=0.9)
        pg.doubleClick(item_sel, duration=0.4)
    pg.press('down')
    pg.press('down')
    pg.press('enter')

    busy_utils.find_img('busy/images/standard_format.png')
    pg.click()
    pg.click()
    time.sleep(5)

    pg.typewrite('standard')
    pg.press('enter')

    pg.typewrite("a")
    pg.press("backspace")               #select branch
    time.sleep(0.3)
    pg.press('enter')

    pg.press('n')
    pg.press('enter')

    pg.press('y')
    pg.press('enter')

    pg.press('f2')



def select_sales_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/busy_sales.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass
            

def select_mitp_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images//mitp.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass


def select_salesreturn_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/salesreturn.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass


def select_purchase_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/busy_purchase.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass


def select_purchase_return_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/busy_purchase_return.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass



def select_mrfp_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/mrfp.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass

    

def select_salesorder_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/salesorder.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass
  

def select_stock_transfer_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/stock_transfer.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass


def select_stock_journal_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/stock_journal.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass


def select_production_list():
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/production.png', confidence=0.9)
            pg.click(location)
            pg.press('down')
            pg.press('down')
            pg.press('enter')
        except Exception:
            time.sleep(2)
            pass



def list_format(report_type, start_date, end_date):
    busy_utils.find_img('busy/images/busy_list.png')
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



def purchase_list_format(start_date, end_date):
    busy_utils.find_img('busy/images/list_image.png')
    time.sleep(1)
    
    #format name
    pg.typewrite('new', interval=0.2)    
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

    pg.typewrite('n')           #show batch details 
    pg.press('enter')

    pg.typewrite('y')           #show party TIN/GSTIN no 
    pg.press('enter')

    pg.typewrite('n')           #show report notes in column 
    pg.press('enter')

    pg.press('enter')  



def stock_list_format(report_type, start_date, end_date):
    busy_utils.find_img('busy/images/list_image.png')
    time.sleep(1)
    
    pg.typewrite('new')    
    pg.press('enter')

    pg.typewrite("a")
    pg.press("backspace")               #select branch
    time.sleep(0.3)
    pg.press('enter')

    pg.typewrite("a")
    pg.press("backspace")              #voucher series
    time.sleep(0.3)
    pg.press('enter')

    pg.typewrite(start_date)          #start date
    pg.press('enter')

    pg.typewrite(end_date)            #end date
    pg.press('enter')

    pg.typewrite('both')            #report to be shown in
    pg.press('enter')

    pg.typewrite('name')           #item to be shown in 
    pg.press('enter')
    
    if report_type != 'stock_transfer':
        pg.typewrite('y')           #show material centre namne 
        pg.press('enter')
    else:
        pass
    
    pg.typewrite('y')           #show value of items 
    pg.press('enter')

    pg.typewrite('n')           #show batch details 
    pg.press('enter')

    pg.typewrite('n')           #show report notes in column 
    pg.press('enter')

    pg.press('enter')





def transaction_report_selection(report):
    time.sleep(5)
    select_transaction()
    report()
    


# def main_items():
#     pg.hotkey('alt', 'tab')
#     select_masters()
#     select_items()
#     busy_utils.export_format(report_type= "items", 
#                                      company= 'comp0005', 
#                                      filename=f"comp_master_accounts_curr_date")
            
#     busy_utils.return_to_busy_home(esc=6)
#     time.sleep(5)









