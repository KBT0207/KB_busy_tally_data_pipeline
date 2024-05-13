import glob
from datetime import datetime, timedelta
from database.sql_connector import db_engine, db_connector
from database.busy_data_processor import BusyDataProcessor, get_filename, get_compname
from database.tally_data_processor import TallyDataProcessor
from database.models.base import Base
from database.db_crud import DatabaseCrud
from logging_config import logger
from utils.common_utils import busy_tables, tally_tables



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
        importer.delete_date_range_query(table, start_date= startdate, end_date=endate, commit=True)



def import_busy_sales():    
    Base.metadata.create_all(db_engine)
    
    # todays_date = "08-May-2024"
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
    
    #todays_date = "04-May-2024"
    today_date = datetime.today().strftime("%d-%b-%Y")

    pattern_master = f"D:\\automated_busy_downloads\\**\\*masters*{today_date}.xlsx"
    pattern_item = f"D:\\automated_busy_downloads\\**\\*item*{today_date}.xlsx"
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
    
    # todays_date = "Apr-17-Mar-23"
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

            logger.info(f"{get_filename(file)} and {get_compname(file)} imported into database.. ")
        else:
            logger.error(f"{get_filename(file)} and {get_compname(file)} of {file} didn't match the criteria")    

    else:
        logger.critical("No File for today's date found to import in database")



def test(sheet):
    import pandas as pd
    from xlwings import view
    file_path = r"D:\automated_scripts\busy\Old Busy data.xlsx"
    
    df =  pd.read_excel(file_path, sheet_name= sheet)
    
    columns_ffill = ["Date", "Vch/Bill No", "Party Type", "Material Centre", "Particulars", "State"]
    df.loc[:, columns_ffill] = df[columns_ffill].ffill()

    columns_fillna_with_0 = ["MRP", "Disc %", "Discount Amt", "Tax Amt", "Bill Amount"]
    df.loc[:,columns_fillna_with_0] = df[columns_fillna_with_0].fillna(0)

    columns_conditional_ffill = ["Dealer Code", "TIN/GSTIN No.", "DC No",
                                    "DC Date", "E Invoice", "Salesman",
                                    "SALES ORDER NO", "SALES ORDER DATE", 
                                    "E WAY BILL", "Transporter Name", 
                                    "Narration"]
    
    for column in columns_conditional_ffill:
        vch_to_dc = df[["Vch/Bill No", column]].dropna().set_index('Vch/Bill No')[column].to_dict()
        df.loc[:, column] = df['Vch/Bill No'].map(vch_to_dc)
    
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")
    df = df.rename(columns= {"vch/bill_no": "voucher_no", "tin/gstin_no": "gst_no",
                             "qty": "main_qty", "unit": "main_unit", "price": "main_price",
                             "qty1": "alt_qty", "unit1": "alt_unit", "price1": "alt_price", 
                             "disc_%": "discount_perc", "bill_amount": "bill_amt",
                             })

    df["mfg_date"] = pd.to_datetime(df["mfg_date"]).dt.strftime("%b-%Y")
    df["exp_date"] = pd.to_datetime(df["exp_date"]).dt.strftime("%b-%Y")

    #view(df)
    importer = DatabaseCrud(db_connector)
    importer.import_data("busy_sales", df=df, commit=True)

