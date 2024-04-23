import pandas as pd


class ExcelProcessor:
    def __init__(self, excel_file_path) -> None:
        self.excel_file_path = excel_file_path

    def clean_and_transform(self):
        df = pd.read_excel(self.excel_file)
        return df