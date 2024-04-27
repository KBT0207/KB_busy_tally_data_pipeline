import glob
from datetime import datetime, timedelta
from database.sql_connector import db_engine, db_connector
from database.excel_cleanup import ExcelProcessor, get_filename
from database.models import Base
from database.db_import import ImportExcel



def main_sql():    
    Base.metadata.create_all(db_engine)
    
    # file = r"D:\automated_busy_downloads\comp0014\material_received_from_party\comp0014_material_received_from_party_25-Apr-2024.xlsx"
    # excel_data = ExcelProcessor(file)
    # print(get_compname(file))
    # print(excel_data.clean_and_transform())
    current_date = datetime.today().date()
    date1 = current_date - timedelta(days=1)
    date2 = current_date - timedelta(days=2)

    importer = ImportExcel(db_connector)
    importer.delete_date_query("busy_sales", date1, date2)
    # importer.import_data('busy_mitp', excel_data.clean_and_transform(top_rows=5))
    
    todays_date = datetime.today().strftime("%d-%b-%Y")
    busy_files = glob.glob("D:\\automated_busy_downloads\\" + f"**\\*{todays_date}.xlsx", recursive=True)

    for file in busy_files:
        if get_filename(file) == 'sales':
            excel_data = ExcelProcessor(file)
            importer = ImportExcel(db_connector)
            importer.import_data('busy_sales', excel_data.clean_and_transform())
        if get_filename(file) == 'sales_return':
            excel_data = ExcelProcessor(file)
            importer = ImportExcel(db_connector)
            importer.import_data('busy_sales_return', excel_data.clean_and_transform())
        if get_filename(file) == 'sales_order':
            excel_data = ExcelProcessor(file)
            importer = ImportExcel(db_connector)
            importer.import_data('busy_sales_order', excel_data.clean_and_transform())
        if get_filename(file) == 'material_issued_to_party':
            excel_data = ExcelProcessor(file)
            importer = ImportExcel(db_connector)
            importer.import_data('busy_mitp', excel_data.clean_and_transform())
        if get_filename(file) == 'material_received_from_party':
            excel_data = ExcelProcessor(file)
            importer = ImportExcel(db_connector)
            importer.import_data('busy_mrfp', excel_data.clean_and_transform())
        

