import pandas as pd
from logging_config import logger
from database.busy_data_processor import get_compname, get_filename



def apply_sales_transformation(file_path:str, top_row:int) -> pd.DataFrame:
    try:
        df =  pd.read_excel(file_path,skiprows= top_row, skipfooter= 1)
        df = df.drop(index=0)
    except FileNotFoundError as e:
        logger.warning(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None




class TallyDataProcessor:
    def __init__(self, excel_file_path) -> None:
        self.excel_file_path = excel_file_path

    def clean_and_transform(self): 
        if get_filename(self.excel_file_path) == "sales" and get_compname(self.excel_file_path) != "comp0014" :
            df = apply_sales_transformation(self.excel_file_path, top_row=3)

        if get_filename(self.excel_file_path) == "sales" and get_compname(self.excel_file_path) == "comp0014" :
            df = apply_sales_transformation(self.excel_file_path, top_row=5)

        return df


