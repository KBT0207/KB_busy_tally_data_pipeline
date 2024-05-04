import pyautogui as pg
import time
from busy import busy_utils
from dotenv import load_dotenv
from datetime import datetime, timedelta



load_dotenv()



pg.PAUSE = 1.0


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



def transaction_report_selection(report):
    time.sleep(10)
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









