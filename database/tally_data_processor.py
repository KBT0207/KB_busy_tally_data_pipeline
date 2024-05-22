import pandas as pd
import numpy as np
from logging_config import logger
from database.busy_data_processor import get_compname, get_filename
from utils.common_utils import tally_comp_codes, acc_comp_codes

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
    df["voucher_no"] = df["voucher_no"].replace("_x000D_\\n", "", regex=True)

    df["voucher_no"] = df["voucher_no"].fillna(df["particulars"])
    df = df.loc[~df["particulars"].isna()]

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
    
    df["material_centre"] = mc_name
    df["particulars"] = df["particulars"].str.rstrip().str.rstrip("_x000D_")
    df["voucher_no"] = df["voucher_no"].replace("_x000D_\\n", "", regex=True)
    df.loc[:,["date",'voucher_no']] = df.loc[:,["date",'voucher_no']].ffill()
    df['date'] = pd.to_datetime(df["date"])
    df.loc[:,['credit', 'debit']] = df.loc[:,['credit', 'debit']].fillna(0)
    
    df['amount'] = np.where((df['credit'] != 0), df['credit'], df['debit'])
    df['amount'] = np.where((df['debit'] != 0), df['debit'], df['amount'])

    df["amount_type"] = np.where(df['credit'] != 0, 'credit', 'debit')
    df = df.drop(columns= ["vch_type", "debit", "credit"])
    df['particulars'] = np.where(df['particulars'] == "(cancelled)", "Cancelled", df['particulars'])
    df = df[['date', 'particulars', 'voucher_no','material_centre', 'amount', 'amount_type', ]]
    df = df.loc[~df["particulars"].isna()]

    return df



def apply_accounts_transformation(file_path, material_centre_name) -> pd.DataFrame:
    try:
        df = pd.read_excel(file_path, header=None)
        header_row = df[df.iloc[:, 0] == 'Sl. No.'].index[0]
        df = df.iloc[header_row:].reset_index(drop=True)
        df.columns = df.iloc[0]
        df = df.iloc[1:]
    except FileNotFoundError as e:
        print(e)
        logger.warning(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")
    mc_name = acc_comp_codes[int(material_centre_name)]
    df = df.drop(columns="sl_no", axis='columns')
    
    df = df.rename(columns= {"name_of_ledger": "ledger_name", "state_name": "state", 
                             "gstin/un": "gst_no",
                             })

    df["material_centre"] = mc_name
    df["ledger_name"] = df["ledger_name"].replace('_x000D_\\n','', regex=True)
    df["under"] = df["under"].replace('_x000D_\\n','', regex=True)
    # columns_to_na = ['alias_code', 'busy_name', 'dealer_code']
    # for col in columns_to_na:
    #     df[col] = np.where(df[col] == '-', np.nan, df[col])
    df["gst_no"] = df["gst_no"].str.rstrip()
    df["opening_balance"] = df["opening_balance"].fillna(0)
    
    return df



def apply_items_transformation(file_path:str) -> pd.DataFrame:
    try:
        df = pd.read_excel(file_path, header=None)
        header_row = df[df.iloc[:, 0] == 'Sl. No.'].index[0]
        df = df.iloc[header_row:].reset_index(drop=True)
        df.columns = df.iloc[0]
        df = df.iloc[1:]
    except FileNotFoundError as e:
        print(e)
        logger.warning(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")

    df = df.drop(columns="sl_no", axis='columns')
    
    df = df.rename(columns= {"name_of_item": "item_name",
                             })

    df["item_name"] = df["item_name"].replace('_x000D_\\n','', regex=True)
    df["under"] = df["under"].replace('_x000D_\\n','', regex=True)
    df["under"] = df["under"].replace('_x0004_','', regex=True)
    df.loc[:,['opening_qty', 'rate', 'opening_balance']] = df.loc[:,['opening_qty', 'rate', 'opening_balance']].fillna(0)
    
    return df




class TallyDataProcessor:
    def __init__(self, excel_file_path) -> None:
        self.excel_file_path = excel_file_path      

    
    def clean_and_transform(self):
        df = None

        company_code = get_compname(self.excel_file_path)
        report_type = get_filename(self.excel_file_path)
        
        if report_type in ['sales', 'sales_return', 'purchase', 'purchase_return']:
            df = apply_transformation(file_path=self.excel_file_path, material_centre_name=company_code)
        
        elif report_type in ['receipts', 'payments', 'journal']:
            df = apply_register_transformation(file_path=self.excel_file_path, material_centre_name=company_code)
        
        elif report_type == "accounts":
            df = apply_accounts_transformation(file_path=self.excel_file_path, material_centre_name=company_code)

        # elif report_type == "items":
        #     df = apply_items_transformation(file_path=self.excel_file_path)

        if df is None:
            logger.error("Dataframe is None.. Check path variable/value!")
            return None

        return df


