import pandas as pd
import numpy as np
from logging_config import logger
from Database.busy_data_processor import get_compname, get_filename, get_date
from utils.common_utils import tally_comp_codes, acc_comp_codes, balance_comp_codes, receivables_comp_codes

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
    df["particulars"] = df["particulars"].str.replace('\n', '', regex=True).str.replace('_x000D_', '', regex=True)
    df["voucher_no"] = df["voucher_no"].str.replace('\n', '', regex=True).str.replace('_x000D_', '', regex=True)

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
    df["particulars"] = df["particulars"].str.replace('\n', '', regex=True).str.replace('_x000D_', '', regex=True)
    df["voucher_no"] = df["voucher_no"].str.replace('\n', '', regex=True).str.replace('_x000D_', '', regex=True)
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

    df["alias_code"] = df["ledger_name"].str.extract(pat= r'\(([^()]*?/[^()]*?)\)')
    df["alias_code"] = df["alias_code"].str.replace('\n', '', regex=True).str.replace('_x000D_', '', regex=True)

    df["ledger_name"] = df["ledger_name"].str.replace(r'\([^()]*?/[^()]*?\)$', '', regex= True).str.rstrip()
    df["ledger_name"] = df["ledger_name"].str.replace('\n', '', regex=True).str.replace('_x000D_', '', regex=True)

    df["under"] = df["under"].str.replace('\n', '', regex=True).str.replace('_x000D_', '', regex=True)
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

    df["item_name"] = df["item_name"].str.replace('\n', '', regex=True).str.replace('_x000D_', '', regex=True)
    df["under"] = df["under"].str.replace('\n', '', regex=True).str.replace('_x000D_', '', regex=True)
    df["under"] = df["under"].replace('_x0004_','', regex=True)
    df.loc[:,['opening_qty', 'rate', 'opening_balance']] = df.loc[:,['opening_qty', 'rate', 'opening_balance']].fillna(0)
    
    return df



def apply_outstanding_balance_transformation(file_path, material_centre_name) -> pd.DataFrame:
    try:
        df = pd.read_excel(file_path, header=None, skipfooter=1)
        credit_index = df.loc[df.eq('Credit').any(axis=1)].index[0]
        df = df.drop(range(credit_index)).reset_index(drop=True)
        df.columns = df.iloc[0]
        df = df.iloc[1:].reset_index(drop=True)

    except FileNotFoundError as e:
        logger.warning(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None
    df.columns = df.columns.str.lower()
    mc_name = balance_comp_codes[int(material_centre_name)]

    df = df.rename(columns={np.nan: "particulars"})
    df["date"] = get_date(path=file_path)
    df['date'] = pd.to_datetime(df['date'].str.removesuffix('.xlsx'), dayfirst=True)
    df["material_centre"] = mc_name

    df["particulars"] = df["particulars"].str.replace('\n', '', regex=True).str.replace('_x000D_', '', regex=True)
    df.loc[:, ["credit", "debit"]] = df[["credit", "debit"]].fillna(0)

    return df



def apply_receivables_transformation(file_path, material_centre_name) -> pd.DataFrame:
    try:
        df = pd.read_excel(file_path, header=None, skipfooter=1)
        date_index = df.loc[df.eq('Date').any(axis=1)].index[0]
        df = df.drop(range(date_index)).reset_index(drop=True)
        df.columns = df.iloc[0]
        df = df.drop(index=0)
        df = df.iloc[1:].reset_index(drop=True)
        
    except FileNotFoundError as e:
        logger.warning(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")
    mc_name = receivables_comp_codes[int(material_centre_name)]

    df = df.rename(columns={'date': 'voucher_date', 'ref_no': 'voucher_no', 
                            "party's_name": "particulars", 'opening': 'opening_amt', 
                            'pending': 'pending_amt', 'due_on': 'due_date', 
                            'overdue': 'overdue_days', 
                            })
    df["date"] = get_date(path=file_path)
    df['date'] = df['date'].str.removesuffix('.xlsx')
    date_columns = ['date', 'voucher_date', 'due_date']
    for col in date_columns:
         df[col] = pd.to_datetime(df[col], dayfirst=True)

    df["material_centre"] = mc_name

    df["particulars"] = df["particulars"].str.replace('\n', '', regex=True).str.replace('_x000D_', '', regex=True)
    df["voucher_no"] = df["voucher_no"].str.replace('\n', '', regex=True).str.replace('_x000D_', '', regex=True)

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

        elif report_type == "outstanding":
            df = apply_outstanding_balance_transformation(file_path=self.excel_file_path, material_centre_name=company_code)

        elif report_type == "receivables":
            df = apply_receivables_transformation(file_path=self.excel_file_path, material_centre_name=company_code)
        
        if df is None:
            logger.error("Dataframe is None!")
            return None

        return df


