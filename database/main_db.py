import glob
import pandas as pd
from datetime import datetime, timedelta
from database.sql_connector import db_engine, db_connector
from database.busy_data_processor import BusyDataProcessor, get_filename, get_compname
from database.tally_data_processor import TallyDataProcessor
from database.models.base import Base
from database.db_crud import DatabaseCrud
from logging_config import logger
from utils.common_utils import busy_tables, tally_tables
from utils.email import email_send
from main_reports.reports import Reports



def truncate_busy_masters():    
    Base.metadata.create_all(db_engine)    

    tables_list = list(busy_tables.keys())
    importer = DatabaseCrud(db_connector)
    for table in tables_list:
        if "acc" in table or "items" in table:
            importer.truncate_table(table_name=table, commit=True)
    



def delete_busy_sales(startdate:str, enddate:str, commit:bool):   
    if startdate <= enddate:
        Base.metadata.create_all(db_engine)

        busy_sales_table = ['busy_sales', 'busy_sales_order', 'busy_sales_return']
        importer = DatabaseCrud(db_connector)
        for table in busy_sales_table:
            importer.delete_date_range_query(table, start_date= startdate, end_date=enddate, commit=commit)
    else:
        logger.critical(f"Start date: {startdate} should be equal or greater than end date: {enddate}.")



def delete_busy_material():    
    Base.metadata.create_all(db_engine)

    startdate = datetime.now().replace(day=1).strftime("%Y-%m-%d")

    endate = datetime.today().strftime("%Y-%m-%d")
    
    tables_list = list(busy_tables.keys())
    importer = DatabaseCrud(db_connector)
    for table in tables_list:
        if "mitp" in table or "mrfp" in table:
            importer.delete_date_range_query(table, start_date=startdate, end_date=endate, commit=True)




def delete_tally_data(start_date:str, end_date:str, commit:bool):    
    Base.metadata.create_all(db_engine)

    tables_list = list(tally_tables.keys())
    importer = DatabaseCrud(db_connector)
    
    exclude_tables = ['tally_accounts', 'outstanding_balance', 'tally_receivables']
    for table in tables_list:
        if table not in exclude_tables:
            importer.delete_date_range_query(table, start_date= start_date, 
                                             end_date=end_date, commit=commit)
    importer.truncate_table(table_name= 'tally_accounts', commit= commit)



