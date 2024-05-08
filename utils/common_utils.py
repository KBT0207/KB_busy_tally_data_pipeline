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



from database.models.busy_models.busy_reports_models import (SalesKBBIO, SalesReturnKBBIO, 
                                        SalesOrderKBBIO, MITPKBBIO, MRFPKBBIO,
                                        )
from database.models.busy_models.busy_accounts_models import (BusyAccountsKBBIO, 
                                        BusyAccounts100x, BusyAccountsAgri,
                                        BusyAccountsGreenEra, BusyAccountsNewAge,
                                        )
from database.models.busy_models.busy_items_models import (BusyItemsKBBIO, 
                                        BusyItems100x, BusyItemsGreenEra,
                                        BusyItemsAgri, BusyItemsNewAge,
                                        )
from database.models.tally_models.tally_report_models import (TallySales, TallyPurchase,
                                        TallyPurchaseReturn, TallySalesReturn,
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
          "tally_sales": TallySales, "tally_sales_return": TallySalesReturn, 
          "tally_purchase": TallyPurchase, "tally_purchase_return": TallyPurchaseReturn, 
        }



tally_tables = {"tally_sales": TallySales, "tally_sales_return": TallySalesReturn, 
          "tally_purchase": TallyPurchase, "tally_purchase_return": TallyPurchaseReturn, 
        }


tables = {**busy_tables, **tally_tables}


tally_reports = {
     's': 'sales', 'e': 'sales_return',
                 'p': "purchase" ,
                 'd': 'purchase_return',
                }
        

tally_comp_codes = {
    10009: "Vijaywada", 
    10002: "Pune" , 
                    10008: "Raipur", 
                    10010: "Ahmedabad", 10016: "Karnal", 10004: "Jejuri", 
                    10007: "Hubli", 10003: "Indore", 10020: "Khorda", 
                    91820: "Phaltan", 
                    10001: "Pune", 
                    10022: "Bhatinda",
                    10019: "Jaipur", 10011: "Hyderabad", 10012: "Lucknow", 
                    10018: "Phaltan", 10017: "Phaltan", 
                    10005: "Nashik", 
                    10023: "Hubli", 10014: "Phaltan", 10021: "AS Phaltan",                 
                    }


# tally_comp_codes = {10005: "Nashik", 
#                     10023: "Hubli", 10014: "Phaltan", 10021: "AS Phaltan",}