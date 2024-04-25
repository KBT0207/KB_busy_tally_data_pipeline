from sqlalchemy.ext.declarative import declarative_base
from database.sql_connector import db_engine
from database.excel_cleanup import ExcelProcessor
from database.models import metadata, base


def main_sql():    

    base.metadata = metadata
    base.metadata.create_all(db_engine)

    # file_path = r'D:\automated_busy_downloads\comp0005\material_issued_to_party\comp0005_material_issued_to_party_22-Apr-2024.xlsx'
    # excel_data = ExcelProcessor(file_path)
    # excel_data.clean_and_transform()
    # print(excel_data.clean_and_transform())