def import_busy_sales(filename:str):    
    Base.metadata.create_all(db_engine)

    busy_files = glob.glob("D:\\automated_busy_downloads\\" + f"**\\*sales*{filename}.xlsx", recursive=True)
    if len(busy_files) != 0:
        for file in busy_files:
            excel_data = BusyDataProcessor(file)
            importer = DatabaseCrud(db_connector)
            if get_filename(file) == 'sales':
                importer.import_data('busy_sales', excel_data.clean_and_transform(), commit=True)
    
            if get_filename(file) == 'sales_return':
                importer.import_data('busy_sales_return', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == 'sales_order':
                importer.import_data('busy_sales_order', excel_data.clean_and_transform(), commit=True)

            else:
                logger.error(f"{get_filename(file)} and {get_compname(file)} of {file} didn't match the criteria")    

    else:
        logger.critical("No File for today's date found to import in database")        




def import_busy_masters_material():
    Base.metadata.create_all(db_engine)
    
    # today_date = "17-Apr-2024"
    today_date = datetime.today().strftime("%d-%b-%Y")

    pattern_master = f"D:\\automated_busy_downloads\\**\\*master*{today_date}.xlsx"
    pattern_item = f"D:\\automated_busy_downloads\\**\\*items*{today_date}.xlsx"
    pattern_material = f"D:\\automated_busy_downloads\\**\\*material*{today_date}.xlsx"

    busy_files_material = glob.glob(pattern_material, recursive=True)
    busy_files_master = glob.glob(pattern_master, recursive=True)
    busy_files_item = glob.glob(pattern_item, recursive=True)

    busy_files = busy_files_master + busy_files_item + busy_files_material

    if len(busy_files) != 0:
        for file in busy_files:
            excel_data = BusyDataProcessor(file)
            importer = DatabaseCrud(db_connector)

            if get_filename(file) == 'material_issued_to_party':
                importer.import_data('busy_mitp', excel_data.clean_and_transform(), commit=True)
                
            if get_filename(file) == 'material_received_from_party':
                importer.import_data('busy_mrfp', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == "master_accounts" and get_compname(file) == "comp0005":
                importer.import_data('busy_acc_kbbio', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == "master_accounts" and get_compname(file) == "comp0010":
                importer.import_data('busy_acc_agri', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == "master_accounts" and get_compname(file) == "comp0011":
                importer.import_data('busy_acc_greenera', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == "master_accounts" and get_compname(file) == "comp0014":
                importer.import_data('busy_acc_newage', excel_data.clean_and_transform(), commit=True)
            
            if get_filename(file) == "master_accounts" and get_compname(file) == "comp0015":
                importer.import_data('busy_acc_100x', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == "items" and get_compname(file) == "comp0005":
                importer.import_data('busy_items_kbbio', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == "items" and get_compname(file) == "comp0015":
                importer.import_data('busy_items_100x', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == "items" and get_compname(file) == "comp0011":
                importer.import_data('busy_items_greenera', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == "items" and get_compname(file) == "comp0014":
                importer.import_data('busy_items_newage', excel_data.clean_and_transform(), commit=True)
            
            if get_filename(file) == "items" and get_compname(file) == "comp0010":
                importer.import_data('busy_items_agri', excel_data.clean_and_transform(), commit=True)

    else:
        logger.critical("No File for today's date found to import in database")




def import_tally_data(date):    
    Base.metadata.create_all(db_engine)
    
    tally_files = glob.glob("D:\\automated_tally_downloads\\" + f"**\\*{date}.xlsx", recursive=True)
    if len(tally_files) != 0:
        for file in tally_files:
            excel_data = TallyDataProcessor(file)
            importer = DatabaseCrud(db_connector)
            if get_filename(file) == 'sales':
                importer.import_data('tally_sales', excel_data.clean_and_transform(), commit=True)
    
            if get_filename(file) == 'sales_return':
                importer.import_data('tally_sales_return', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == 'purchase':
                importer.import_data('tally_purchase', excel_data.clean_and_transform(), commit=True)
    
            if get_filename(file) == 'purchase_return':
                importer.import_data('tally_purchase_return', excel_data.clean_and_transform(), commit=True)
            
            if get_filename(file) == 'payments':
                importer.import_data('tally_payments', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == 'receipts':
                importer.import_data('tally_receipts', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == 'journal':
                importer.import_data('tally_journal', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == 'accounts':
                importer.import_accounts_data(df=excel_data.clean_and_transform(), commit=True)

            # if get_filename(file) == 'items':
            #     importer.import_data('tally_items', excel_data.clean_and_transform(), commit=True)

                logger.info(f"{get_filename(file)} and {get_compname(file)} imported into database.. ")

    else:
        logger.critical("No File for today's date found to import in database")




def import_outstanding_tallydata(dates:list):    
    Base.metadata.create_all(db_engine)
    for date in dates:
        tally_files = glob.glob("D:\\automated_tally_downloads\\" + f"**\\*outstanding_{date}.xlsx", recursive=True)
        if len(tally_files) != 0:
            for file in tally_files:
                excel_data = TallyDataProcessor(file)
                importer = DatabaseCrud(db_connector)
                if get_filename(file) == 'outstanding':
                    importer.import_data('outstanding_balance', excel_data.clean_and_transform(), commit=True)



def import_receivables_tallydata(dates:list):    
    Base.metadata.create_all(db_engine)
    for date in dates:
        tally_files = glob.glob("D:\\automated_tally_downloads\\" + f"**\\*receivables_{date}.xlsx", recursive=True)
        if len(tally_files) != 0:
            for file in tally_files:
                excel_data = TallyDataProcessor(file)
                importer = DatabaseCrud(db_connector)
                if get_filename(file) == 'receivables':
                    importer.import_data('tally_receivables', excel_data.clean_and_transform(), commit=True)



def dealer_price_validation_report(from_date:str, to_date:str, send_email:bool, exceptions:list = None) -> None:
    """Generated dealer price validation report as per the arguments.

    Args:
        from_date (str): The date from which busy sales needed to be validated from.
        to_date (str): The date till which busy sales needed to be validated.
        send_email (bool): when False only excel file with report get generated. True if you want to send email with the excel file.
        exceptions (list, optional): Takes in Sales Voucher Number which you want to be excluded from the report. Defaults to None.
    """
    reports = Reports(db_connector)
    
    validation_df = reports.sales_price_validation(from_date= from_date, to_date= to_date, exceptions= exceptions)
    
    counts = len(validation_df)
    if counts != 0:
        
        validation_df.to_excel(fr"D:\Reports\Busy_Sales_Price\Price Validation from Month to {to_date}.xlsx", index= False)
        
        subject = f"Busy Sales Price Validation Report from Month to {to_date} with {counts} rows of discrepancies"
        body = f"Greetings All,\nKindly find the Busy Sales Price Validation Report attached from Month to {to_date} with {counts} rows of discrepancies.\n In the attached excel, column 'Total Price' is the sum of List Price ('Sales_Price') and 'Discout_Amt' which is the compared with the actual Price List."
        attachment = fr"D:\Reports\Busy_Sales_Price\Price Validation from Month to {to_date}.xlsx"
        logger.info(f"Busy Sales Price Validation Report Exported to Excel with {counts} Discrepencies")

    else:
        subject = f"Busy Sales Price Validation Report from Month to {to_date} without discrepancy"
        attachment = None
        body = f"Greetings All,\nAs per yesterday's data, there were no discrepancy found in busy sales with the price list."

        logger.info(f"Busy Sales Price Validation Report Produced without discrepancies")

    if send_email:
        try:
            receivers = ['shivprasad@kaybeebio.com', 
                        'holkar.h@kaybeebio.com'
                        ]
            cc = ['danish@kaybeeexports.com', 's.gaurav@kaybeeexports.com', 
                'mahendra@kaybeeexports.com'
                ]
            email_send(reciever= receivers, 
                       cc= cc, 
                       subject= subject, contents= body, attachemnts= attachment)
            logger.info(f"Successfully emailed the Busy Sales Price Validation Report.")
        except Exception as e:
            logger.critical(f"Failed to email the Busy Sales Price Validation Report : {e}")




def salesorder_salesman_report(from_date:str, to_date:str, send_email:bool, exceptions:list = None) -> None:
    reports = Reports(db_connector)
    
    validation_df = reports.salesman_order_validation(from_date= from_date, to_date= to_date, exceptions= exceptions)
    
    counts = len(validation_df)
    if counts != 0:
        
        validation_df.to_excel(fr"D:\Reports\Busy_SalesOrder_Salesman\Salesman Validation from Month to {to_date}.xlsx", index= False)
        
        subject = f"Busy SalesOrder Salesman Validation Report from Month to {to_date} with {counts} rows of discrepancies"
        body = f"Greetings All,\nKindly find the Busy SalesOrder Salesman Validation Report attached from Month to {to_date} with {counts} rows of discrepancies.\nThe attached excel contains the busy entries without the mention of salesman name."
        attachment = fr"D:\Reports\Busy_SalesOrder_Salesman\Salesman Validation from Month to {to_date}.xlsx"
        logger.info(f"Busy SalesOrder Salesman Validation Report Exported to Excel with {counts} Discrepencies")

    else:
        subject = f"Busy SalesOrder Salesman Validation Report from Month to {to_date} without discrepancy"
        attachment = None
        body = f"Greetings All,\nAs per yesterday's data, there were no descrepancy found in busy salesorder regarding salesman."

        logger.info(f"SalesOrder Salesman Validation Report Produced without discrepancies")

    if send_email:
        try:
            receivers = ['shivprasad@kaybeebio.com', 
                        ]
            cc = ['danish@kaybeeexports.com', 's.gaurav@kaybeeexports.com', 
                ]
            email_send(reciever= receivers, 
                       cc= cc, 
                       subject= subject, contents= body, attachemnts= attachment)
            logger.info(f"Successfully emailed the Busy SalesOrder Salesman Validation Report.")
        except Exception as e:
            logger.critical(f"Failed to email the Busy SalesOrder Salesman Validation Report : {e}")



def volume_discount_report(dates:list, send_email:bool, exceptions:list = None) -> None:
    
    def filename_date(date_range= dates) -> str:
        if len(dates) > 1:
            name = f'from {date_range[0]} to {date_range[-1]}'
        else:
            name = f'of {date_range[0]}'
        return name
    
    reports = Reports(db_connector)
    
    validation_df = reports.volume_discount_validation(dates= dates, exceptions= exceptions)
    # return view(validation_df)
    validation_df.to_excel(fr"D:\Reports\Volume_Discount\Volume Discount Report {filename_date(date_range=dates)}.xlsx", index= False)
    
    discrepancy_count = validation_df.loc[validation_df['remark'] == 'Discrepancy', 'remark'].count() 
    # print(discrepancy_count)
    if discrepancy_count > 0:
        subject = f"Busy Sales Volume Discount Report {filename_date(date_range=dates)} with {discrepancy_count} discrepancies"
        body = f"Greetings All,\nKindly find the Busy Sales Volume Discount Report {filename_date(date_range=dates)} attached with discrepancy."
        logger.info(f"Busy Sales Volume Discount Report Exported to Excel with {discrepancy_count} Discrepencies")

    else:
        subject = f"Busy Sales Volume Discount Report {filename_date(date_range=dates)} without discrepancy"
        body = f"Greetings All,\nAs per the data, there were no descrepancy found in busy sales regarding volume discount."
        logger.info(f"Volume Discount Report Produced without discrepancies")

    if send_email:
        attachment = fr"D:\Reports\Volume_Discount\Volume Discount Report {filename_date(date_range=dates)}.xlsx"
        try:
            receivers = ['shivprasad@kaybeebio.com', 
                        ]
            cc = ['danish@kaybeeexports.com', 's.gaurav@kaybeeexports.com', 
                ]
            email_send(reciever= receivers, 
                       cc= cc, 
                       subject= subject, contents= body, attachemnts= attachment)
            logger.info(f"Successfully emailed the Busy Sales Volume Discount Report.")
        except Exception as e:
            logger.critical(f"Failed to email the Busy Sales Volume Discount Report : {e}")



def cash_discount_report(dates:list, send_email:bool, exceptions:list = None) -> None:

    def filename_date(date_range= dates) -> str:
        if len(dates) > 1:
            name = f'from {date_range[0]} to {date_range[-1]}'
        else:
            name = f'of {date_range[0]}'
        return name
    
    reports = Reports(db_connector)
    # from xlwings import view
    validation_df = reports.cash_discount_validation(dates= dates, exceptions= exceptions)
    # return print(validation_df)
    validation_df.to_excel(fr"D:\Reports\Cash_Discount\Cash Discount Report {filename_date(date_range= dates)}.xlsx", index= False)
    
    discrepancy_count = validation_df.loc[validation_df['remark'] == 'Discrepancy', 'remark'].count() 
    if discrepancy_count > 0:
        subject = f"Busy Sales Cash Discount Report {filename_date(date_range= dates)} with {discrepancy_count} discrepancies"
        body = f"Greetings All,\nKindly find the Busy Sales Cash Discount Report {filename_date(date_range= dates)} attached with discrepancy."
        logger.info(f"Busy Sales Cash Discount Report Exported to Excel with {discrepancy_count} Discrepencies")

    else:
        subject = f"Busy Sales Cash Discount Report {filename_date(date_range= dates)} without discrepancy"
        body = f"Greetings All,\nAs per the data of the above mentioned dates, there were no descrepancy found in busy sales regarding Cash discount."
        logger.info(f"Cash Discount Report Produced without discrepancies")

    if send_email:
        attachment = fr"D:\Reports\Cash_Discount\Cash Discount Report {filename_date(date_range= dates)}.xlsx"
        try:
            receivers = ['shivprasad@kaybeebio.com', 
                        ]
            cc = ['danish@kaybeeexports.com', 's.gaurav@kaybeeexports.com', 
                ]
            email_send(reciever= receivers, 
                       cc= cc, 
                       subject= subject, contents= body, attachemnts= attachment)
            logger.info(f"Successfully emailed the Busy Sales Cash Discount Report.")
        except Exception as e:
            logger.critical(f"Failed to email the Busy Sales Cash Discount Report : {e}")



def busy_tally_sales_reco(start_date:str, end_date:str, send_email:bool, exceptions:list = None) -> None:
    report = Reports(db_connector)
    try:
        report.sales_validation(fromdate= start_date, todate= end_date, exceptions= exceptions)
        logger.info(f"Busy-Tally sales reco from Month to date: {end_date} exported in excel")
        busy_sales_df = pd.read_excel(fr'D:\Reports\Sales_Validation\Busy_vs_Tally_Sales_Reco_Month-to-{end_date}.xlsx', 
                                      sheet_name= 'Busy Sales')
        tally_sales_df = pd.read_excel(fr'D:\Reports\Sales_Validation\Busy_vs_Tally_Sales_Reco_Month-to-{end_date}.xlsx', 
                                       sheet_name= 'Tally Sales')
    except Exception as e :
        logger.critical(f"Error occured: {e} \n\nWhile exporting Busy-Tally sales reco from Month to date: {end_date} in excel format")
    busy_amnt_discrepancy = busy_sales_df.loc[busy_sales_df['amount_diff'] >= 5].shape[0]
    tally_amnt_discrepancy = tally_sales_df.loc[tally_sales_df['amount_diff'] >= 5].shape[0]
    busy_gst_discrepancy = busy_sales_df.loc[busy_sales_df['gst_remark'] == 'Matched'].shape[0]
    tally_gst_discrepancy = tally_sales_df.loc[tally_sales_df['gst_remark'] == 'Matched'].shape[0]

    if (busy_amnt_discrepancy > 0) or (tally_amnt_discrepancy > 0) or (busy_gst_discrepancy > 0) or (tally_gst_discrepancy > 0):
        subject = f"Discrepancy found in Busy-Tally Sales Reco from Month to date: {end_date}"
        body = f"Greetings All,\nKindly find the Busy-Tally Sales Reco from Month to date: {end_date} attached with discrepancies."
        logger.info(f"Busy-Tally Sales Reco Exported to Excel with discrepancy.")

    else:
        subject = f"No discrepancy found in Busy-Tally Sales Reco from Month to date: {end_date}"
        body = f"Greetings All,\nKindly find the Busy-Tally Sales Reco from Month to date: {end_date} attached without discrepancies."
        logger.info(f"Busy-Tally Sales Reco Exported to Excel without discrepancy.")

    if send_email:
        attachment = fr"D:\Reports\Sales_Validation\Busy_vs_Tally_Sales_Reco_Month-to-{end_date}.xlsx"
        try:
            receivers = ['shivprasad@kaybeebio.com', 
                        ]
            cc = ['danish@kaybeeexports.com', 's.gaurav@kaybeeexports.com', 
                ]
            email_send(reciever= receivers, 
                       cc= cc, 
                       subject= subject, contents= body, attachemnts= attachment)
            logger.info(f"Successfully emailed the Busy-Tally Sales Reco Report.")
        except Exception as e:
            logger.critical(f"Failed to email the Busy-Tally Sales Reco Report: {e}")


def busy_tally_salesreturn_reco(start_date:str, end_date:str, send_email:bool, exceptions:list = None) -> None:
    report = Reports(db_connector)
    try:
        report.sales_return_validation(fromdate= start_date, todate= end_date, exceptions= exceptions)
        logger.info(f"Busy-Tally sales return reco from Month to date: {end_date} exported in excel")
        busy_df = pd.read_excel(fr'D:\Reports\Sales_Return_Validation\Busy_vs_Tally_Sales_Return_Reco_Month-to-{end_date}.xlsx', 
                                      sheet_name= 'Busy Sales Return')
        tally_df = pd.read_excel(fr'D:\Reports\Sales_Return_Validation\Busy_vs_Tally_Sales_Return_Reco_Month-to-{end_date}.xlsx', 
                                       sheet_name= 'Tally Sales Return')
    except Exception as e :
        logger.critical(f"Error occured: {e} \n\nWhile exporting Busy-Tally sales return reco from Month to date: {end_date} in excel format")
    busy_amnt_discrepancy = busy_df.loc[busy_df['amount_diff'] >= 5].shape[0]
    tally_amnt_discrepancy = tally_df.loc[tally_df['amount_diff'] >= 5].shape[0]
    busy_gst_discrepancy = busy_df.loc[busy_df['gst_remark'] == 'Matched'].shape[0]
    tally_gst_discrepancy = tally_df.loc[tally_df['gst_remark'] == 'Matched'].shape[0]

    if (busy_amnt_discrepancy > 0) or (tally_amnt_discrepancy > 0) or (busy_gst_discrepancy > 0) or (tally_gst_discrepancy > 0):
        subject = f"Discrepancy found in Busy-Tally Sales Return Reco from Month to date: {end_date}"
        body = f"Greetings All,\nKindly find the Busy-Tally Sales Return Reco from Month to date: {end_date} attached with discrepancies."
        logger.info(f"Busy-Tally Sales Return Reco Exported to Excel with discrepancy.")

    else:
        subject = f"No discrepancy found in Busy-Tally Sales Return Reco from Month to date: {end_date}"
        body = f"Greetings All,\nKindly find the Busy-Tally Sales Return Reco from Month to date: {end_date} attached without discrepancies."
        logger.info(f"Busy-Tally Sales Return Reco Exported to Excel without discrepancy.")

    if send_email:
        attachment = fr"D:\Reports\Sales_Return_Validation\Busy_vs_Tally_Sales_Return_Reco_Month-to-{end_date}.xlsx"
        try:
            receivers = ['shivprasad@kaybeebio.com', 
                        ]
            cc = ['danish@kaybeeexports.com', 's.gaurav@kaybeeexports.com', 
                ]
            email_send(reciever= receivers, 
                       cc= cc, 
                       subject= subject, contents= body, attachemnts= attachment)
            logger.info(f"Successfully emailed the Busy-Tally Sales Return Reco Report.")
        except Exception as e:
            logger.critical(f"Failed to email the Busy-Tally Sales Return Reco Report: {e}")



def salesorder_mitp_reco_report(start_date:str, end_date:str, send_email:bool, exceptions:list = None) -> None:
    reports = Reports(db_connector)
    salesorder_df = reports.salesorder_mitp_reco(fromdate= start_date, todate= end_date, exceptions= exceptions)
    salesorder_df.to_excel(fr"D:\Reports\SalesOrder_MITP_Reco\SalesOrder-MITP-Reco-Month-to-{end_date}.xlsx", index= False)
    
    discrepancy_count = salesorder_df.loc[salesorder_df['remark'] == 'Discrepancy', 'remark'].count() 
    if discrepancy_count > 0:
        subject = f"Busy Sales Order-MITP Reco from Month to {end_date} with {discrepancy_count} discrepancies"
        body = f"Greetings All,\nKindly find the Busy Sales Order - MITP Reco from Month to {end_date} attached with discrepancy."
        logger.info(f"Busy Sales Order - MITP Reco Exported to Excel with {discrepancy_count} Discrepencies")
    
    else:
        subject: f"Busy Sales Order-MITP Reco from Month to {end_date} without discrepancies"
        body = f"Greetings All,\nKindly find the Busy Sales Order - MITP Reco from Month to {end_date} attached without discrepancy."
        logger.info(f"Busy Sales Order - MITP Reco Exported to Excel without Discrepencies")

    if send_email:
        attachment = fr"D:\Reports\SalesOrder_MITP_Reco\SalesOrder-MITP-Reco-Month-to-{end_date}.xlsx"
        try:
            receivers = ['shivprasad@kaybeebio.com', 
                        ]
            cc = ['danish@kaybeeexports.com', 's.gaurav@kaybeeexports.com', 
                ]
            email_send(reciever= receivers, 
                       cc= cc, 
                       subject= subject, contents= body, attachemnts= attachment)
            logger.info(f"Successfully emailed the Busy Sales Order - MITP Reco.")
        except Exception as e:
            logger.critical(f"Failed to email the Busy Sales Order - MITP Reco : {e}")




# def import_tally_accounts():
#     path = r'D:\automated_tally_downloads\10007\accounts\10007_accounts_21-May-2024.xlsx'
#     db_crud = DatabaseCrud(db_connector)
#     tally = TallyDataProcessor(path)
#     data = tally.clean_and_transform()
#     db_crud.import_unmatched_data(df=data, commit=True)
    
    # db_crud.import_unmatched_data(df=data, commit=False)
#     db_crud = DatabaseCrud(db_connector)
#     data = db_crud.import_unmatched_data(df=df, commit=commit)
#     print(data)


def rep():
    Base.metadata.create_all(db_engine)
    r = Reports(db_connector)
    return r.populate_debtor_balances(fromdate= '2024-04-01', todate= '2024-06-15', to_import= False,
                                      to_export= True , filename= "test_file", commit= True
                            # # fromdate= datetime.today().date().replace(day=1).strftime("%Y-%m-%d"), 
                            # todate= datetime.today().date().strftime("%Y-%m-%d"), 
                            )


def one(path, commit):
    Base.metadata.create_all(db_engine)

    import pandas as pd
    import numpy as np
    xl = BusyDataProcessor(excel_file_path= path)
    data = xl.clean_and_transform()

    from xlwings import view
    importer = DatabaseCrud(db_connector)
    importer.import_data( df= data, table_name= 'busy_acc_kbbio', commit=commit)
    # importer.test_import_data(table_name= 'busy_sales', 
    #                                 df= data, commit=commit)
    # view(data)


def balance(path):
    # Base.metadata.create_all(db_engine)
    
    importer = TallyDataProcessor(excel_file_path=path)
    df = importer.clean_and_transform()
    from xlwings import view
    view(df)

# def delete_one(commit):
#     # Base.metadata.create_all(db_engine)
#     acc_file = r"D:\tally_accounts\10001_accounts_testing.xlsx"
#     xl = TallyDataProcessor(excel_file_path= acc_file)
#     df = xl.clean_and_transform()
#     df = df.fillna("NA")
#     df = df.drop(columns='material_centre', axis=1)
#     # print(df.head(10))
#     importer = DatabaseCrud(db_connector)
#     importer.test_delete(table_name='test_table', start_date= '2024-05-20 17:47:00' , end_date= '2024-05-20 17:49:00', commit=commit)

