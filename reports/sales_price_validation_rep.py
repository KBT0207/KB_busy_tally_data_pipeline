from database.db_crud import DatabaseCrud
from database.sql_connector import db_connector
from logging_config import logger
from utils.email import email_send




def dealer_price_validation_report(from_date, to_date, exceptions):
    
    db_crud = DatabaseCrud(db_connector)
    
    validation_df = db_crud.sales_price_validation(from_date= from_date, to_date= to_date)  
    
    if validation_df is not None:
        counts = len(validation_df)
        validation_df.to_excel(fr"D:\Reports\Price Validation from Month to {to_date}.xlsx")
        
        subject = f"Busy Sales Price Validation Report from Month to {to_date} with {counts} rows of descrepancies"
        body = f"Greetings All,\nKindly find the Busy Sales Price Validation Report attached from Month to {to_date} with {counts} rows of descrepancies.\n In the attached excel, column 'Total Price' is the sum of List Price ('Sales_Price') and 'Discout_Amt' which is the compared with the actual Price List."
        attachment = fr"D:\Reports\Price Validation from Month to {to_date}.xlsx"
        logger.info(f"Busy Sales Price Validation Report Exported to Excel with Descrepencies")

    else:
        subject = f"Busy Sales Price Validation Report from Month to {to_date} without descrepancy"
        attachment = None
        body = f"Greetings All,\nAs per yesterday's data, there were no descrepancy found in busy sales with the price list."

        logger.info(f"Report Produced without discrepancies")

    # try:
    #     receivers = ['shivprasad@kaybeebio.com', 
    #                  'holkar.h@kaybeebio.com'
    #                 ]
    #     cc = ['danish@kaybeeexports.com', 's.gaurav@kaybeeexports.com', 
    #           'mahendra@kaybeeexports.com'
    #         ]
    #     email_send(reciever= receivers, cc= cc, subject= subject, contents= body, attachemnts= attachment)
    #     logger.info(f"Successfully emailed the Busy Sales Price Validation Report.")
    # except Exception as e:
    #     logger.critical(f"Failed to email the Busy Sales Price Validation Report : {e}")
