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




tally_reports = {'s': 'sales', 'p': "purchase" , 'e': 'sales_return', 
                 'd': 'purchase_return'}
        

