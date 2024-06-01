import pandas as pd
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import insert, delete, and_, func, cast, select, Numeric, Table, text, MetaData
from logging_config import logger
from utils.common_utils import tables
from database.models.busy_models.busy_pricing import BusyPricingKBBIO
from database.models.busy_models.busy_accounts import (BusyAccounts100x, BusyAccountsAgri, 
                                                    BusyAccountsGreenEra, BusyAccountsKBBIO,
                                                    BusyAccountsNewAge)
from database.models.busy_models.busy_reports import SalesKBBIO, SalesOrderKBBIO
from sqlalchemy.exc import SQLAlchemyError
from database.models.tally_models.tally_report_models import TallyAccounts



class DatabaseCrud:
    def __init__(self, db_connector) -> None:
        self.db_connector = db_connector
        self.db_engine = db_connector.engine
        self.Session = scoped_session(sessionmaker(bind=self.db_connector.engine, autoflush=False))
        self.metadata = MetaData()


    
    def delete_date_range_query(self, table_name, start_date, end_date, commit):
        table_class = tables.get(table_name)
        if table_class:
            if start_date <= end_date:
                date_condition = and_(table_class.date.between(start_date, end_date))
            else:
                logger.critical("Start date or end date not provided for deletion.")
                return
            
            delete_query = delete(table_class).where(date_condition)
            
            with self.db_engine.connect() as connection:
                try:
                    result = connection.execute(delete_query)
                    deleted_count = result.rowcount
                    if commit:
                        connection.commit()
                    logger.info(f"Deleted {deleted_count} rows in {table_name} between {start_date} and {end_date}.")
                except SQLAlchemyError as e:
                    connection.rollback()
                    logger.error(f"Error occurred during deletion: {e}")
        else:
            logger.info(f"Table {table_name} not found in table_mapping. Delete query Failed to execute")
        


    def get_row_count(self, table_name):
        table_class = tables.get(table_name)
        
        if not table_class:
            logger.error(f"Table '{table_name}' not found in table_mapping.")
            return None

        with self.db_engine.connect() as connection:
            if isinstance(table_class, Table):  # If it's a Table object
                count_query = select([func.count()]).select_from(table_class)
                row_count = connection.execute(count_query).scalar()
            else:  # If it's an ORM class
                table_name = table_class.__tablename__
                row_count = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()

        return row_count
    
    

    def import_data(self, table_name, df: pd.DataFrame, commit):
        if df is not None:
            row_count_before = self.get_row_count(table_name)
            row_count_after = None
            
            try:
                with self.db_engine.connect() as connection:
                    df.to_sql(table_name, self.db_connector.engine, if_exists='append', index=False, method='multi', chunksize=500)
                    row_count_after = self.get_row_count(table_name)
                    if commit:
                        connection.commit()
            except SQLAlchemyError as e:
                logger.critical(f"Error inserting data into {table_name}: {e}")
                if row_count_after is not None:
                    connection.rollback()
                    logger.error(f"Rolling back changes in {table_name} due to import error.")
            except Exception as e:
                logger.critical(f"Unknown error occurred: {e}")

            if (row_count_before is not None) and (row_count_after is not None):
                rows_inserted = row_count_after - row_count_before
                logger.info(f"Data imported into {table_name}. {rows_inserted} rows inserted.")
            else:
                logger.error("Failed to determine rows inserted.")
        else:
            logger.error(f"Empty Dataframe hence 0 rows imported in {table_name}")



    def truncate_table(self, table_name, commit):
        table_class = tables.get(table_name)
        if table_class:
            truncate_query = delete(table_class)
            try:
                with self.db_engine.connect() as connection:
                    connection.execute(truncate_query)
                    if commit:
                        connection.commit()
                    logger.info(f"Table '{table_name}' truncated successfully.")
            except SQLAlchemyError as e:
                logger.critical(f"Error truncating table '{table_name}': {e}")
                connection.rollback()
        else:
            logger.error(f"Table '{table_name}' not found in table_mapping.")



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
    


    def import_accounts_data(self, 
                              df:pd.DataFrame, 
                              commit:bool,
                              ):
        
        df['ledger_name'] = df['ledger_name'].str.title()

        df_material_centre = df["material_centre"][1]
        
        if 'NA' in df_material_centre:
            busy_table = BusyAccountsNewAge
        elif 'AS' in df_material_centre:
            busy_table = BusyAccountsAgri
        elif 'GE' in df_material_centre:
            busy_table = BusyAccountsGreenEra
        else:
            busy_table = BusyAccountsKBBIO

        busy_data = self.Session.query(busy_table).with_entities(busy_table.name, busy_table.alias, 
                                                                 ).all()
        df_busy_data = pd.DataFrame(busy_data, columns= ['busy_name', 'alias_code'])

        join_query = self.Session.query(TallyAccounts).filter(TallyAccounts.material_centre == df_material_centre)

        accounts = join_query.with_entities(TallyAccounts.ledger_name, TallyAccounts.alias_code, 
                                            TallyAccounts.state, TallyAccounts.material_centre,                                 
                                            ).all()
        df_accounts = pd.DataFrame(accounts, columns=['ledger_name', 'alias_code', 
                                                      'state', 'material_centre', 
                                                    ])
        
        df_accounts['ledger_name'] = df_accounts['ledger_name'].str.title()

        new_data = df.merge(df_accounts, how= 'left', on= 'ledger_name', indicator=True)
        new_data = new_data.loc[new_data['_merge']=='left_only', 
                                  ['ledger_name', 'under', 'state_x', 'gst_registration_type', 
                                   'gst_no', 'opening_balance', 'material_centre_x', 
                                    'alias_code',
                                    ]
                                    ].replace({pd.NA: None})
        new_data.columns = new_data.columns.str.rstrip("_x")

        new_data_with_busy_name = new_data.merge(df_busy_data, how= 'left', 
                                                 left_on= 'ledger_name', right_on= 'busy_name', 
                                                 indicator= True)
        new_data_with_busy_name = new_data_with_busy_name.drop(columns=['alias_code_x', '_merge']).replace({pd.NA: None})

        new_data_with_busy_name.columns = new_data_with_busy_name.columns.str.rstrip("_y")

        if not new_data_with_busy_name.empty: 
            values = new_data_with_busy_name.to_dict('records')
            insert_stmt = insert(TallyAccounts).values(values)
            try:
                with self.db_engine.connect() as connection:
                    result = connection.execute(insert_stmt)
                    if commit:
                        connection.commit()
                        logger.info(f"Inserted {result.rowcount} rows into tally_accounts.")
                    else:
                        connection.rollback()
                        logger.info(f"Transaction rollback successfully without any errors as commit was given False.")
            except SQLAlchemyError as e:
                logger.critical(f"Error inserting data into tally_accounts: {e}")
                connection.rollback()
                logger.error(f"Rolling back changes in tally_accounts due to import error.")
            except Exception as e:
                logger.critical(f"Unknown error occurred: {e}")
        else:
            logger.info(f"No new data to import in the database.")
        # from xlwings import view
        # return view(to_import_data)
        # return view(new_data_with_busy_name)
    
        # # return df_accounts['material_centre'].value_counts()
        # return df['material_centre'].value_counts()

        # to_import_data.to_excel(r"C:\Users\HP\Desktop\test_files\Accounts_merged.xlsx", index=False)



    # def import_items_data(self, 
    #                           df:pd.DataFrame, 
    #                           commit:bool,
    #                           ):
        
    #     df['ledger_name'] = df['ledger_name'].str.title()

    #     df_material_centre = df["material_centre"][1]
        
    #     if 'NA' in df_material_centre:
    #         busy_table = BusyAccountsNewAge
    #     elif 'AS' in df_material_centre:
    #         busy_table = BusyAccountsAgri
    #     elif 'GE' in df_material_centre:
    #         busy_table = BusyAccountsGreenEra
    #     else:
    #         busy_table = BusyAccountsKBBIO

    #     busy_data = self.Session.query(busy_table).with_entities(busy_table.name, busy_table.alias, 
    #                                                              ).all()
    #     df_busy_data = pd.DataFrame(busy_data, columns= ['busy_name', 'alias_code'])

    #     join_query = self.Session.query(TallyAccounts).filter(TallyAccounts.material_centre == df_material_centre)

    #     accounts = join_query.with_entities(TallyAccounts.ledger_name, TallyAccounts.alias_code, 
    #                                         TallyAccounts.state, TallyAccounts.material_centre,                                 
    #                                         ).all()
    #     df_accounts = pd.DataFrame(accounts, columns=['ledger_name', 'alias_code', 
    #                                                   'state', 'material_centre', 
    #                                                 ])
        
    #     df_accounts['ledger_name'] = df_accounts['ledger_name'].str.title()

    #     new_data = df.merge(df_accounts, how= 'left', on= 'ledger_name', indicator=True)
    #     new_data = new_data.loc[new_data['_merge']=='left_only', 
    #                               ['ledger_name', 'under', 'state_x', 'gst_registration_type', 
    #                                'gst_no', 'opening_balance', 'material_centre_x', 
    #                                 'alias_code',
    #                                 ]
    #                                 ].replace({pd.NA: None})
    #     new_data.columns = new_data.columns.str.rstrip("_x")

    #     new_data_with_busy_name = new_data.merge(df_busy_data, how= 'left', 
    #                                              left_on= 'ledger_name', right_on= 'busy_name', 
    #                                              indicator= True)
    #     new_data_with_busy_name = new_data_with_busy_name.drop(columns=['alias_code_x', '_merge']).replace({pd.NA: None})

    #     new_data_with_busy_name.columns = new_data_with_busy_name.columns.str.rstrip("_y")

    #     if not new_data_with_busy_name.empty: 
    #         values = new_data_with_busy_name.to_dict('records')
    #         # print(values)
    #         insert_stmt = insert(TallyAccounts).values(values)
    #         try:
    #             with self.db_engine.connect() as connection:
    #                 result = connection.execute(insert_stmt)
    #                 if commit:
    #                     connection.commit()
    #                     logger.info(f"Inserted {result.rowcount} rows into tally_accounts.")
    #                 else:
    #                     connection.rollback()
    #                     logger.info(f"Transaction rollback successfully without any errors as commit was given False.")
    #         except SQLAlchemyError as e:
    #             logger.critical(f"Error inserting data into tally_accounts: {e}")
    #             connection.rollback()
    #             logger.error(f"Rolling back changes in tally_accounts due to import error.")
    #         except Exception as e:
    #             logger.critical(f"Unknown error occurred: {e}")
    #     else:
    #         logger.info(f"No new data to import in the database.")
    #     # from xlwings import view
    #     # return view(to_import_data)
    #     # return view(new_data_with_busy_name)
    
    #     # # return df_accounts['material_centre'].value_counts()
    #     # return df['material_centre'].value_counts()

    #     # to_import_data.to_excel(r"C:\Users\HP\Desktop\test_files\Accounts_merged.xlsx", index=False)



    def test_import_data(self, table_name, df:pd.DataFrame, commit):
 
        if df is not None and not df.empty:
            # Assuming data_to_insert is a list of dictionaries representing rows
            data_to_insert = df.to_dict(orient='records')
            if not data_to_insert:
                print(f"No data to insert into {table_name}.")
                return

            table = tables.get(table_name)
            if table is None:
                print(f"Table {table_name} not found in metadata.")
                return

            insert_query = insert(table).values(data_to_insert)
            try:
                with self.db_engine.connect() as connection:
                    result = connection.execute(insert_query)
                    if commit:
                        connection.commit()
                        print(f"Inserted {result.rowcount} rows into {table_name}.")
                    else:
                        connection.rollback()
            except SQLAlchemyError as e:
                logger.critical(f"Error inserting data into {table_name}: {e}")
                connection.rollback()
                logger.error(f"Rolling back changes in {table_name} due to import error.")
            except Exception as e:
                logger.critical(f"Unknown error occurred: {e}")
                    
        else:
            print(f"Empty DataFrame, no rows inserted into {table_name}.")



    def test_delete(self, table_name, start_date, end_date, commit):


        table_class = tables.get(table_name)
        if table_class:
            if start_date <= end_date:
                date_condition = and_(table_class.created_at.between(start_date, end_date))
            else:
                logger.critical("Start date or end date not provided for deletion.")
                return
            
            delete_query = delete(table_class).where(date_condition)
            
            with self.db_engine.connect() as connection:
                try:
                    result = connection.execute(delete_query)
                    deleted_count = result.rowcount
                    if commit:
                        connection.commit()
                    logger.info(f"Deleted {deleted_count} rows in {table_name} between {start_date} and {end_date}.")
                except SQLAlchemyError as e:
                    connection.rollback()
                    logger.error(f"Error occurred during deletion: {e}")
        else:
            logger.info(f"Table {table_name} not found in table_mapping. Delete query Failed to execute")



