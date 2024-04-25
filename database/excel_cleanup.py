import pandas as pd
from xlwings import view



def apply_sales_transformation(df:pd.DataFrame):
    df = df.loc[~df["Product Group"].isnull()]

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
    return df



def apply_sales_order_transformation(df:pd.DataFrame):
    df = df.loc[~df["Item Details"].isnull()]

    columns_ffill = ["Date", "Vch/Bill No", "Particulars", "Material Centre"]
    df.loc[:, columns_ffill] = df[columns_ffill].ffill()

    columns_fillna_with_0 = ["Tax", "Order Total"]
    df.loc[:,columns_fillna_with_0] = df[columns_fillna_with_0].fillna(0)
    
    columns_conditional_ffill = ["Salesman", "Salesman ID",
                                    ]
    
    for column in columns_conditional_ffill:
        vch_to_dc = df[["Vch/Bill No", column]].dropna().set_index('Vch/Bill No')[column].to_dict()
        df.loc[:, column] = df['Vch/Bill No'].map(vch_to_dc)
    return df



def apply_sales_return_transformation(df:pd.DataFrame):
    df = df.loc[~df["Product Group"].isnull()]

    columns_ffill = ["Date", "Vch/Bill No", "Party Type", "State", "Material Centre", "Particulars", ]
    df.loc[:, columns_ffill] = df[columns_ffill].ffill()

    columns_fillna_with_0 = ["Disc %", "Disc Amt", "Tax Amount", "Price", "Amount", "Bill Amount"]
    df.loc[:,columns_fillna_with_0] = df[columns_fillna_with_0].fillna(0)
    
    columns_conditional_ffill = ["Dealer Code", "TIN/GSTIN No.",
                                "GRN No", "GRN Date", 
                                "E-Invoice", "Salesman",
                                "SO No.", "SO Date.", 
                                "E-Way Bill No.", "Narration"]
    
    for column in columns_conditional_ffill:
        vch_to_dc = df[["Vch/Bill No", column]].dropna().set_index('Vch/Bill No')[column].to_dict()
        df.loc[:, column] = df['Vch/Bill No'].map(vch_to_dc)
    return df



def apply_material_issued_to_party_transformation(df:pd.DataFrame):
    df = df.loc[~df["Product Group"].isnull()]

    columns_ffill = ["Date", "Vch/Bill No", "Account Group", "Particulars", "Material Centre"]
    df.loc[:, columns_ffill] = df[columns_ffill].ffill()

    columns_fillna_with_0 = ["CGST AMT", "SGST AMT", "IGST AMT"]
    df.loc[:,columns_fillna_with_0] = df[columns_fillna_with_0].fillna(0)
    
    columns_conditional_ffill = ["Salesman", "Sales Order No", "Territory", 
                                 "Narration", "Transporter"]
    
    for column in columns_conditional_ffill:
        vch_to_dc = df[["Vch/Bill No", column]].dropna().set_index('Vch/Bill No')[column].to_dict()
        df.loc[:, column] = df['Vch/Bill No'].map(vch_to_dc)
    return df



def apply_material_received_from_party_transformation(df:pd.DataFrame):
    df = df.loc[~df["Item Details"].isnull()]

    columns_ffill = ["Date", "Vch/Bill No", "Particulars", "Material Centre"]
    df.loc[:, columns_ffill] = df[columns_ffill].ffill()

    columns_fillna_with_0 = ["CGST AMT", "SGST AMT", "IGST AMT"]
    df.loc[:,columns_fillna_with_0] = df[columns_fillna_with_0].fillna(0)
    
    columns_conditional_ffill = ["Salesman", "Sales Order No", "Territory", 
                                 "Narration", "Transporter"]
    
    for column in columns_conditional_ffill:
        vch_to_dc = df[["Vch/Bill No", column]].dropna().set_index('Vch/Bill No')[column].to_dict()
        df.loc[:, column] = df['Vch/Bill No'].map(vch_to_dc)
    return df




class ExcelProcessor:
    def __init__(self, excel_file_path) -> None:
        self.excel_file_path = excel_file_path

    def clean_and_transform(self):
        data = pd.read_excel(self.excel_file_path, skiprows= 3) 
        
        file_name = self.excel_file_path.split("\\")[-1].split("_", maxsplit=1)[-1].rsplit("_", 1)[:-1][0]
        
        if file_name == "sales":
            df = apply_sales_transformation(data)

        if file_name == "sales_order":
            df = apply_sales_order_transformation(data)

        if file_name == "sales_return":
            df = apply_sales_return_transformation(data)

        if file_name == "material_issued_to_party":
            df = apply_material_issued_to_party_transformation(data)

        if file_name == "material_received_from_party":
            df = apply_material_received_from_party_transformation(data)
            
        return df
        