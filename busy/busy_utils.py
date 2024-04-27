import pyautogui as pg
import time
from datetime import datetime
from typing import Union
from utils import common_utils
from dotenv import load_dotenv
import logging
from logging_config import logger

load_dotenv('.env')


def find_img(img:str, timeout:int = 10, conf: Union[float, int] = 0.9, gs:bool=False ) -> None:
    """Function will continue to look for the image for the time given as timeout parameter seconds (default is 10 secs).

    Args:
        img (str): The image you want to find.
        timeout(int): Amount of seconds it should take to find the image the image 
                    if None is given then it waits indefinetly. Defaults to 10 seconds
        conf (float, optional): Confidence parameter same as found in             location methods in Pyautogui. Defaults to 0.9.
        gs(bool, optional): Grayscale property applied to image or not. Defaults to False 
    """
    location = None
    start_time = time.time()
    while (location == None) and (timeout is None or (time.time() - start_time) < timeout):
        try:
            location = pg.locateOnScreen(img, confidence= conf, grayscale=gs)
        except Exception:
            continue
    pg.moveTo(location,duration=0.1)




def start_rdc(password:str) -> None:            #modify so that it takes password as parameter
    """This starts Remote Desktop Connection (RDC) and maximizes its window 
    if the RDC is not running already.

    Args:
        password (str): Password for the RDC.
    """
    if not common_utils.is_process_running('mstsc.exe'):
        pg.hotkey("win", "r")
        pg.typewrite("mstsc")
        pg.press("enter")
        find_img('busy/images/busy_connect.png')
        pg.typewrite("192.168.0.233:7217")
        pg.press("enter")
        find_img("busy/images/password_ok.png")
        time.sleep(0.3)
        pg.typewrite(password)
        pg.click()
        find_img('busy/images/rdc_desktop.png')
        time.sleep(0.5)
        pg.hotkey("win", 'up')
        time.sleep(0.3)
        pg.hotkey("win", "d")
    else:
        rdc = pg.locateCenterOnScreen('busy/images/rdc.png', confidence=0.9)
        pg.click(rdc)
        pg.hotkey("win", 'up')
        time.sleep(0.3)
        pg.hotkey('win', 'd')



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



def open_busy() -> None:
    pg.hotkey('win', 'd')
    time.sleep(0.5)
    try:
        busy = pg.locateCenterOnScreen(image="busy/images/busy_desktop_icon.png",
                                       confidence=0.8)
        pg.doubleClick(busy, duration=0.3)
    except pg.ImageNotFoundException as e:
        logger.critical(f"Busy Icon not found!: {e}")         
    finally:
        time.sleep(3)
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/open_company.png', confidence= 0.9)
        except pg.ImageNotFoundException as e:
            pg.press('enter', interval=0.4)
            time.sleep(1)
    pg.click(location,duration=0.3)
    logger.info("Busy opened successfully..")




def company_selection(comp_code:str):
    """Selected the company in Busy

    Args:
        comp_code (str): Busy Company Code
    """
    find_img('busy/images/select_company.png', timeout= 200)
    time.sleep(0.5)
    pg.typewrite(comp_code)
    pg.press('tab')
    pg.press("enter")
    




def busy_login(username:str, password:str):    #implement logging and end script if incorrect user/pass [logging required here]
    """Function starts after a company is selected and then logs into it 
    using the provided credentials 
    If either the username of password is found incorrect it closes the Busy and then the RDC
       
    Args:
        username (str): Username for the Busy
        password (str): Password for the Busy
    """
    find_img('busy/images/busy_username.png', timeout= 300)
    pg.write(username, interval= 0.3)
    pg.press("enter")
    time.sleep(0.3)
    try:
        pg.locateCenterOnScreen('busy/images/incorrect_username.png', confidence=0.9)
        time.sleep(0.5)
        pg.press("enter")
        quit = pg.locateCenterOnScreen('busy/images/quit_at_login.png', confidence=0.9)
        pg.click(quit, duration=0.3)

        quit = pg.locateCenterOnScreen('busy/images/quit_at_login.png', confidence=0.9)
        pg.click(quit, duration=0.3)
        pg.press('e')
        pg.press("enter")

        close_rdc()
    except:
        pg.write(password, interval= 0.3)
        time.sleep(0.4)
        pg.press("enter")
        try:
            pg.locateCenterOnScreen('busy/images/incorrect_password.png', confidence=0.9)
            time.sleep(0.5)
            pg.press("enter")
            quit = pg.locateCenterOnScreen('busy/images/quit_at_login.png', confidence=0.9)
            pg.click(quit, duration=0.3)

            quit = pg.locateCenterOnScreen('busy/images/quit_at_login.png', confidence=0.9)
            pg.click(quit, duration=0.3)
            pg.press('e')
            pg.press("enter")
            close_rdc()
        except:
            pg.press("enter")
            find_img('busy/images/busy_loggedin.png', timeout= 25)
            


def export_format(report_type:str, company:str, filename):
    save_location = f"D:\\automated_busy_downloads\{company}\{report_type}\{filename}"
    find_img('busy/images/busy_report_list.png', timeout=3000)
    time.sleep(0.3)
    pg.moveTo(150, 150,duration=0.3)
    time.sleep(1)
    pg.hotkey('alt', 'e')
    
    find_img('busy/images/busy_export_format.png', timeout=600)

    pg.typewrite('micros')           #data format 
    pg.press('enter')

    #save location and file name
    pg.typewrite(save_location, interval=0.1)           
    pg.press('enter')

    pg.typewrite("zero")
    pg.press('enter')
    pg.press('enter')

    pg.typewrite("not req")
    pg.press('enter')    
    pg.press('enter')

    find_img('busy/images/busy_download_prompt.png', timeout= 300)
    time.sleep(0.5)
    pg.click()




def preparing_envs(rdc_password:str , company:str ,username:str, password:str) -> None:
    start_rdc(rdc_password )
    time.sleep(2)
    open_busy()
    company_selection(comp_code= company)
    busy_login(username, password)
           


def change_company():
    find_img('busy/images/busy_home.png', timeout= 60)
    time.sleep(0.5)
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/busy_menu_company.png', confidence= 0.9)
            pg.click(location, duration=0.3)
            pg.press('enter')
        except Exception:
            location = pg.locateOnScreen('busy/images/busy_sel_menu_company.png', confidence= 0.9)
            pg.press('enter')
    time.sleep(0.5)
    


def return_to_busy_home(esc=3):
    time.sleep(0.5)
    for _ in range(1, esc+1):
        pg.press('esc')
        time.sleep(2)
    



