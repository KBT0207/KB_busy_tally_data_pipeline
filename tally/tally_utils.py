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
    find_img('tally/images/tally_desktop.png', conf=0.9)
    pg.doubleClick()    
    find_img('tally/images/tally_start.png')
    pg.press('down', presses=3, interval=0.5)
    pg.press('enter')
    pg.typewrite(r"\\honas\SERVER DATA\IT & MIS\Jovo Tally\Data\Data", interval=0.3)
    pg.press('enter')



def select_company(company_code):
    find_img('tally/images/tally_start.png', conf=0.95)
    time.sleep(1)
    pg.typewrite(str(company_code), interval=0.4)
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
    time.sleep(3)
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



def export_data(path, filename):
    find_img('tally/images/report_list.png')
    time.sleep(2)
    pg.hotkey('ctrl', 'e')
    time.sleep(1.5)
    pg.press('c')
    time.sleep(2)
    pg.press('down')
    time.sleep(1)
    find_img('tally/images/export_settings.png', conf=0.95 )
    time.sleep(1)
    pg.click()
    time.sleep(0.5)
    pg.press('down')
    pg.press('enter')
    pg.typewrite('excel', interval=0.3)
    pg.press('enter')

    find_img("tally/images/folder_path.png")
    pg.click()
    pg.press('enter')
    pg.typewrite(path, interval=0.2)
    pg.press('enter', presses=2, interval=0.4)
    
    pg.press('down')
    pg.press('enter')
    pg.typewrite(filename, interval=0.2)
    pg.press('enter')

    pg.hotkey("ctrl", "a")  #uncomment later very important
    time.sleep(1)
    pg.press('e')

    find_img(img='tally/images/report_list.png')



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
    time.sleep(1)
    select_report(report_type= report)
    time.sleep(1)
    change_period(from_date= from_date , to_date= to_date) 
    time.sleep(1)
    export_data(path= path, filename= filename)
    time.sleep(1.5)
    back_to_tally_home(times=esc)
