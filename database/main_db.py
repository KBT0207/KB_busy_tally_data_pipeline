import glob
from datetime import datetime, timedelta
from database.sql_connector import db_engine, db_connector
from database.busy_data_processor import BusyDataProcessor, get_filename, get_compname
from database.tally_data_processor import TallyDataProcessor
from database.models.base import Base
from database.db_crud import DatabaseCrud
from logging_config import logger
from utils.common_utils import busy_tables, tally_tables
from utils.email import email_send



def truncate_busy_masters():    
    Base.metadata.create_all(db_engine)    

    tables_list = list(busy_tables.keys())
    importer = DatabaseCrud(db_connector)
    for table in tables_list:
        if "acc" in table or "items" in table:
            importer.truncate_table(table_name=table, commit=True)
    


def delete_busy_sales():    
    Base.metadata.create_all(db_engine)

    current_date = datetime.today().date()
    date1 = current_date - timedelta(days=2)
    # date1= "2024-05-06"
    date2 = current_date - timedelta(days=1)
    # date2= "2024-05-07"

    tables_list = list(busy_tables.keys())
    importer = DatabaseCrud(db_connector)
    for table in tables_list:
        if "sales" in table:
            importer.delete_date_range_query(table, start_date= date1, end_date=date2, commit=True)



def delete_busy_material():    
    Base.metadata.create_all(db_engine)

    startdate = datetime.now().replace(day=1).strftime("%Y-%m-%d")

    endate = datetime.today().strftime("%Y-%m-%d")
    
    tables_list = list(busy_tables.keys())
    importer = DatabaseCrud(db_connector)
    for table in tables_list:
        if "mitp" in table or "mrfp" in table:
            importer.delete_date_range_query(table, start_date=startdate, end_date=endate, commit=True)



def delete_tally_data():    
    Base.metadata.create_all(db_engine)

    current_date = datetime.today().date()
    startdate = current_date - timedelta(days=2)
    #date1= "2024-05-03"
    endate = current_date - timedelta(days=1)
    #date2= "2024-05-02"

    tables_list = list(tally_tables.keys())
    importer = DatabaseCrud(db_connector)
    
    for table in tables_list:
        if 'accounts' not in table:
            importer.delete_date_range_query(table, start_date= startdate, end_date=endate, commit=True)



def import_busy_sales():    
    Base.metadata.create_all(db_engine)
    
    # todays_date = "Apr-2024"
    todays_date = datetime.today().strftime("%d-%b-%Y")
    busy_files = glob.glob("D:\\automated_busy_downloads\\" + f"**\\*sales*{todays_date}.xlsx", recursive=True)
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
            logger.error(f"{get_filename(file)} and {get_compname(file)} of {file} didn't match the criteria")    
    else:
        logger.critical("No File for today's date found to import in database")



def import_tally_data():    
    Base.metadata.create_all(db_engine)
    
    # todays_date = "Apr-17-May-24"
    todays_date = datetime.today().strftime("%d-%b-%Y")
    tally_files = glob.glob("D:\\automated_tally_downloads\\" + f"**\\*{todays_date}.xlsx", recursive=True)
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
                importer.import_data('tally_accounts', excel_data.clean_and_transform(), commit=True)

            if get_filename(file) == 'items':
                importer.import_data('tally_items', excel_data.clean_and_transform(), commit=True)

            logger.info(f"{get_filename(file)} and {get_compname(file)} imported into database.. ")
        else:
            logger.error(f"{get_filename(file)} and {get_compname(file)} of {file} didn't match the criteria")    

    else:
        logger.critical("No File for today's date found to import in database")




def dealer_price_validation_report(from_date, to_date):
    
    db_crud = DatabaseCrud(db_connector)
    
    validation_df = db_crud.sales_price_validation(from_date= from_date, to_date= to_date)  
    
    if validation_df is not None:
        counts = len(validation_df)
        validation_df.to_excel(fr"D:\Reports\Price Validation from Month to {to_date}.xlsx", index=False)
        
        subject = f"Busy Sales Price Validation Report from Month to {to_date} with {counts} rows of descrepancies"
        body = f"Greetings All,\nKindly find the Busy Sales Price Validation Report attached from Month to {to_date} with {counts} rows of descrepancies.\n In the attached excel, column 'Total Price' is the sum of List Price ('Sales_Price') and 'Discout_Amt' which is the compared with the actual Price List."
        attachment = fr"D:\Reports\Price Validation from Month to {to_date}.xlsx"
        logger.info(f"Busy Sales Price Validation Report Exported to Excel with Descrepencies")

    else:
        subject = f"Busy Sales Price Validation Report from Month to {to_date} without descrepancy"
        attachment = None
        body = f"Greetings All,\nAs per yesterday's data, there were no descrepancy found in busy sales with the price list."

        logger.info(f"Report Produced without discrepancies")

    try:
        receivers = ['shivprasad@kaybeebio.com', 
                     'holkar.h@kaybeebio.com'
                    ]
        cc = ['danish@kaybeeexports.com', 's.gaurav@kaybeeexports.com', 
              'mahendra@kaybeeexports.com'
            ]
        email_send(reciever= receivers, cc= cc, subject= subject, contents= body, attachemnts= attachment)
        logger.info(f"Successfully emailed the Busy Sales Price Validation Report.")
    except Exception as e:
        logger.critical(f"Failed to email the Busy Sales Price Validation Report : {e}")



from database.test_import import test_importing

def one():
    # Base.metadata.create_all(db_engine)
    acc_file = r"D:\tally_accounts\10001_accounts_testing.xlsx"
    xl = TallyDataProcessor(excel_file_path= acc_file)
    df = xl.clean_and_transform()
    df = df.fillna("NA")
    df = df.drop(columns='material_centre', axis=1)
    # print(df.head(10))
    # importer = DatabaseCrud(db_connector)
    test_importing(table_name='test_table', df=df, commit=True)


