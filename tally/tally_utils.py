import pyautogui as pg
import os
from dotenv import load_dotenv
import time
from busy.busy_utils import start_rdc
from logging_config import logger
from utils import common_utils
from busy.busy_utils import find_img

load_dotenv('.env')

pg.FAILSAFE = True
pg.PAUSE = 1


def close_rdc() -> None:
    """Closes the RDC if its running.
    """
    if not common_utils.is_process_running('mstsc.exe'):
        print("RDC alrady closed!")
    else:
        pg.press("win")
        power = pg.locateCenterOnScreen('busy/images/rdc_power_button.png')
        pg.click(power)
        find_img('busy/images/disconnect.png')
        pg.click()
        time.sleep(2)



def start_tally() -> None:
    find_img('tally/images/tally_desktop.png')
    pg.doubleClick()    
    find_img('tally/images/tally_start.png')
    pg.press('down', presses=3, interval=0.5)
    pg.press('enter')
    pg.typewrite(r"\\honas\SERVER DATA\IT & MIS\Jovo Tally\Data")
    pg.press('enter')



def select_company(company_code):
    find_img('tally/images/tally_start.png')
    pg.typewrite(str(company_code), interval=0.2)
    pg.press("enter")
    find_img('tally/images/tally_username.png')
    pg.typewrite(os.getenv('TALLY_USERNAME'), interval=0.2)
    pg.press('enter')
    pg.typewrite(os.getenv('TALLY_PASSWORD'), interval=0.2)
    pg.press('enter')
    


def select_report(report_type):
    find_img('tally/images/tally_gateway.png')
    pg.press("d")
    find_img('tally/images/display_reports.png')
    pg.press('a')
    time.sleep(5)
    pg.press(report_type)
    find_img('tally/images/report_particulars.png')
    pg.press('enter')    
    



def change_period(from_date, to_date):
    find_img('tally/images/report_list.png')
    time.sleep(2)
    pg.hotkey("alt", "f2")
    pg.typewrite(from_date, interval=0.2)
    pg.press('enter')
    pg.typewrite(to_date, interval=0.2)
    pg.press('enter')
    

# def export_list_configuration(value):
#     pg.press('enter')
#     pg.typewrite(value)
#     pg.press('enter')


def export_list_configuration(img):
    time.sleep(0.3)
    try:
        pg.locateOnScreen(img, confidence=0.9)
    except:
        pg.press('enter')       



def export_sales(path, filename):
    find_img('tally/images/report_list.png')
    time.sleep(2)
    pg.hotkey('ctrl', 'e')
    time.sleep(0.3)
    pg.press('c')
    
    find_img('tally/images/file_format.png')
    pg.click()
    time.sleep(0.4)
    pg.press('enter')

    pg.typewrite('excel', interval=0.2)
    pg.press('enter')

    report = pg.locateOnScreen('tally/images/report_details.png', confidence=0.9)
    pg.click(report, duration=0.4)
    pg.press('down')

    pg.press('enter')           #Report Type
    pg.typewrite('vouchers')
    pg.press('enter')   
    pg.press('down')

    export_list_configuration(img="tally/images/export_narrations.png")    #Narrations
    pg.press('down')

    export_list_configuration(img="tally/images/show_vouchers.png")    #vouchers
    pg.press('down')

    export_list_configuration(img="tally/images/format_report.png")    #report format
    pg.press('down', presses=6, interval= 0.3)

    export_list_configuration(img="tally/images/gross_profits.png")    #gross profit estimates
    pg.press('down')

    export_list_configuration(img="tally/images/entered_by.png")    #entered by
    pg.press('down')

    export_list_configuration(img="tally/images/display_name.png")    #display name
    pg.press('down', presses=3, interval=0.3)

    export_list_configuration(img="tally/images/show_companyname.png")    #display name
    pg.press('down')

    export_list_configuration(img="tally/images/company_address.png")    #display name
    pg.press('down', presses=7, interval=0.3)

    pg.press('enter')
    pg.typewrite(path)
    pg.press('enter', presses=2, interval=0.4)
    
    pg.press('down')
    pg.press('enter')
    pg.typewrite(filename)
    pg.press('enter')

    pg.hotkey("ctrl", "a")  #uncomment later very important
    time.sleep(0.3)
    pg.press('e')

    find_img(img='tally/images/report_list.png')



def export_purchase(path, filename):
    find_img('tally/images/report_list.png')
    time.sleep(2)
    pg.hotkey('ctrl', 'e')
    time.sleep(0.3)
    pg.press('c')
    
    find_img('tally/images/file_format.png')
    pg.click()
    time.sleep(0.4)
    pg.press('enter')
    pg.typewrite('excel', interval=0.2)
    pg.press('enter')

    report = pg.locateOnScreen('tally/images/report_details.png', confidence=0.9)
    pg.click(report, duration=0.4)
    pg.press('down')

    pg.press('enter')           #Report Type
    pg.typewrite('vouchers')
    pg.press('enter')   
    pg.press('down')

    export_list_configuration(img="tally/images/export_narrations.png")    #Narrations
    pg.press('down')

    export_list_configuration(img="tally/images/show_vouchers.png")    #vouchers
    pg.press('down')

    export_list_configuration(img="tally/images/format_report.png")    #report format
    pg.press('down', presses=6, interval= 0.3)

    export_list_configuration(img="tally/images/entered_by.png")    #entered by
    pg.press('down')

    export_list_configuration(img="tally/images/display_name.png")    #display name
    pg.press('down', presses=3, interval=0.3)

    export_list_configuration(img="tally/images/show_companyname.png")    #display name
    pg.press('down')

    export_list_configuration(img="tally/images/company_address.png")    #display name
    pg.press('down', presses=7, interval=0.3)

    pg.press('enter')
    pg.typewrite(path)
    pg.press('enter', presses=2, interval=0.4)
    
    pg.press('down')
    pg.press('enter')
    pg.typewrite(filename)
    pg.press('enter')

    pg.hotkey("ctrl", "a")  #uncomment later very important
    time.sleep(0.3)
    pg.press('e')

    find_img(img='tally/images/report_list.png')



def export_data(report, path, filename):
    if report == "s":
        export_sales(path=path, filename= filename)
    if report == "p" or report == "e" or report == "d":
        export_purchase(path=path, filename= filename)

        


def back_to_tally_home(times):
    for _ in range(1, times+1):
        pg.press('esc')
        time.sleep(2)



def change_company():
    find_img('tally/images/tally_gateway.png')
    time.sleep(0.5)
    pg.hotkey('alt', 'f1')
    time.sleep(1)
    pg.press('y')
    time.sleep(1)
    pg.press('enter')



def exporting_reports(report:str, from_date:str, to_date:str,  path:str, filename:str, esc:int):
    select_report(report_type= report)
    change_period(from_date= from_date , to_date= to_date) 
    export_data(report=report, path= path, filename= filename)
    back_to_tally_home(times=esc)
