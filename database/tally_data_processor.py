import pandas as pd
import numpy as np
from logging_config import logger
from database.busy_data_processor import get_compname, get_filename
from utils.common_utils import tally_comp_codes

pd.set_option('future.no_silent_downcasting', True)


def apply_transformation(dataframe:pd.DataFrame, material_centre_name) -> pd.DataFrame:
    mc_name = tally_comp_codes[int(material_centre_name)]
    dataframe = dataframe.rename(columns= {"vch_type": "voucher_type", "vch_no": "voucher_no"})

    dataframe.loc[:, ["credit", "debit"]] = dataframe.loc[:, ["credit", "debit"]].fillna(0)

    dataframe["material_centre"] = mc_name
    dataframe["particulars"] = dataframe["particulars"].str.rstrip().str.rstrip("_x000D_")
    dataframe["voucher_no"] = dataframe["voucher_no"].fillna(dataframe["particulars"])

    return dataframe



def apply_register_transformation(dataframe:pd.DataFrame, material_centre_name) -> pd.DataFrame:
    mc_name = tally_comp_codes[int(material_centre_name)]
    
    dataframe = dataframe.rename(columns= {"vch_no": "voucher_no"})
    dataframe = dataframe.dropna(axis=1, how='all')
    dataframe["material_centre"] = mc_name
    dataframe["particulars"] = dataframe["particulars"].str.rstrip().str.rstrip("_x000D_")
    dataframe.loc[:,["date",'voucher_no']] = dataframe.loc[:,["date",'voucher_no']].ffill()
    dataframe['date'] = pd.to_datetime(dataframe["date"])
    dataframe.loc[:,['credit', 'debit']] = dataframe.loc[:,['credit', 'debit']].fillna(0)
    
    dataframe['amount'] = np.where((dataframe['credit'] != 0), dataframe['credit'], dataframe['debit'])
    dataframe['amount'] = np.where((dataframe['debit'] != 0), dataframe['debit'], dataframe['amount'])

    dataframe["amount_type"] = np.where(dataframe['credit'] != 0, 'credit', 'debit')
    dataframe = dataframe.drop(columns= ["vch_type", "debit", "credit"])
    dataframe['particulars'] = np.where(dataframe['particulars'] == "(cancelled)", "Cancelled", dataframe['particulars'])
    
    return dataframe




class TallyDataProcessor:
    def __init__(self, excel_file_path) -> None:
        self.excel_file_path = excel_file_path      

    
    def clean_and_transform(self):
        try:
            excel_df =  pd.read_excel(self.excel_file_path, skipfooter= 1, header=None)
            date_row = excel_df[excel_df.iloc[:, 0] == 'Date'].index[0]
            excel_df = excel_df.iloc[date_row:].reset_index(drop=True)
            excel_df.columns = excel_df.iloc[0]
            excel_df = excel_df.iloc[1:]
            excel_df = excel_df.drop(index=1)
        except FileNotFoundError as e:
            print(e)
            logger.warning(f"Excel File not found in the given {self.excel_file_path}: {e}")
        if excel_df.empty:
            logger.warning(f"Empty Excel File of {get_compname(self.excel_file_path)} and report {get_filename(self.excel_file_path)}")
            return None
        excel_df.columns = excel_df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")
        
        company_code = get_compname(self.excel_file_path)
        report_type = get_filename(self.excel_file_path)
        if report_type in ['s', 'e', 'p', 'd']:
            df = apply_transformation(excel_df, material_centre_name=company_code)
        else:
            df = apply_register_transformation(excel_df, material_centre_name=company_code)

        return df


