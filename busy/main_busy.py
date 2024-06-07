import pyautogui as pg
import time
import os
import glob
from datetime import datetime, timedelta
from dotenv import load_dotenv
from busy import busy_utils
from utils import email
from logging_config import logger
from busy import export_busy_reports

load_dotenv('.env')


companies = ['comp0005', 'comp0010', 'comp0011', 'comp0014', 'comp0015']

sales_dict = {'trans_list': [export_busy_reports.select_sales_list, 
                                   export_busy_reports.select_salesreturn_list, 
                                   export_busy_reports.select_salesorder_list,
                                   ], 
                'reports': ['sales', 'sales_return', "sales_order",
                                    ]}

material_dict = {'trans_list': [export_busy_reports.select_mrfp_list, 
                                export_busy_reports.select_mitp_list,
                                ], 
                'reports': ["material_received_from_party", "material_issued_to_party",
                            ]}



def exporting_sales():

    busy_utils.open_busy()
    
    for comp in companies:

        busy_utils.company_selection(comp_code = comp)
        
        try:
            busy_utils.busy_login(username= os.getenv('BUSY_USERNAME'),
                            password= os.getenv('BUSY_PASSWORD'))
            logger.info(f"Logged into Busy of {comp} successfully...")
        except Exception as e:
            logger.critical(f"Logging into Busy of {comp} Failed! : {e}")
        
        
        for rep_func, report in zip(sales_dict['trans_list'], sales_dict['reports']):
            if comp != "comp0005" and report == "sales_order" and rep_func == export_busy_reports.select_salesorder_list:
                continue
            else:
                export_busy_reports.transaction_report_selection(report= rep_func)

                endate = datetime.today().date()
                #endate = "2024-05-03"
                startdate = endate - timedelta(days=2)

                endate_str = endate.strftime("%d-%m-%Y")
                #endate_str = "03-05-2024"
                #startdate_str = "01-05-2024"
                startdate_str = startdate.strftime("%d-%m-%Y")
                
                try:
                    export_busy_reports.list_format(report_type= report, 
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

    busy_utils.find_img(img='busy/images/quit_at_login.png')
    pg.click()
    time.sleep(5)
    pg.press('e')
    pg.press('enter')
    logger.info("Quit Busy Successfully!")

    today_date = datetime.today().strftime("%d-%b-%Y")
    #today_date = "03-May-2024"
    receivers = ['shivprasad@kaybeebio.com',  
                 'sayali@kaybeeexports.com']
    cc = ['s.gaurav@kaybeeexports.com', 'danish@kaybeeexports.com']
    attachment_path = glob.glob("D:\\automated_busy_downloads\\" + f"**\\*sales*{today_date}.xlsx", recursive=True)

    subj_sales = f"KB Companies ['Sales, Sales Voucher and Sales Order'] data of {endate_str}"
    body_sales = f"Kindly find the attached 'Sales, Sales Voucher and Sales Order' data of {companies} from {startdate_str} to {endate_str}" 
    attachment_path_sales = []
    for file in attachment_path:
        if 'sale' in file:
            attachment_path_sales.append(file) 
    if len(attachment_path_sales) != 0:
        try:
            email.email_send(reciever=receivers, cc = cc,
                            subject= subj_sales, 
                            contents= body_sales, 
                            attachemnts= attachment_path_sales)
            logger.info("Attachments (All Sales) emailed successfully... ")
        except Exception as e:
            logger.critical(f"Failed to email the attachment for (All Sales)! : {e}")
    else:
        logger.critical("No data for (All Sales) exported today")


    subj_sales_order = f"KBBIO Sales Order of {endate_str}"
    attachment_path_sales_order = fr"D:\automated_busy_downloads\comp0005\sales_order\comp0005_sales_order_{today_date}.xlsx"
    body_sales_order = f"Kinldy find the Sales Order of {endate_str}"
    if attachment_path_sales_order:
        try:
            email.email_send(reciever="rajani@kaybeebio.com", cc = "s.gaurav@kaybeeexports.com", 
                            subject= subj_sales_order, 
                            contents= body_sales_order, 
                            attachemnts= attachment_path_sales_order)
            logger.info("Sales Order emailed successfully... ")
        except Exception as e:
            logger.critical(f"Failed to email the attachment for Sales Order! : {e}")
    else:
        logger.critical("No data for Sales_Order exported today")




def exporting_master_and_material():

    busy_utils.open_busy()
    
    for comp in companies:

        busy_utils.company_selection(comp_code = comp)
        
        try:
            busy_utils.busy_login(username= os.getenv('BUSY_USERNAME'),
                            password= os.getenv('BUSY_PASSWORD'))
            logger.info(f"Logged into Busy of {comp} successfully...")
        except Exception as e:
            logger.critical(f"Logging into Busy of {comp} Failed! : {e}")
            
        curr_date = datetime.today().strftime("%d-%b-%Y")

        for rep_func, report in zip(material_dict['trans_list'], material_dict['reports']):
        
            export_busy_reports.transaction_report_selection(report= rep_func)
            #endate = "2024-05-03"
            startdate = datetime.now().replace(day=1).strftime("%d-%m-%Y")

            endate = datetime.today().strftime("%d-%m-%Y")
            #endate_str = "03-05-2024"
            
            try:
                export_busy_reports.list_format(report_type= report, 
                                start_date= startdate, 
                                end_date= endate)
                logger.info(f"Generated data for {comp} and {report} to export successfully...")
            except Exception as e:
                logger.critical(f"Data Generation for {comp} and {report} Failed! : {e}")

            try:
                #curr_date = datetime.today().strftime("%d-%b-%Y")
                busy_utils.export_format(report_type = report, company = comp, 
                                        filename= f"{comp}_{report}_{curr_date}")
                logger.info(f"Exported data for {comp} and {report} successfully...")
            except Exception as e:
                logger.critical(f"Exporting Data for {comp} and {report} Failed! : {e}")

            try:    
                busy_utils.return_to_busy_home(esc=3)
                time.sleep(3)

                logger.info(f"Report Generated for {comp} and {report} successfully and back to busy home...")
            except Exception as e:
                logger.critical(f"Failed to go back busy home! : {e}")

        try:
            export_busy_reports.select_masters()
            export_busy_reports.select_accounts()
            busy_utils.export_format(report_type= "master_accounts", 
                                     company= comp, 
                                     filename=f"{comp}_master_accounts_{curr_date}")
            
            busy_utils.return_to_busy_home(esc=6)
            time.sleep(5)
            logger.info(f"Master Accounts for {comp} generated successfully and back to busy home...")
        except:
            logger.critical(f"Failed to go back busy home! : {e}")
      
        try:
            export_busy_reports.select_masters()
            export_busy_reports.select_items()
            busy_utils.export_format(report_type= "items", 
                                            company= comp, 
                                            filename=f"{comp}_items_{curr_date}")
                    
            logger.info(f"Items Data for {comp} generated successfully and back to busy home...")
            busy_utils.return_to_busy_home(esc=5)
        except:
            logger.critical(f"Failed to go back busy home! : {e}")

        try:    
            busy_utils.change_company()
            time.sleep(5)
            pg.press('enter')
            logger.info(f"Successfully came to company page after {comp} page...")
        except Exception as e:
            logger.critical(f"Failed to go to company page! : {e}")

    time.sleep(2)

    busy_utils.find_img(img='busy/images/quit_at_login.png')
    pg.click()
    time.sleep(5)
    pg.press('e')
    pg.press('enter')
    logger.info("Quit Busy Successfully!")

    #today_date = "03-May-2024"
    receivers = ['shivprasad@kaybeebio.com', 'danish@kaybeeexports.com']
    #receivers = ['s.gaurav@kaybeeexports.com']
    body_material = f"Kindly find the attached MITP & MRFP data of {companies} from {startdate} to {endate}"
    
    attachment_path = glob.glob("D:\\automated_busy_downloads\\" + f"**\\*{curr_date}.xlsx", recursive=True)

    subj_material = f"KB Companies ['MITP & MRFP'] data of MTD of {datetime.today().strftime("%B")}"
    attachment_path_material = []
    for file in attachment_path:
        if 'material' in file:
            attachment_path_material.append(file) 
    if len(attachment_path_material) != 0:
        try:
            email.email_send(reciever=receivers, cc = "s.gaurav@kaybeeexports.com", 
                            subject= subj_material, 
                            contents= body_material, 
                            attachemnts= attachment_path_material)
            logger.info("Attachments of MITP & MRFP emailed successfully... ")
        except Exception as e:
            logger.critical(f"Failed to email the attachment for (MITP & MRFP)! : {e}")
    else:
        logger.critical("No data for MITP & MRFP exported today")
