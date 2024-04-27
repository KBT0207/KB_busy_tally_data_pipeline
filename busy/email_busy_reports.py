from datetime import datetime, timedelta
import glob
from utils import email
from logging_config import logger
from busy.export_busy_reports import (
    select_mitp_list,
    select_mrfp_list,
    select_sales_list,
    select_salesorder_list,
    select_salesreturn_list,
)

companies = ['comp0005', 'comp0010', 'comp0011', 'comp0014', 'comp0015']
companies = ['comp0014', 'comp0015']

transaction_dict = {'trans_list': [select_sales_list, select_salesreturn_list, 
                                       select_mrfp_list, select_mitp_list, 
                                       select_salesorder_list], 
                        'reports': ['sales', 'sales_return', 
                                    "material_received_from_party", "material_issued_to_party", 
                                    "sales_order"] }


endate = datetime.today()
startdate = endate - timedelta(days=2)

endate_str = endate.strftime("%d-%m-%Y")
startdate_str = startdate.strftime("%d-%m-%Y")


today_date = datetime.today().strftime("%d-%b-%Y")
receivers = ['shivprasad@kaybeebio.com', 'danish@kaybeeexports.com', "rajani@kaybeebio.com"]
#receivers = ['s.gaurav@kaybeeexports.com']
reps = [r for r in transaction_dict['reports']]
body = f"Kindly find the attached [{', '.join(reps)} data of {companies} from {startdate_str} to {endate_str}"
attachment_path = glob.glob("D:\\automated_busy_downloads\\" + f"**\\*{today_date}.xlsx", recursive=True)


def mitp_mrfp_email():
    subj_material = f"KB Companies ['MITP & MRFP'] data of {endate_str}"
    attachment_path_material = []
    for file in attachment_path:
        if 'material' in file:
            attachment_path_material.append(file) 
    if len(attachment_path_material) != 0:
        try:
            email.email_send(reciever=receivers, cc = "s.gaurav@kaybeeexports.com", 
                            subject= subj_material, 
                            contents= body, 
                            attachemnts= attachment_path_material)
            logger.info("Attachments (MITP & MRFP) emailed successfully... ")
        except Exception as e:
            logger.critical(f"Failed to email the attachment for (MITP & MRFP)! : {e}")
    else:
        logger.critical("No data for (MITP & MRFP) exported today")


def sales_email():
    subj_sales = f"KB Companies ['Sales, Sales Voucher and Sales Order'] data of {endate_str}"
    attachment_path_sales = []
    for file in attachment_path:
        if 'sale' in file:
            attachment_path_sales.append(file) 
    if len(attachment_path_sales) != 0:
        try:
            email.email_send(reciever=receivers, cc = "s.gaurav@kaybeeexports.com", 
                            subject= subj_sales, 
                            contents= body, 
                            attachemnts= attachment_path_sales)
            logger.info("Attachments (All Sales) emailed successfully... ")
        except Exception as e:
            logger.critical(f"Failed to email the attachment for (All Sales)! : {e}")
    else:
        logger.critical("No data for (All Sales) exported today")


def test():
    attachment_path_sales = []
    for file in attachment_path:
        if 'sale' in file:
            attachment_path_sales.append(file) 
    print(attachment_path_sales)
