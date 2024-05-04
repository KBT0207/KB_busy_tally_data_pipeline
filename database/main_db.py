import glob
from datetime import datetime, timedelta
from database.sql_connector import db_engine, db_connector
from database.busy_data_processor import ExcelProcessor, get_filename, get_compname
from database.models.base import Base
from database.db_crud import DatabaseCrud, tables
from logging_config import logger



def delete_busy_data():    
    Base.metadata.create_all(db_engine)
    
    # file = r"D:\automated_busy_downloads\comp0014\material_received_from_party\comp0014_material_received_from_party_25-Apr-2024.xlsx"
    # excel_data = ExcelProcessor(file)
    # print(get_compname(file))
    # print(excel_data.clean_and_transform())
    #current_date = datetime.today().date()
    current_date = "2024-05-03"
    date1 = current_date - timedelta(days=1)
    date2 = current_date - timedelta(days=2)

    tables_list = list(tables.keys())
    importer = DatabaseCrud(db_connector)
    for table in tables_list:
        if "acc" in table or "items" in table:
            importer.truncate_table(table_name=table)
        else:
            importer.delete_date_query(table, date1, date2)




def import_busy_data():    
    Base.metadata.create_all(db_engine)
    
    todays_date = "03-May-2024"
    #todays_date = datetime.today().strftime("%d-%b-%Y")
    busy_files = glob.glob("D:\\automated_busy_downloads\\" + f"**\\*{todays_date}.xlsx", recursive=True)
    if len(busy_files) != 0:
        for file in busy_files:
            excel_data = ExcelProcessor(file)
            importer = DatabaseCrud(db_connector)
            if get_filename(file) == 'sales':
                importer.import_data('busy_sales', excel_data.clean_and_transform())
    
            if get_filename(file) == 'sales_return':
                importer.import_data('busy_sales_return', excel_data.clean_and_transform())

            if get_filename(file) == 'sales_order':
                importer.import_data('busy_sales_order', excel_data.clean_and_transform())

            if get_filename(file) == 'material_issued_to_party':
                importer.import_data('busy_mitp', excel_data.clean_and_transform())
                
            if get_filename(file) == 'material_received_from_party':
                importer.import_data('busy_mrfp', excel_data.clean_and_transform())

            if get_filename(file) == "master_accounts" and get_compname(file) == "comp0005":
                importer.import_data('busy_acc_kbbio', excel_data.clean_and_transform())

            if get_filename(file) == "master_accounts" and get_compname(file) == "comp0010":
                importer.import_data('busy_acc_agri', excel_data.clean_and_transform())

            if get_filename(file) == "master_accounts" and get_compname(file) == "comp0011":
                importer.import_data('busy_acc_greenera', excel_data.clean_and_transform())

            if get_filename(file) == "master_accounts" and get_compname(file) == "comp0014":
                importer.import_data('busy_acc_newage', excel_data.clean_and_transform())
            
            if get_filename(file) == "master_accounts" and get_compname(file) == "comp0015":
                importer.import_data('busy_acc_100x', excel_data.clean_and_transform())

            if get_filename(file) == "items" and get_compname(file) == "comp0005":
                importer.import_data('busy_items_kbbio', excel_data.clean_and_transform())

            if get_filename(file) == "items" and get_compname(file) == "comp0015":
                importer.import_data('busy_items_100x', excel_data.clean_and_transform())

            if get_filename(file) == "items" and get_compname(file) == "comp0011":
                importer.import_data('busy_items_greenera', excel_data.clean_and_transform())

            if get_filename(file) == "items" and get_compname(file) == "comp0014":
                importer.import_data('busy_items_newage', excel_data.clean_and_transform())
            
            if get_filename(file) == "items" and get_compname(file) == "comp0010":
                importer.import_data('busy_items_agri', excel_data.clean_and_transform())

        else:
            logger.error(f"{get_filename(file)} and {get_compname(file)} of {file} didn't match the criteria")    

    else:
        logger.critical("No File for today's date found to import in database")            



# def test():
#     Base.metadata.create_all(db_engine)
#     file = r"D:\automated_busy_downloads\comp0005\master_accounts\comp0005_master_accounts_02-May-2024.xlsx"
#     excel_data = ExcelProcessor(file)
#     #print(get_filename(file))
#     importer = DatabaseCrud(db_connector)
#     #importer.import_data("busy_items_kbbio", excel_data.clean_and_transform())
#     if get_filename(file) == "master_accounts" and get_compname(file) == "comp0005":
#         #print(get_filename(file), get_compname(file))
#         importer.import_data('busy_acc_kbbio', excel_data.clean_and_transform())