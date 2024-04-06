import pyautogui as pg
import time
from utils import busy_utils
import logging
import os

pg.PAUSE = 0.8



def preparing_envs():
    busy_utils.start_rdc(password= os.getenv('BUSY_RDC_PASSWORD'))
    time.sleep(2)
    busy_utils.open_busy()
    busy_utils.company_selection(comp_code= 'COMP0007')
    busy_utils.busy_login(username= os.getenv('BUSY_USERNAME') ,
                          password=os.getenv('BUSY_PASSWORD'))
    

    





