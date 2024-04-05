import pyautogui as pg
import time
from utils import utils
import logging

pg.PAUSE = 0.8


def find_img(img, conf=0.9, *args ):
    location = None
    while (location == None):
        try:
            location = pg.locateOnScreen(img, confidence= conf)
        except Exception:
            continue
    pg.moveTo(location,duration=0.1)



def start_rdc():
    if not utils.is_process_running('mstsc.exe'):
        pg.hotkey("win", "r")
        pg.typewrite("mstsc")
        pg.press("enter")
        pg.typewrite("192.168.0.233:7217")
        pg.press("enter")
        time.sleep(2)
        pg.typewrite("GA@ur0107$")
        time.sleep(2)
        ok = pg.locateCenterOnScreen(image="busy/images/password_ok.png", confidence= 0.85)
        pg.click(ok)
        time.sleep(1)
        pg.hotkey("win", 'up')
    else:
        rdc = pg.locateCenterOnScreen('busy/images/rdc.png', confidence=0.9)
        pg.click(rdc)
        pg.hotkey("win", 'up')



def close_rdc():
    if not utils.is_process_running('mstsc.exe'):
        print("RDC alrady closed!")
    else:
        pg.press("win")
        power = pg.locateCenterOnScreen('busy/images/rdc_power_button.png')
        pg.click(power)
        pg.press('down')
        pg.press("enter")
        time.sleep(2)



def open_busy():          #implement try error for this method
    time.sleep(2)
    pg.hotkey("win", "d")
    busy = pg.locateCenterOnScreen(image="busy/images/busy_desktop_icon.png",confidence=0.8)
    pg.doubleClick(busy, duration=0.3)
    time.sleep(3)


def company_selection(comp_code):
    pg.press("enter")
    time.sleep(0.5)
    pg.typewrite(comp_code)
    pg.press('tab')
    pg.press("enter")
    time.sleep(1)


def busy_login(username):    #implement logging and end script if incorrect creds
    pg.typewrite(username)
    pg.press("tab")
    try:
        
    pg.typewrite



def sales_report():
    start_rdc()
    time.sleep(2)
    open_busy()    





