import pandas as pd
import numpy as np
from xlwings import view



class ExcelProcessor:
    def __init__(self, excel_file_path) -> None:
        self.excel_file_path = excel_file_path

    def clean_and_transform(self):
        df = pd.read_excel(self.excel_file_path, skiprows= 3) 
        columns_ffill = ["Date", "Vch/Bill No", "Party Type", "Material Centre", "Particulars", "State"]
        df[columns_ffill] = df[columns_ffill].ffill()
        df[["Disc %", "Discount Amt", "Tax Amt", "Bill Amount"]] = df[["Disc %", "Discount Amt", "Tax Amt", "Bill Amount"]].fillna(0)
        
        party_type_changes = df["Vch/Bill No"].eq(df["Vch/Bill No"].shift())
        columns_conditional_ffill = ["Dealer Code", "TIN/GSTIN No.", "DC No", "DC Date", 
                                     "E Invoice", "Salesman", "SALES ORDER NO",
                                     "SALES ORDER DATE", "E WAY BILL", "Transporter Name"]
        df[columns_conditional_ffill] = np.where(party_type_changes, df[columns_conditional_ffill].ffill(), df[columns_conditional_ffill])

        return df
    