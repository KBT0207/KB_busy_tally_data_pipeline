import pandas as pd
from logging_config import logger


def get_filename(path:str):
    return path.split("\\")[-1].split("_", maxsplit=1)[-1].rsplit("_", 1)[:-1][0]


def get_compname(path:str):
    return path.split("\\")[-1].split("_")[0]


def get_date(path:str):
    return path.split("\\")[-1].split("_")[-1]



def apply_sales_transformation(file_path:str, top_row:int) -> pd.DataFrame:
    try:
        df =  pd.read_excel(file_path,skiprows= top_row, skipfooter= 2)
    except FileNotFoundError as e:
        logger.warning(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None
    
    columns_ffill = ["Date", "Vch/Bill No", "Party Type", "Material Centre", "Particulars", "State"]
    df.loc[:, columns_ffill] = df[columns_ffill].ffill()

    columns_fillna_with_0 = ["Disc %", "Discount Amt", "Tax Amt", "Bill Amount"]
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
    
    # df['main_price'] = df['main_price'].fillna(0)
    # df['alt_price'] = df['alt_price'].fillna(0)
    # df['mrp'] = df['mrp'].fillna(0)
    # df['amount'] = df['amount'].fillna(0)


    return df



def apply_sales_order_transformation(file_path:str, top_row:int) -> pd.DataFrame:
    try:
        df =  pd.read_excel(file_path,skiprows= top_row, skipfooter= 2)
    except FileNotFoundError as e:
        logger.warning(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None
    
    columns_ffill = ["Date", "Vch/Bill No", "Particulars", "Material Centre"]
    df.loc[:, columns_ffill] = df[columns_ffill].ffill()

    columns_fillna_with_0 = ["Tax", "Order Total"]
    df.loc[:,columns_fillna_with_0] = df[columns_fillna_with_0].fillna(0)
    
    columns_conditional_ffill = ["Salesman", "Salesman ID",
                                    ]
    
    for column in columns_conditional_ffill:
        vch_to_dc = df[["Vch/Bill No", column]].dropna().set_index('Vch/Bill No')[column].to_dict()
        df.loc[:, column] = df['Vch/Bill No'].map(vch_to_dc)

    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")
    df = df.rename(columns= {"vch/bill_no": "voucher_no", "qty": "main_qty", 
                             "unit": "main_unit", "price": "main_price",
                             "qty1": "alt_qty", "unit1": "alt_unit", "price1": "alt_price", 
                             "order_total": "order_amt", "tax": "tax_amt",
                             })

    return df    



def apply_sales_return_transformation(file_path:str, top_row:int) -> pd.DataFrame:
    try:
        df =  pd.read_excel(file_path,skiprows= top_row, skipfooter= 2)
    except FileNotFoundError as e:
        logger.warning(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None
    
    columns_ffill = ["Date", "Vch/Bill No", "Party Type", "State", "Material Centre", "Particulars", ]
    df.loc[:, columns_ffill] = df[columns_ffill].ffill()

    columns_fillna_with_0 = ["Disc %", "Disc Amt", "Tax Amount", "Price", "Amount", "Bill Amount", "MRP"]
    df.loc[:,columns_fillna_with_0] = df[columns_fillna_with_0].fillna(0)

    columns_conditional_ffill = ["Dealer Code", "TIN/GSTIN No.",
                                "GRN No", "GRN Date", 
                                "E-Invoice", "Salesman",
                                "SO No.", "SO Date.", 
                                "E-Way Bill No.", "Narration"]
    
    for column in columns_conditional_ffill:
        vch_to_dc = df[["Vch/Bill No", column]].dropna().set_index('Vch/Bill No')[column].to_dict()
        df.loc[:, column] = df['Vch/Bill No'].map(vch_to_dc)
    
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")
    df = df.rename(columns= {"vch/bill_no": "voucher_no", "tin/gstin_no": "gst_no",
                             "qty": "main_qty", "unit": "main_unit", "price": "main_price",
                             "qty1": "alt_qty", "unit1": "alt_unit", "price1": "alt_price", 
                             "disc_%": "discount_perc", "bill_amount": "bill_amt",
                             "so_no": "sales_order_no" ,"so_date": "sales_order_date",
                             "disc_amt": "discount_amt", "tax_amount": "tax_amt",
                             "e-invoice": "e_invoice", "e-way_bill_no": "e_way_bill",
                             })

    df["mfg_date"] = pd.to_datetime(df["mfg_date"]).dt.strftime("%b-%Y")
    df["exp_date"] = pd.to_datetime(df["exp_date"]).dt.strftime("%b-%Y")
    
    # df["main_qty"] = df["main_qty"].fillna(0)
    # df["alt_qty"] = df["alt_qty"].fillna(0)
    # df["alt_price"] = df["alt_price"].fillna(0)

    return df



def apply_material_issued_to_party_transformation(file_path:str, top_row:int) -> pd.DataFrame:
    try:
        df =  pd.read_excel(file_path, skiprows= top_row, skipfooter= 2)
    except FileNotFoundError as e:
        logger.warning(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None
    
    columns_ffill = ["Date", "Vch/Bill No", "Account Group", "Particulars", "Material Centre"]
    df.loc[:, columns_ffill] = df[columns_ffill].ffill()
    
    columns_fillna_with_0 = ["Price", "Amount", "CGST AMT", "SGST AMT", "IGST AMT"]
    df.loc[:,columns_fillna_with_0] = df[columns_fillna_with_0].fillna(0)
    
    columns_conditional_ffill = ["Salesman", "Sales Order No", "Territory", 
                                 "Narration", "Transporter"]
    
    for column in columns_conditional_ffill:
        vch_to_dc = df[["Vch/Bill No", column]].dropna().set_index('Vch/Bill No')[column].to_dict()
        df.loc[:, column] = df['Vch/Bill No'].map(vch_to_dc)
    
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")
    df = df.rename(columns= {"vch/bill_no": "voucher_no", "account_group": "party_type",
                             "qty": "main_qty", "unit": "main_unit", "price": "main_price",
                             "qty1": "alt_qty", "unit1": "alt_unit", "price1": "alt_price", 
                             })
    df["alt_price"] = df["alt_price"].fillna(0)

    df["mfg_date"] = pd.to_datetime(df["mfg_date"]).dt.strftime("%b-%Y")
    df["exp_date"] = pd.to_datetime(df["exp_date"]).dt.strftime("%b-%Y")

    return df



def apply_material_received_from_party_transformation(file_path:str, top_row:int) -> pd.DataFrame:
    try:
        df =  pd.read_excel(file_path,skiprows= top_row, skipfooter= 2)
    except FileNotFoundError as e:
        logger.warning(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None
    
    columns_ffill = ["Date", "Vch/Bill No", "Particulars", "Material Centre"]
    df.loc[:, columns_ffill] = df[columns_ffill].ffill()

    columns_fillna_with_0 = ["Price", "Amount", "CGST", "SGST", "IGST"]
    df.loc[:,columns_fillna_with_0] = df[columns_fillna_with_0].fillna(0)
    
    columns_conditional_ffill = ["Narration"]
    
    for column in columns_conditional_ffill:
        vch_to_dc = df[["Vch/Bill No", column]].dropna().set_index('Vch/Bill No')[column].to_dict()
        df.loc[:, column] = df['Vch/Bill No'].map(vch_to_dc)
    
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")
    df = df.rename(columns= {"vch/bill_no": "voucher_no", "qty": "main_qty", 
                             "unit": "main_unit", "price": "main_price",
                             "qty1": "alt_qty", "unit1": "alt_unit", "price1": "alt_price", 
                             "cgst": "cgst_amt", "sgst": "sgst_amt", "igst": "igst_amt",
                             })
    df["alt_price"] = df["alt_price"].fillna(0)

    df["mfg_date"] = pd.to_datetime(df["mfg_date"]).dt.strftime("%b-%Y")
    df["exp_date"] = pd.to_datetime(df["exp_date"]).dt.strftime("%b-%Y")

    return df



def apply_accounts_transformation(file_path:str, top_row:int) -> pd.DataFrame:
    try:
        df =  pd.read_excel(file_path,skiprows= top_row, skipfooter= 2)
    except FileNotFoundError as e:
        logger.error(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None
    df = df.drop(columns= "Created Date")

    columns_fillna_with_0 = ["Op. Bal.(Dr)", "Op. Bal.(Cr)", "Credit Limit"]
    df.loc[:,columns_fillna_with_0] = df[columns_fillna_with_0].fillna(0)

    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")
    df = df.rename(columns= {"op_bal(cr)": "opening_balance_debit", 
                             "op_bal(dr)": "opening_balance_credit", 
                             "type_of_dealer": "dealer_type", "gstin": "gst_no",
                             "addline1": "address1", "addline2": "address2",
                            })
    
    return df



def apply_stock_transfer_transformation(file_path:str, top_row:int) -> pd.DataFrame:
    try:
        df =  pd.read_excel(file_path, skiprows= top_row, skipfooter= 2)
    except FileNotFoundError as e:
        logger.warning(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None
    
    columns_ffill = ["Date", "Vch/Bill No", "From", "To"]
    df.loc[:, columns_ffill] = df[columns_ffill].ffill()
    
    
    columns_conditional_ffill = ["Transporter"]
    
    for column in columns_conditional_ffill:
        vch_to_dc = df[["Vch/Bill No", column]].dropna().set_index('Vch/Bill No')[column].to_dict()
        df.loc[:, column] = df['Vch/Bill No'].map(vch_to_dc)
    
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")
    df = df.rename(columns= {"vch/bill_no": "voucher_no", "from": "material_from", "to": "material_to", 
                             "qty": "main_qty", "unit": "main_unit", "price": "main_price",
                             "qty1": "alt_qty", "unit1": "alt_unit", "price1": "alt_price", 
                             })
    
    columns_fillna_with_0 = ["main_qty", "alt_qty", "main_price", "alt_price", "amount"]
    df.loc[:,columns_fillna_with_0] = df[columns_fillna_with_0].fillna(0)

    df["mfg_date"] = pd.to_datetime(df["mfg_date"]).dt.strftime("%b-%Y")
    df["exp_date"] = pd.to_datetime(df["exp_date"]).dt.strftime("%b-%Y")

    return df



def apply_production_transformation(file_path:str, top_row:int) -> pd.DataFrame:
    try:
        df =  pd.read_excel(file_path, skiprows= top_row, skipfooter= 2)
    except FileNotFoundError as e:
        logger.warning(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None
    
    columns_ffill = ["Date", "Vch/Bill No", "Material Centre"]
    df.loc[:, columns_ffill] = df[columns_ffill].ffill()
    
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")
    df = df.rename(columns= {"vch/bill_no": "voucher_no", "qty_generated": "generated_qty", "unit_main": "generated_unit", 
                             "price": "generated_price", "amount": "generated_amount", 
                             "qty_consumed": "consumed_qty", "unit_main1": "consumed_unit", "price2": "consumed_price", 
                             "amount1": "consumed_amount", 
                             })
    
    df = df.drop(columns= ["qty_generated1", "unit_alt", "price1", "qty_consumed1", "unit_alt1", "price3"])

    columns_fillna_with_0 = ["generated_qty", "generated_price", "generated_amount", "batch_qty", "consumed_price", "consumed_amount"]
    df.loc[:,columns_fillna_with_0] = df[columns_fillna_with_0].fillna(0)

    df["mfg_date"] = pd.to_datetime(df["mfg_date"]).dt.strftime("%b-%Y")
    df["exp_date"] = pd.to_datetime(df["exp_date"]).dt.strftime("%b-%Y")

    return df




def apply_stock_journal_transformation(file_path:str, top_row:int) -> pd.DataFrame:
    try:
        df =  pd.read_excel(file_path, skiprows= top_row, skipfooter= 2)
    except FileNotFoundError as e:
        logger.warning(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None
    
    columns_ffill = ["Date", "Vch/Bill No", "Material Centre"]
    df.loc[:, columns_ffill] = df[columns_ffill].ffill()
    
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")
    df = df.rename(columns= {"vch/bill_no": "voucher_no", "qty_generated": "generated_qty", "unit_main": "generated_unit", 
                             "price": "generated_price", "amount": "generated_amount", 
                             "qty_consumed": "consumed_qty", "unit_main1": "consumed_unit", "price2": "consumed_price", 
                             "amount1": "consumed_amount", 
                             })
    
    df = df.drop(columns= ["qty_generated1", "unit_alt", "price1", "qty_consumed1", "unit_alt1", "price3"])

    columns_fillna_with_0 = ["generated_qty", "generated_price", "generated_amount", "consumed_price", "consumed_amount"]
    df.loc[:,columns_fillna_with_0] = df[columns_fillna_with_0].fillna(0)

    df["mfg_date"] = pd.to_datetime(df["mfg_date"]).dt.strftime("%b-%Y")
    df["exp_date"] = pd.to_datetime(df["exp_date"]).dt.strftime("%b-%Y")

    return df




def apply_items_transformation(file_path:str, top_row:int) -> pd.DataFrame:
    try:
        df =  pd.read_excel(file_path,skiprows= top_row, skipfooter= 2)
    except FileNotFoundError as e:
        logger.error(f"Excel File not found in the given {file_path}: {e}")
    if df.empty:
        logger.warning(f"Empty Excel File of {get_compname(file_path)} and report {get_filename(file_path)}")
        return None

    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(".", "")
    df = df.rename(columns= {"op_stock": "opening_stock"})
    
    if "<<---None--->>" in df["tax_category"].values:
        df["tax_category"] = df["tax_category"].replace("<<---None--->>", "None")

    return df


class BusyDataProcessor:
    def __init__(self, excel_file_path) -> None:
        self.excel_file_path = excel_file_path

    def clean_and_transform(self): 
        if get_filename(self.excel_file_path) == "sales" and get_compname(self.excel_file_path) != "comp0014" :
            df = apply_sales_transformation(self.excel_file_path, top_row=3)

        if get_filename(self.excel_file_path) == "sales" and get_compname(self.excel_file_path) == "comp0014" :
            df = apply_sales_transformation(self.excel_file_path, top_row=5)

        if get_filename(self.excel_file_path) == "sales_return" and get_compname(self.excel_file_path) != "comp0014" :
            df = apply_sales_return_transformation(self.excel_file_path, top_row= 3)

        if get_filename(self.excel_file_path) == "sales_return" and get_compname(self.excel_file_path) == "comp0014" :
            df = apply_sales_return_transformation(self.excel_file_path, top_row= 5)

        if get_filename(self.excel_file_path) == "sales_order" :
            df = apply_sales_order_transformation(self.excel_file_path, top_row= 3)

        if get_filename(self.excel_file_path) == "material_issued_to_party" and get_compname(self.excel_file_path) != "comp0014" :
            df = apply_material_issued_to_party_transformation(self.excel_file_path, top_row= 3)

        if get_filename(self.excel_file_path) == "material_issued_to_party" and get_compname(self.excel_file_path) == "comp0014" :
            df = apply_material_issued_to_party_transformation(self.excel_file_path, top_row= 5)

        if get_filename(self.excel_file_path) == "material_received_from_party" and get_compname(self.excel_file_path) != "comp0014" :
            df = apply_material_received_from_party_transformation(self.excel_file_path, top_row=3)

        if get_filename(self.excel_file_path) == "material_received_from_party" and get_compname(self.excel_file_path) == "comp0014" :
            df = apply_material_received_from_party_transformation(self.excel_file_path, top_row= 5)

        if get_filename(self.excel_file_path) == "master_accounts" and get_compname(self.excel_file_path) != "comp0014":
            df = apply_accounts_transformation(self.excel_file_path, top_row=2)

        if get_filename(self.excel_file_path) == "master_accounts" and get_compname(self.excel_file_path) == "comp0014":
            df = apply_accounts_transformation(self.excel_file_path, top_row=4)

        if get_filename(self.excel_file_path) == "items" and get_compname(self.excel_file_path) != "comp0014":
            df = apply_items_transformation(self.excel_file_path, top_row=2)

        if get_filename(self.excel_file_path) == "items" and get_compname(self.excel_file_path) == "comp0014":
            df = apply_items_transformation(self.excel_file_path, top_row=4)
        
        if get_filename(self.excel_file_path) == "stock_transfer" and get_compname(self.excel_file_path) != "comp0014":
            df = apply_stock_transfer_transformation(self.excel_file_path, top_row=3)

        if get_filename(self.excel_file_path) == "stock_transfer" and get_compname(self.excel_file_path) == "comp0014":
            df = apply_stock_transfer_transformation(self.excel_file_path, top_row=6)
        
        if get_filename(self.excel_file_path) == "stock_journal" and get_compname(self.excel_file_path) != "comp0014":
            df = apply_stock_journal_transformation(self.excel_file_path, top_row=3)

        if get_filename(self.excel_file_path) == "stock_journal" and get_compname(self.excel_file_path) == "comp0014":
            df = apply_stock_journal_transformation(self.excel_file_path, top_row=6)
        
        if get_filename(self.excel_file_path) == "production" and get_compname(self.excel_file_path) != "comp0014":
            df = apply_production_transformation(self.excel_file_path, top_row=3)

        if get_filename(self.excel_file_path) == "production" and get_compname(self.excel_file_path) == "comp0014":
            df = apply_production_transformation(self.excel_file_path, top_row=6)


        return df
