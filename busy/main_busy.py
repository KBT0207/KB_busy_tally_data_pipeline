import pyautogui as pg
import time
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from busy import busy_utils
from logging_config import logger
from busy import email_busy_reports
from busy.export_busy_reports import (
    select_mitp_list,
    select_mrfp_list,
    select_sales_list,
    select_salesorder_list,
    select_salesreturn_list,
    transaction_report_selection,
    list_format
)

load_dotenv('.env')


companies = ['comp0005', 'comp0010', 'comp0011', 'comp0014', 'comp0015']
companies = ['comp0014', 'comp0015']

transaction_dict = {'trans_list': [select_sales_list, select_salesreturn_list, 
                                       select_mrfp_list, select_mitp_list, 
                                       select_salesorder_list], 
                        'reports': ['sales', 'sales_return', 
                                    "material_received_from_party", "material_issued_to_party", 
                                    "sales_order"] }



def exporting_and_emailing():

    busy_utils.open_busy()
    
    for comp in companies:

        busy_utils.company_selection(comp_code = comp)
        
        try:
            busy_utils.busy_login(username= os.getenv('BUSY_USERNAME'),
                            password= os.getenv('BUSY_PASSWORD'))
            logger.info(f"Logged into Busy of {comp} successfully...")
        except Exception as e:
            logger.critical(f"Logging into Busy of {comp} Failed! : {e}")
        

        for rep_func, report in zip(transaction_dict['trans_list'], transaction_dict['reports']):
            if comp != "comp0005" and report == "sales_order" and rep_func == select_salesorder_list:
                continue
            else:
                transaction_report_selection(report= rep_func)

                endate = datetime.today()
                startdate = endate - timedelta(days=2)

                endate_str = endate.strftime("%d-%m-%Y")
                startdate_str = startdate.strftime("%d-%m-%Y")
                
                try:
                    list_format(report_type= report, 
                                    start_date= startdate_str, 
                                    end_date= endate_str)
                    logger.info(f"Generated data for {comp} and {report} to export successfully...")
                except Exception as e:
                    logger.critical(f"Data Generation for {comp} and {report} Failed! : {e}")

                try:
                    curr_date = datetime.today().strftime("%d-%b-%Y")
                    busy_utils.export_format(report_type = report, company = comp, 
                                            filename= f"{comp}_{report}_{curr_date}")
                    logger.info(f"Exported data for {comp} and {report} successfully...")
                except Exception as e:
                    logger.critical(f"Exporting Data for {comp} and {report} Failed! : {e}")

                try:    
                    busy_utils.return_to_busy_home(esc=3)
                    time.sleep(5)

                    logger.info(f"Report Generated for {comp} and {report} successfully and back to busy home...")
                except Exception as e:
                    logger.critical(f"Failed to go back busy home! : {e}")

        try:    
            busy_utils.change_company()
            time.sleep(5)
            pg.press('enter')
            logger.info(f"Successfully came to company page after {comp} page...")
        except Exception as e:
            logger.critical(f"Failed to go to company page! : {e}")

    time.sleep(2)

    busy_utils.find_img(img='busy/images/quit_at_login.png', timeout= 300)
    pg.click()
    time.sleep(5)
    pg.press('e')
    pg.press('enter')
    logger.info("Quit Busy Successfully!")

    email_busy_reports.mitp_mrfp_email()
    email_busy_reports.sales_email()