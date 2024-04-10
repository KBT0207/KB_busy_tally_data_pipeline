import pyautogui as pg
import time
from utils import busy_utils
import logging
import os
from logging_config import LOGGING_CONFIG 

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("rep1")

pg.PAUSE = 0.8


def preparing_envs():
    busy_utils.start_rdc(password= os.getenv('BUSY_RDC_PASSWORD'))
    time.sleep(2)
    busy_utils.open_busy()
    busy_utils.company_selection(comp_code= 'COMP0005')
    busy_utils.busy_login(username= os.getenv('BUSY_USERNAME') , password= os.getenv('BUSY_PASSWORD'))
    


def report_selection():
    #delete this
    pg.hotkey('alt', 'tab')
    #remember
    busy_utils.find_img("busy/images/busy_top.png")
    time.sleep(0.5)
    pg.move(xOffset=10, yOffset= 25, duration=0.2)
    pg.click()
    pg.move(xOffset=0, yOffset= 115, duration=0.5)
    pg.click()
    pg.move(xOffset=20, yOffset= 40, duration=0.3)
    pg.click()



def test_1():
    pg.hotkey("win", "d")
    try:
        new = pg.locateOnScreen('busy/images/delete_new_folder.png', confidence=0.9)
        pg.click(new, duration=0.5)
        logger.info("Image Found")
    except pg.ImageNotFoundException as e:
        logger.error("Image not Abort asap")
    finally:
        print("Testing Logs")