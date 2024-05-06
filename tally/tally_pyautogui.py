import pyautogui as pag
import subprocess
import time
from datetime import date


pag.FAILSAFE = True

pag.PAUSE = 0.5


rdc_password = "GA@ur0107$"

test_id = "Ruchir"
test_pass = r"RU@5087$$"

t_comp_path = r"\\BusyServer\Phaltan Tally Data\Data\Data" 

test_path = r"D:\Python Envs\Data_1"




def get_pos(img):
    try:
        position = pag.locateCenterOnScreen(img,confidence=0.8)
        if position is None:
            print(f"{img} not found on screen ")
            return None
        else:
            x = position[0]
            y = position[1]
            return x,y
    except OSError as e:
        raise Exception(e)


def is_process_running(process_name):
    cmd = 'tasklist /fi "imagename eq {}"'.format(process_name)
    output = subprocess.check_output(cmd, shell=True).decode()
    if process_name.lower() in output.lower():
        return True
    else:
        return False

def starting_tally():
    pag.hotkey("win", "d")
    if not is_process_running("tally.exe"):
        tally_pos = get_pos("tally_image.jpeg")
        pag.moveTo(tally_pos, duration=1)
        pag.doubleClick(tally_pos)
        time.sleep(7)
        pag.press(["down", "down", "down", "enter"], interval=0.5)
        pag.typewrite(test_path)
        pag.press("enter")
    else:
        print("Tally is already running...Close it before running the script!")
        quit()



#starts with going to Desktop and checks if tally is running or not
def picking_company(company_code):
    #Choose a company here
    pag.typewrite(f'{company_code}', interval= 0.5)
    pag.press("enter")
    time.sleep(5)
    

#credentials for company selected
def entering_credentails_for_comp():
    pag.typewrite(test_id)
    pag.press("tab")
    pag.typewrite(test_pass)
    pag.press("enter")


#Starts from GOT and selects report
def selects_report(report):       #selects report type
    report_type = report
    pag.press(["d", "a",], interval= 1)
    pag.press(report_type, interval= 1)  #selects report type
    pag.press("enter", interval= 0.5)


#Changing Period
def period_input():    
    current_month = date.today().replace(day=1).strftime("%d-%m-%Y")
    today = date.today().strftime("%d-%m-%Y")
    pag.hotkey("alt", "f2")
    pag.typewrite(f'{current_month}', interval= 0.5)  
    pag.press("tab")
    pag.typewrite(f"{today}", interval= 0.5)
    pag.press("enter")


#change export format and sleep for 5secs to let the data load
def export_format_for_sales(): 
    e = "enter"   
    pag.press("f8")

    pag.press(["n",e], interval=.5) #party's address
    pag.press(["y",e], interval=.5) #voucher type
    pag.press(["y",e], interval=.5) #voucher number
    pag.press(["n",e], interval=.5) #voucher reference number
    pag.press(["n",e], interval=.5) #cosignee/buyer name
    pag.press(["y",e], interval=.5) #party's GSTIN/UIN
    pag.press(["n",e], interval=.5) #party's tax registration number
    pag.press(["n",e], interval=.5) #service tax registration number
    pag.press(["n",e], interval=.5) #PAN
    pag.press(["n",e], interval=.5) #CST Number
    pag.press(["n",e], interval=.5) #Voucher Narration
    pag.press(["n",e], interval=.5) #order details
    pag.press(["n",e], interval=.5) #receipt/dispatch details
    pag.press(["n",e], interval=.5) #import/export details
    pag.press(["n",e], interval=.5) #shipping details
    pag.press(["n",e], interval=.5) #port code 
    pag.press(["y",e], interval=.5) #quantity details
    pag.press(["n",e], interval=.5) #show using alternate units
    pag.press(["n",e], interval=.5) #rate details
    pag.press(["y",e], interval=.5) #item value
    pag.press(["y",e, e], interval=.5) #ledger amounts with Dr/Cr    
    time.sleep(1)
    pag.press("y", interval=1)
    time.sleep(5)


