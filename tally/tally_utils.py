import pyautogui as pg
import os
from dotenv import load_dotenv
import time
from busy.busy_utils import start_rdc
from logging_config import logger
from utils import common_utils
from busy.busy_utils import find_img

load_dotenv('.env')



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



def open_tally() -> None:
    time.sleep(0.5)
    find_img("busy/images/tally_desktop.png", timeout=180)
    logger.info("Busy opened successfully..")



def start():
    pg.hotkey("win", "d")
    start_rdc(os.getenv("BUSY_RDC_PASSWORD"))

    #start_rdc


