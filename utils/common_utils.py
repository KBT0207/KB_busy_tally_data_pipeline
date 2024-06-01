"""This module contain functions that will used as helper/common functions in the report modules 
"""
import psutil


def is_process_running(process_name:str) -> bool:
    """This method will check whether a specific process is running or not.

    Args:
        process_name (_type_): Name of the process which you want to check it is running or not.

    Returns:
        _type_: Returns True if provided process_name is already running.
                Returns False if provided process_name is not running. 
    """
    for process in psutil.process_iter():
        if process.name().lower() == process_name.lower():
            return True
    return False



from database.models.busy_models.busy_reports import (SalesKBBIO, SalesReturnKBBIO, 
                                        SalesOrderKBBIO, MITPKBBIO, MRFPKBBIO,
                                        )
from database.models.busy_models.busy_accounts import (BusyAccountsKBBIO, 
                                        BusyAccounts100x, BusyAccountsAgri,
                                        BusyAccountsGreenEra, BusyAccountsNewAge,
                                        )
from database.models.busy_models.busy_items import (BusyItemsKBBIO, 
                                        BusyItems100x, BusyItemsGreenEra,
                                        BusyItemsAgri, BusyItemsNewAge,
                                        )
from database.models.tally_models.tally_report_models import (TallySales, TallyPurchase,
                                        TallyPurchaseReturn, TallySalesReturn,
                                        TallyPayment, TallyReceipts , TallyJournal, 
                                        TallyAccounts, TallyOutstandingBalance, TestTable, 
                                        )
from database.models.busy_models.busy_pricing import (BusyPricingKBBIO,
                                        )


busy_tables = {'busy_sales': SalesKBBIO, 'busy_sales_order': SalesOrderKBBIO,
          'busy_sales_return': SalesReturnKBBIO, "busy_mitp": MITPKBBIO,
          "busy_mrfp": MRFPKBBIO, 
          "busy_acc_kbbio": BusyAccountsKBBIO,
          "busy_acc_100x": BusyAccounts100x, "busy_acc_agri": BusyAccountsAgri,
          "busy_acc_greenera": BusyAccountsGreenEra, "busy_acc_newage": BusyAccountsNewAge,
          "busy_items_kbbio": BusyItemsKBBIO, "busy_items_100x": BusyItems100x, 
          "busy_items_agri": BusyItemsAgri, "busy_items_greenera": BusyItemsGreenEra, 
          "busy_items_newage": BusyItemsNewAge,
        }


tally_tables = {"tally_sales": TallySales, "tally_sales_return": TallySalesReturn, 
                "tally_purchase": TallyPurchase, "tally_purchase_return": TallyPurchaseReturn, 
                "tally_payments": TallyPayment, "tally_receipts": TallyReceipts, "tally_journal": TallyJournal, 
                "tally_accounts": TallyAccounts, "outstanding_balance": TallyOutstandingBalance,
               }



other_tables = {"busy_pricing_kbbio": BusyPricingKBBIO, "test_table": TestTable,
               }


tables = {**busy_tables, **tally_tables, **other_tables}


tally_reports = {
                's': 'sales', 'e': 'sales_return', 'p': "purchase" , 'd': 'purchase_return',
                'y': "payments", 'r': 'receipts', 'j': 'journal',
                }
        

tally_comp_codes = {
                    10001: "Pune",
                    10002: "Pune" , 
                    10003: "Indore", 
                    10004: "Jejuri", 
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
                    10018: "100x Phaltan", 
                    10019: "Jaipur", 
                    10020: "Khorda", 
                    10021: "AS Phaltan", 
                    10022: "Bhatinda",
                    10023: "NA Hubli", 
                    # 20000: "Phaltan",  
                    20001: "Phaltan", 
                    # 91820: "Phaltan",
                    }


acc_comp_codes = {
                    10001: "Pune",
                    10002: "Baner" , 
                    10003: "Indore", 
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
                    10019: "Jaipur", 
                    10020: "Khorda", 
                    10021: "AS Phaltan", 
                    10022: "Bhatinda",
                    10023: "NA Hubli", 
                    20001: "Phaltan", 
                    }


