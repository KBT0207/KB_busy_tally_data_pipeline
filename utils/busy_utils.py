import pyautogui as pg
import time
from typing import Union
from utils import common_utils
from dotenv import load_dotenv

load_dotenv()


def find_img(img, conf: Union[float, int] = 0.9 , **args ) -> None:
    """Function will continue to look for the image and will not continue
       until it finds the image.

    Args:
        img (float, int): The image you want to find.
        conf (float, optional): Confidence parameter same as found in location methods
                                in Pyautogui. Defaults to 0.9.
    """
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen(img, confidence= conf)
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
        pg.typewrite("192.168.0.233:7217")
        pg.press("enter")
        time.sleep(2)
        pg.typewrite(password)
        time.sleep(2)
        ok = pg.locateCenterOnScreen(image="busy/images/password_ok.png", confidence= 0.85)
        pg.click(ok)
        time.sleep(1)
        pg.hotkey("win", 'up')
    else:
        rdc = pg.locateCenterOnScreen('busy/images/rdc.png', confidence=0.9)
        pg.click(rdc)
        pg.hotkey("win", 'up')



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
    time.sleep(2)
    pg.hotkey("win", "d")
    try:
        busy = pg.locateCenterOnScreen(image="busy/images/busy_desktop_icon.png",
                                       confidence=0.8)
        pg.doubleClick(busy, duration=0.3)
    except pg.ImageNotFoundException as e:
        print("Busy Icon not found!", e)          # [logging required here]
    finally:
        time.sleep(3)
    location = None
    while location == None:
        try:
            location = pg.locateOnScreen('busy/images/open_company.png', confidence= 0.9)
        except pg.ImageNotFoundException as e:
            find_img('busy/images/busy_startup_prompt.png')
            pg.click()
    pg.moveTo(location,duration=0.1)




def company_selection(comp_code):
    pg.press("enter")
    time.sleep(0.5)
    pg.typewrite(comp_code)
    pg.press('tab')
    pg.press("enter")
    time.sleep(1)





def busy_login(username, password):    #implement logging and end script if incorrect user/pass [logging required here]
    pg.write(username, interval= 0.3)
    time.sleep(0.4)
    pg.press("enter")
    time.sleep(1)
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
        pg.write(password)
        time.sleep(1)
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
            time.sleep(3)
        



