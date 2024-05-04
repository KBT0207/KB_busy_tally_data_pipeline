import pyautogui as pg
from tally import tally_utils
from utils.common_utils import tally_reports
from datetime import datetime

def test():
    for r in list(tally_reports.keys()):
        print(r, tally_reports[r])


companies = ["10009"]

def exporting_data(company=companies):
    todays_date = datetime.today().strftime("%d-%b-%Y")
    date1 = '01-5-2024'
    date2 = '04-5-2024'
    pg.hotkey("win", "d")
    tally_utils.start_tally()
    
    for comp in company:
        tally_utils.select_company(company_code= comp)
        for rep in list(tally_reports.keys()):
            tally_utils.exporting_reports(report= rep, 
                        from_date= date1, to_date= date2,
                        path= fr"D:\automatic_tally_downloads\{comp}\{tally_reports[rep]}",
                        filename= f"{comp}_{tally_reports[rep]}_{todays_date}.xlsx", 
                        esc= 4)
        
        tally_utils.change_company()