def export_format_for_debit(): 
    e = "enter"   
    pag.press("f8")
    pag.press(["n",e], interval=.5) #party's address
    pag.press(["y",e], interval=.5) #voucher type
    pag.press(["y",e], interval=.5) #voucher number
    pag.press(["n",e], interval=.5) #voucher reference number
    pag.press(["y",e], interval=.5) #party's GSTIN/UIN
    pag.press(["n",e], interval=.5) #party's tax registration number
    pag.press(["n",e], interval=.5) #service tax registration number
    pag.press(["n",e], interval=.5) #PAN
    pag.press(["n",e], interval=.5) #CST Number
    pag.press(["n",e], interval=.5) #Voucher Narration
    pag.press(["n",e], interval=.5) #order details
    pag.press(["n",e], interval=.5) #receipt/dispatch details
    pag.press(["n",e], interval=.5) #import/export details
    pag.press(["n",e], interval=.5) #shipping details
    pag.press(["n",e], interval=.5) #port code 
    pag.press(["y",e], interval=.5) #quantity details
    pag.press(["n",e], interval=.5) #show using alternate units
    pag.press(["n",e], interval=.5) #rate details
    pag.press(["y",e], interval=.5) #item value
    pag.press(["n",e], interval=.5) #additional cost
    pag.press(["y",e, e], interval=.5) #ledger amounts with Dr/Cr    
    time.sleep(1)
    pag.press("y", interval=1)
    time.sleep(5)


def export_format_for_credit(): 
    e = "enter"   
    pag.press("f8")
    pag.press(["n",e], interval=.5) #party's address
    pag.press(["y",e], interval=.5) #voucher type
    pag.press(["y",e], interval=.5) #voucher number
    pag.press(["n",e], interval=.5) #voucher reference number
    pag.press(["y",e], interval=.5) #party's GSTIN/UIN
    pag.press(["n",e], interval=.5) #party's tax registration number
    pag.press(["n",e], interval=.5) #service tax registration number
    pag.press(["n",e], interval=.5) #PAN
    pag.press(["n",e], interval=.5) #CST Number
    pag.press(["n",e], interval=.5) #Voucher Narration
    pag.press(["n",e], interval=.5) #order details
    pag.press(["n",e], interval=.5) #receipt/dispatch details
    pag.press(["n",e], interval=.5) #import/export details
    pag.press(["n",e], interval=.5) #shipping details
    pag.press(["n",e], interval=.5) #port code 
    pag.press(["y",e], interval=.5) #quantity details
    pag.press(["n",e], interval=.5) #show using alternate units
    pag.press(["n",e], interval=.5) #rate details
    pag.press(["y",e], interval=.5) #item value
    pag.press(["y",e, e], interval=.5) #ledger amounts with Dr/Cr    
    time.sleep(1)
    pag.press("y", interval=1)
    time.sleep(5)


#on the way to export
def initiating_export_with_configuration(filename, number):

    pag.hotkey("alt", "e")
    pag.press("enter")
    pag.press("c")

#export type configuration
    export_path = r"D:\UserProfile\Desktop\test_tally_export"
    pag.press("down", presses= number)
    pag.press(["enter","e", "enter"],interval=.5) #change file type
    pag.press("down", presses= 5)
    pag.press(["enter", "up", "up", "enter"], interval=0.5)
    pag.typewrite(export_path, interval=0.3)
    pag.press("enter", interval=0.5)
    pag.press("enter", interval=0.5)
    pag.press(["down","enter"],interval=0.5)
    pag.press("del", presses= 20)
    pag.typewrite(filename)

    pag.press("enter")
    pag.hotkey("ctrl", "a")
    time.sleep(1)
    pag.press("e")
    time.sleep(5)





def closes_export_file_back_to_GOT():
    pag.hotkey("alt", "f4")

    #coming back to tally report page
    pag.press("esc", presses=4)
    

def selecting_report_and_interating(reports, comp):

    for rep in reports:
        if rep == "s" :
            selects_report(report=rep)
            period_input()
            export_format_for_sales()
            initiating_export_with_configuration(filename= f"{comp}_{rep}.xlsx", number= 11 )
            closes_export_file_back_to_GOT()
        elif rep == "d":
            selects_report(report=rep)
            period_input()
            export_format_for_debit()
            initiating_export_with_configuration(filename= f"{comp}_{rep}.xlsx", number= 10)
            closes_export_file_back_to_GOT()
        elif rep == "e":
            selects_report(report=rep)
            period_input()
            export_format_for_credit()
            initiating_export_with_configuration(filename= f"{comp}_{rep}.xlsx", number= 10)
            closes_export_file_back_to_GOT()
        elif rep == "r" or rep == "y" or rep == "j":
            selects_report(report=rep)
            period_input()
            pag.hotkey("alt", "f5",interval=0.5)
            time.sleep(5)
            initiating_export_with_configuration(filename= f"{comp}_{rep}.xlsx", number= 16)
            closes_export_file_back_to_GOT()            


## Iteration for reports of a company starts here  ##
company_reports = ["y", "j"] 
comp = [10009, 91820]


starting_tally()
for c in comp:
    picking_company(company_code=f"{c}")

    entering_credentails_for_comp()

    selecting_report_and_interating(reports= company_reports, comp= c)

    pag.hotkey("alt", "f3")




