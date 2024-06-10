from sqlalchemy import insert, distinct, and_, case, func, cast, DECIMAL, select, Numeric, Table, text, MetaData
import pandas as pd
import numpy as np
from database.db_crud import DatabaseCrud
from logging_config import logger
# from utils.email import email_send
from database.models.busy_models.busy_pricing import BusyPricingKBBIO
from database.models.busy_models.busy_accounts import (BusyAccounts100x, BusyAccountsAgri, 
                                                    BusyAccountsGreenEra, BusyAccountsKBBIO,
                                                    BusyAccountsNewAge)
from database.models.busy_models.busy_reports import SalesKBBIO, SalesOrderKBBIO
from database.models.tally_models.tally_report_models import TallyAccounts, TallyOutstandingBalance


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
    
    
    
    def volume_discount_validation(self, dates:list, exceptions:list = None) -> pd.DataFrame:

        def calculate_remark(row):
            slabs = [
                    ('Others', 50, 99, 2),
                    ('Others', 100, 199, 4),
                    ('Others', 200, 399, 6),
                    ('Others', 400, 750, 8),
                    ('Others', 751, float('inf'), 10),
                    ('Granules', 500, 999, 2),
                    ('Granules', 1000, 2499, 3),
                    ('Granules', 2500, 4999, 5),
                    ('Granules', 5000, float('inf'), 7),
                    ]

            if row['item_category'] == 'Others' and row['total_qty'] < 50:
                return 'Match' if row['volume_disc'] == 0 else 'Discrepancy'

            for item_cat, lower, upper, discount in slabs:
                if row['item_category'] == item_cat and lower <= row['total_qty'] <= upper:
                    if row['volume_disc'] < discount:
                        return 'Less Discount'
                    elif row['volume_disc'] == discount:
                        return 'Match'

            if row['item_category'] == 'Granules' and row['total_qty'] < 500:
                return 'Match' if row['volume_disc'] == 0 else 'Discrepancy'
            
            if row['item_category'] == 'Organeem' and row['total_qty'] <= 50:
                return 'Match' if row['volume_disc'] == 0 else 'Discrepancy'

            return 'Discrepancy'
            
        item_catergory_column = case(
                                    # (SalesKBBIO.item_details.contains('Organeem'), 'Organeem'),
                                    (SalesKBBIO.item_details.contains('Granules'), 'Granules'),
                                    (SalesKBBIO.item_details.contains('Tunner'), 'Tunner'),
                                else_='Others').label('item_category')
        
        volume_disc = cast(case(
                            (and_(SalesKBBIO.discount_perc < 25, item_catergory_column == 'Others'), SalesKBBIO.discount_perc),
                            (and_(SalesKBBIO.discount_perc > 25, item_catergory_column == 'Others'), SalesKBBIO.discount_perc - 25),
                            (and_(SalesKBBIO.discount_perc < 20, item_catergory_column == 'Granules'), SalesKBBIO.discount_perc),
                            (and_(SalesKBBIO.discount_perc > 20, item_catergory_column == 'Granules'), SalesKBBIO.discount_perc - 20),
                        else_=0).label('volume_disc'), DECIMAL(10, 2))
        
        cash_disc = case((SalesKBBIO.discount_perc >= 25, 25), else_= 0).label('cash_disc')

        query = self.Session.query(SalesKBBIO.date, SalesKBBIO.voucher_no, SalesKBBIO.alt_qty, 
                                   SalesKBBIO.item_details, SalesKBBIO.particulars, 
                                   SalesKBBIO.discount_perc, item_catergory_column, volume_disc, cash_disc,
                                ).filter(and_(SalesKBBIO.party_type == 'Dealer', SalesKBBIO.date.in_(dates),
                                              item_catergory_column != 'Tunner', 
                                    )).filter(~SalesKBBIO.material_centre.like('NA %'),
                                              ~SalesKBBIO.material_centre.like('GE %'), 
                                              ~SalesKBBIO.material_centre.like('AS %'),
                                              )
        if exceptions:
            query = query.filter(~SalesKBBIO.dealer_code.in_(exceptions))

        group_query = query.group_by(SalesKBBIO.date, SalesKBBIO.particulars, 
                                     item_catergory_column, SalesKBBIO.discount_perc, volume_disc, cash_disc,
                                    )
        entity_query = group_query.order_by(SalesKBBIO.date, SalesKBBIO.particulars, 
                                            
                        ).with_entities(
                                    SalesKBBIO.date, SalesKBBIO.particulars, 
                                    item_catergory_column,
                                    cast(func.sum(SalesKBBIO.alt_qty).label('total_qty'), Numeric()), 
                                    SalesKBBIO.discount_perc, volume_disc, cash_disc)
                                
        # df = pd.read_sql(entity_query.statement, self.Session.bind)
        df = pd.DataFrame(entity_query, columns= ['date', 'particulars', 
                                                  'item_category', 
                                           'total_qty', 'disc_perc',
                                             'volume_disc', 'cash_disc', 
                                           ])
        df['remark'] = df.apply(calculate_remark, axis= 1)

        return df



    def cash_discount_validation(self, dates:list, exceptions:list = None) -> pd.DataFrame:
        #main busy sales query
        sales_query = self.Session.query(SalesKBBIO.date, SalesKBBIO.voucher_no,  SalesKBBIO.alt_qty, 
                                   SalesKBBIO.item_details, SalesKBBIO.particulars, 
                                   SalesKBBIO.discount_perc, SalesKBBIO.dealer_code,
                                ).filter(and_(SalesKBBIO.party_type == 'Dealer', SalesKBBIO.date.in_(dates),
                                              SalesKBBIO.discount_perc >= 20)
                                    ).filter(~SalesKBBIO.material_centre.like('NA %'),
                                              ~SalesKBBIO.material_centre.like('GE %'), 
                                              ~SalesKBBIO.material_centre.like('AS %'),
                                              )
 
        sales_distinct_invoice_query = sales_query.distinct(SalesKBBIO.voucher_no)
        
        sales_distinct_dealer_query = sales_query.distinct(SalesKBBIO.dealer_code)

        if exceptions:
            sales_distinct_invoice_query = sales_distinct_invoice_query.filter(~SalesKBBIO.dealer_code.in_(exceptions))
            sales_distinct_dealer_query = sales_distinct_dealer_query.filter(~SalesKBBIO.dealer_code.in_(exceptions))
        
        #busy sales distinct invoice query
        sales_distinct_invoice_query = sales_distinct_invoice_query.with_entities(SalesKBBIO.date, SalesKBBIO.voucher_no, 
                                            SalesKBBIO.particulars, SalesKBBIO.dealer_code, 
                                            SalesKBBIO.discount_perc,
                                    ).order_by(SalesKBBIO.date, SalesKBBIO.dealer_code)
        #busy sales distinct dealer query
        sales_distinct_dealer_query = sales_distinct_dealer_query.with_entities(SalesKBBIO.date, 
                                            SalesKBBIO.particulars, SalesKBBIO.dealer_code, 
                                    )
        # come back here ..requires modifications if data not found
        tally_accounts_query = (sales_distinct_dealer_query.outerjoin(TallyAccounts, 
                                                                      SalesKBBIO.dealer_code == TallyAccounts.alias_code
                                                                      ).with_entities(
                                        SalesKBBIO.date.label('sales_date'), 
                                        SalesKBBIO.dealer_code.label('sales_dealer_code'), 
                                        TallyAccounts.alias_code.label('tally_alias_code'), 
                                        SalesKBBIO.particulars.label('sales_particulars'), 
                                        TallyAccounts.ledger_name.label('tally_particulars'),
                                            )
                                            ).subquery()

        tally_code_query = sales_distinct_dealer_query.outerjoin(TallyAccounts, 
                                                                      SalesKBBIO.dealer_code == TallyAccounts.alias_code
                                                                      ).with_entities(
                                        TallyAccounts.alias_code.label('tally_alias_code'), 
                                        TallyAccounts.ledger_name.label('tally_particulars'),
                                            )

        outstanding_query = (self.Session.query(
                                    TallyOutstandingBalance.particulars, 
                                    tally_accounts_query.c.tally_alias_code, tally_accounts_query.c.sales_dealer_code, 

                                    (func.sum(TallyOutstandingBalance.credit) - func.sum(TallyOutstandingBalance.debit)).label("balance")
                                )
                                .outerjoin(tally_accounts_query,
                                    (TallyOutstandingBalance.particulars == tally_accounts_query.c.tally_particulars) &
                                    (TallyOutstandingBalance.date == tally_accounts_query.c.sales_date)
                                )
                                .filter(tally_accounts_query.c.tally_particulars != None)
                                .group_by(TallyOutstandingBalance.date, 
                                    TallyOutstandingBalance.particulars,  
                                    tally_accounts_query.c.tally_alias_code, 
                                    tally_accounts_query.c.sales_dealer_code, 
                                )
                            )
                      
        sales_invoice_df = pd.DataFrame(sales_distinct_invoice_query, columns= ['busy_date', 'invoice_no', 'busy_particulars', 
                                                  'busy_dealer_code', 'disc_perc', 
                                           ])
        
        tally_code_df = pd.DataFrame(tally_code_query, 
                                         columns= ['tally_dealer_code_new', 
                                                   'tally_particulars_new',
                                                   ])
        # outstanding_df = pd.DataFrame(outstanding_query, 
        #                               columns=['outstanding_date', 'outstanding_particulars', 
        #                                        'outs_debit', 'outs_credit', 'material_centre',
        #                                        'sales_date', 'sales_dealer_code', 'tally_alias_code', 
        #                                        'sales_particulars', 'tally_particulars', 
        #                                        ]
        #                                 )
        outstanding_df = pd.DataFrame(outstanding_query, 
                                      columns=['outstanding_particulars', 
                                               'tally_alias_code', 'sales_dealer_code', 'balance', 
                                               ])
        
        results_df = sales_invoice_df.merge(outstanding_df, how= 'left', 
                                            left_on= 'busy_dealer_code', right_on= 'tally_alias_code').fillna(0)
        
        results_df['remarks'] = np.where(results_df['balance'] >= 0, 'Matched', 'Discrepancy')
        results_df = results_df.sort_values(by=['busy_date', 'busy_particulars'])

        results_df = results_df.merge(tally_code_df, how= 'left', 
                                      left_on= 'busy_dealer_code', right_on= 'tally_dealer_code_new')
        # tally_df = pd.DataFrame(tally_accounts_query, columns= ['sales_date','sales_dealer_code', 
        #                                                         'tally_alias_code', 'sales_particulars',
        #                                                         'tally_particulars'])
        from xlwings import view
        # return sales_invoice_df, view(outstanding_df)
        return view(results_df)
        # return tally_df