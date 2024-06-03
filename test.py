import pandas as pd
import numpy as np
from glob import glob
import os

pd.set_option('future.no_silent_downcasting', True)

balance_comp_codes = {
                    10001: "Pune",
                    10002: "Baner" , 
                    10003: "Indore",
                    # 10004: "Jejuri",
                    10005: "Nashik", 
                    10007: "Hubli",                     
                    10008: "Raipur", 
                    10009: "Vijaywada", 
                    10010: "Ahmedabad", 
                    10011: "Hyderabad", 
                    10012: "Lucknow", 
                    10014: "NA Phaltan", 
                    10016: "Karnal", 
                    10017: "GE Phaltan", 
                    # 10018: "100x Phaltan",
                    10019: "Jaipur", 
                    10020: "Khorda", 
                    10021: "AS Phaltan", 
                    10022: "Bhatinda",
                    10023: "NA Hubli", 
                    20001: "Phaltan", 
                    }


def get_date(path:str):
    return path.split("\\")[-1].split("_")[-1].removesuffix(".xlsx")

def get_mc(path:str):
    mc = balance_comp_codes.get(int(path.split("\\")[-1].split("_")[0]))
    # return print(mc)
    return mc


path = r"D:\automated_tally_downloads\balance_sheet_data"

files = glob(path + '/**/*.xlsx', recursive= True)

def transform(path):
    df = pd.read_excel(path, skipfooter=1)
    # df = pd.read_excel(samp_file)
    credit_index = df.loc[df.eq('Credit').any(axis=1)].index[0]
    df = df.drop(range(credit_index)).reset_index(drop=True)
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)
    df["date"] = pd.to_datetime(get_date(path=path), dayfirst=True)
    df["material_centre"] = get_mc(path=path)
    df.loc[:, ["Credit", "Debit"]] = df[["Credit", "Debit"]].fillna(0)
    df = df.rename(columns= {np.nan: "particulars"})
    df['particulars'] = df["particulars"].replace('_x000D_\\n', '', regex=True)

    df.columns = df.columns.str.lower()

    return df


ea_df = []
for f in files:
    print(f)
    df = transform(path= f)
    ea_df.append(df)

combined = pd.concat(ea_df)
combined.to_excel(r"D:\automated_tally_downloads\balance_sheet_data\Apr24-May24.xlsx")





