from sqlalchemy import insert, delete, and_, case, func, cast, select, Numeric, Table, text, MetaData
import pandas as pd
from database.db_crud import DatabaseCrud
from logging_config import logger
# from utils.email import email_send
from database.models.busy_models.busy_pricing import BusyPricingKBBIO
from database.models.busy_models.busy_accounts import (BusyAccounts100x, BusyAccountsAgri, 
                                                    BusyAccountsGreenEra, BusyAccountsKBBIO,
                                                    BusyAccountsNewAge)
from database.models.busy_models.busy_reports import SalesKBBIO, SalesOrderKBBIO



class Reports(DatabaseCrud):

    def sales_price_validation(self, from_date:str, to_date:str, exceptions:list = None) -> pd.DataFrame:
        """This method queries the database to provide busy sales price validation report in a dataframe.  

        Args:
            from_date (str): The date from which busy sales needed to be validated from.
            to_date (str): The date till which busy sales needed to be validated.
            exceptions (list, optional): Takes in Sales Voucher Number which you want to be excluded from the report. Defaults to None.

        Returns:
            pd.DataFrame: Dataframe includes relevant columns of 'busy_sales' along with Price List column. 
        """
        join_query = self.Session.query(SalesKBBIO, BusyPricingKBBIO).outerjoin(
            BusyPricingKBBIO, and_(
                SalesKBBIO.party_type == BusyPricingKBBIO.customer_type,
                SalesKBBIO.item_details == BusyPricingKBBIO.item_name,
            ))

        query = join_query.filter(
            and_(
                SalesKBBIO.date.between(from_date, to_date),
                func.abs(cast((SalesKBBIO.main_price + SalesKBBIO.discount_amt), Numeric(10,2)) - cast(BusyPricingKBBIO.selling_price, Numeric(10,2))) > 1,
                SalesKBBIO.party_type == "Dealer", BusyPricingKBBIO.selling_price != 0,
            ))
        if exceptions:
            query = query.filter(~SalesKBBIO.voucher_no.in_(exceptions))
        results = query.with_entities(SalesKBBIO.date, SalesKBBIO.voucher_no, 
                                                SalesKBBIO.dealer_code, SalesKBBIO.particulars, 
                                                SalesKBBIO.item_details,           
            cast(SalesKBBIO.main_price + SalesKBBIO.discount_amt, Numeric(10,2)).label('total_price'),
            SalesKBBIO.main_price, BusyPricingKBBIO.selling_price, SalesKBBIO.discount_amt, 
            SalesKBBIO.main_qty, SalesKBBIO.main_unit , SalesKBBIO.material_centre,
                                ).all()

        df_results = pd.DataFrame(results, columns=['Date', 'Invoice No', 'Dealer Code', 
                                                    'Particulars', 'Sales_Item_Name', 'Total Price', 
                                                    'Sales_Price', 'Price_List', 'Discount_Amt', 
                                                    'Qty', 'Unit', 'Material Centre', 
                                                    ])

        return df_results

 

    def salesman_order_validation(self, from_date:str, to_date:str, exceptions:list = None) -> pd.DataFrame:
        
        salesorder = self.Session.query(SalesOrderKBBIO).filter(and_(SalesOrderKBBIO.date.between(from_date, to_date),
                                                        SalesOrderKBBIO.salesman.is_(None), SalesOrderKBBIO.salesman == None))
        if exceptions:
            salesorder = salesorder.filter(SalesOrderKBBIO.voucher_no.in_(exceptions))
        salesorder = salesorder.with_entities(SalesOrderKBBIO.date, SalesOrderKBBIO.voucher_no, 
                                    SalesOrderKBBIO.particulars, SalesOrderKBBIO.item_details, 
                                    SalesOrderKBBIO.material_centre, SalesOrderKBBIO.main_qty, 
                                    SalesOrderKBBIO.main_unit, SalesOrderKBBIO.main_price, SalesOrderKBBIO.alt_qty, 
                                    SalesOrderKBBIO.alt_unit, SalesOrderKBBIO.alt_price, SalesOrderKBBIO.amount, 
                                    SalesOrderKBBIO.tax_amt, SalesOrderKBBIO.order_amt, SalesOrderKBBIO.salesman, 
                                    SalesOrderKBBIO.salesman_id,
                                   ).all()
        df_salesorder = pd.DataFrame(salesorder, 
                                     columns=['Date', 'Voucher No', 'Particulars', 'Item Details', 
                                              'Material Centre', 'Main Qty', 'Main Unit', 'Main Price', 
                                              'Alt Qty', 'Alt Unit', 'Alt Price', 'Amount', 'Tax Amnt', 
                                              'Order Amnt', 'Salesman Name', 'Salesman ID',
                                                    ])
        return df_salesorder
    
    
    
    def volume_discount_validation(self, date:str, exceptions:list = None) -> pd.DataFrame:

        def calculate_remark(row):
            if row['total_qty'] < 50 and row['volume_disc'] == 0:
                return 'ok'
            elif 50 <= row['total_qty'] <= 99 and row['volume_disc'] == 2:
                return 'ok'
            elif 100 <= row['total_qty'] <= 199 and row['volume_disc'] == 4:
                return 'ok'
            elif 200 <= row['total_qty'] <= 399 and row['volume_disc'] == 6:
                return 'ok'
            elif 400 <= row['total_qty'] <= 750 and row['volume_disc'] == 8:
                return 'ok'
            elif row['total_qty'] > 750 and row['volume_disc'] == 10:
                return 'ok'
            else:
                return 'Discrep'
        
        group_query = self.Session.query(SalesKBBIO.date,SalesKBBIO.voucher_no, SalesKBBIO.alt_qty, 
                                         SalesKBBIO.particulars, SalesKBBIO.discount_perc,
                                ).filter(and_(SalesKBBIO.party_type == 'Dealer', SalesKBBIO.date == date, 
                                        ~SalesKBBIO.item_details.contains('Granules'),
                                        ~SalesKBBIO.item_details.contains('Tunner'),
                                        ~SalesKBBIO.item_details.contains('Organeem'),
                                        )
                                    ).group_by(SalesKBBIO.date, SalesKBBIO.particulars,  
                                               SalesKBBIO.discount_perc,
                                    )
        entity_query = group_query.order_by(SalesKBBIO.particulars,

                        ).with_entities(
                                    SalesKBBIO.date, SalesKBBIO.particulars, 
                                    func.sum(SalesKBBIO.alt_qty).label('total_qty'), 
                                    SalesKBBIO.discount_perc, 
                            case(
                                (SalesKBBIO.discount_perc > 25, SalesKBBIO.discount_perc - 25),
                                else_= 0).label('volume_disc'),
                            case(
                                (SalesKBBIO.discount_perc >= 25, 25),
                                else_= 0).label('cash_disc'))
        

        df = pd.DataFrame(entity_query, columns= ['date', 'particulars',  
                                           'total_qty', 
                                           'disc_perc', 'volume_disc', 'cash_disc'])
        df['remark'] = df.apply(calculate_remark, axis= 1)

        return df
