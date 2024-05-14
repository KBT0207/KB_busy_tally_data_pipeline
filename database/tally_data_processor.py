import pandas as pd
import numpy as np
from logging_config import logger
from database.busy_data_processor import get_compname, get_filename
from utils.common_utils import tally_comp_codes

pd.set_option('future.no_silent_downcasting', True)


def apply_transformation(file_path, material_centre_name) -> pd.DataFrame:
    try:
        df = pd.read_excel(file_path, skipfooter= 1, header=None)
        date_row = df[df.iloc[:, 0] == 'Date'].index[0]
        df = df.iloc[date_row:].reset_index(drop=True)
        df.columns = df.iloc[0]
        df = df.iloc[1:]
        df = df.drop(index=1)
    except FileNotFoundError as e:
        print(e)
        logger.warning(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")
    mc_name = tally_comp_codes[int(material_centre_name)]
    df = df.rename(columns= {"vch_type": "voucher_type", "vch_no": "voucher_no"})

    df.loc[:, ["credit", "debit"]] = df.loc[:, ["credit", "debit"]].fillna(0)

    df["material_centre"] = mc_name
    df["particulars"] = df["particulars"].str.rstrip().str.rstrip("_x000D_")
    df["voucher_no"] = df["voucher_no"].fillna(df["particulars"])

    return df



def apply_register_transformation(file_path, material_centre_name) -> pd.DataFrame:
    try:
        df = pd.read_excel(file_path, skipfooter= 1, header=None)
        date_row = df[df.iloc[:, 0] == 'Date'].index[0]
        df = df.iloc[date_row:].reset_index(drop=True)
        df.columns = df.iloc[0]
        df = df.iloc[1:]
        df = df.drop(index=1)
    except FileNotFoundError as e:
        print(e)
        logger.warning(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")
    mc_name = tally_comp_codes[int(material_centre_name)]
    
    df = df.rename(columns= {"vch_no": "voucher_no"})
    df = df.dropna(axis=1, how='all')
    df["material_centre"] = mc_name
    df["particulars"] = df["particulars"].str.rstrip().str.rstrip("_x000D_")
    df.loc[:,["date",'voucher_no']] = df.loc[:,["date",'voucher_no']].ffill()
    df['date'] = pd.to_datetime(df["date"])
    df.loc[:,['credit', 'debit']] = df.loc[:,['credit', 'debit']].fillna(0)
    
    df['amount'] = np.where((df['credit'] != 0), df['credit'], df['debit'])
    df['amount'] = np.where((df['debit'] != 0), df['debit'], df['amount'])

    df["amount_type"] = np.where(df['credit'] != 0, 'credit', 'debit')
    df = df.drop(columns= ["vch_type", "debit", "credit"])
    df['particulars'] = np.where(df['particulars'] == "(cancelled)", "Cancelled", df['particulars'])
    
    return df



def apply_accounts_transformation(file_path, material_centre_name) -> pd.DataFrame:
    try:
        df = pd.read_excel(file_path, header=None)
        header_row = df[df.iloc[:, 0] == 'Sl. No.'].index[0]
        df = df.iloc[header_row:].reset_index(drop=True)
        df.columns = df.iloc[0]
        df = df.iloc[1:]
        df = df.drop(index=1)
    except FileNotFoundError as e:
        print(e)
        logger.warning(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")
    mc_name = tally_comp_codes[int(material_centre_name)]
    df = df.drop(columns="sl_no", axis='columns')
    
    df = df.rename(columns= {"name_of_ledger": "ledger_name", "state_name": "state", 
                             "gstin/un": "gst_no",
                             })

    df["material_centre"] = mc_name
    df["ledger_name"] = df["ledger_name"].str.rstrip().str.rstrip("_x000D_")
    df["alias_code"] = np.where(df["alias_code"] == '-', np.nan, df["alias_code"])
    # dataframe.loc[:,["date",'voucher_no']] = dataframe.loc[:,["date",'voucher_no']].ffill()
    # dataframe['date'] = pd.to_datetime(dataframe["date"])
    # dataframe.loc[:,['credit', 'debit']] = dataframe.loc[:,['credit', 'debit']].fillna(0)
    
    # dataframe['amount'] = np.where((dataframe['credit'] != 0), dataframe['credit'], dataframe['debit'])
    # dataframe['amount'] = np.where((dataframe['debit'] != 0), dataframe['debit'], dataframe['amount'])

    # dataframe["amount_type"] = np.where(dataframe['credit'] != 0, 'credit', 'debit')
    # dataframe = dataframe.drop(columns= ["vch_type", "debit", "credit"])
    # dataframe['particulars'] = np.where(dataframe['particulars'] == "(cancelled)", "Cancelled", dataframe['particulars'])
    
    return df




class TallyDataProcessor:
    def __init__(self, excel_file_path) -> None:
        self.excel_file_path = excel_file_path      

    
    def clean_and_transform(self):
        
        company_code = get_compname(self.excel_file_path)
        report_type = get_filename(self.excel_file_path)
        if report_type in ['s', 'e', 'p', 'd']:
            df = apply_transformation(file_path=self.excel_file_path, material_centre_name=company_code)
        elif report_type in ['r', 'y', 'j']:
            df = apply_register_transformation(file_path=self.excel_file_path, material_centre_name=company_code)
        else:
            df = apply_accounts_transformation(file_path=self.excel_file_path, material_centre_name=company_code)

        return df


