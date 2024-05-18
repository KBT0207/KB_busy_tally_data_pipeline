import pandas as pd
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import insert, delete, and_, func, cast, case, Numeric
from logging_config import logger
from utils.common_utils import tables
from database.models.busy_models.busy_pricing import BusyPricingKBBIO
from database.models.busy_models.busy_reports import SalesKBBIO
from sqlalchemy.exc import SQLAlchemyError


class DatabaseCrud:
    def __init__(self, db_connector) -> None:
        self.db_connector = db_connector
        self.Session = scoped_session(sessionmaker(bind=self.db_connector.engine))

    
    def delete_date_range_query(self, table_name, start_date, end_date, commit):
        table_class = tables.get(table_name)
        if table_class:
            if start_date <= end_date:
                date_condition = and_(table_class.date.between(start_date, end_date))
            else:
                logger.critical("Start date or end date not provided for deletion.")
                return
            
            delete_query = delete(table_class).where(date_condition)
            
            with self.Session() as session:
                try:
                    result = session.execute(delete_query)
                    deleted_count = result.rowcount
                    if commit:
                        session.commit()
                    logger.info(f"Deleted {deleted_count} rows in {table_name} between {start_date} and {end_date}.")
                except SQLAlchemyError as e:
                    session.rollback()
                    logger.error(f"Error occurred during deletion: {e}")
        else:
            logger.info(f"Table {table_name} not found in table_mapping. Delete query Failed to execute")
        


    def get_row_count(self, table_name):
        with self.Session() as session:
            table_class = tables.get(table_name)
            if table_class:
                row_count = session.query(table_class).count()
                return row_count
            else:
                logger.error(f"Table '{table_name}' not found in table_mapping.")
                return None
    
    
    
    def import_data(self, table_name, df: pd.DataFrame, commit):
        if df is not None:
            row_count_before = self.get_row_count(table_name)
            row_count_after = None
            
            try:
                with self.Session() as session:
                    df.to_sql(table_name, self.db_connector.engine, if_exists='append', index=False, method='multi', chunksize=500)
                    row_count_after = self.get_row_count(table_name)
                    if commit:
                        session.commit()
            except SQLAlchemyError as e:
                logger.critical(f"Error inserting data into {table_name}: {e}")
                if row_count_after is not None:
                    session.rollback()
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
                with self.Session() as session:
                    session.execute(truncate_query)
                    if commit:
                        session.commit()
                    logger.info(f"Table '{table_name}' truncated successfully.")
            except SQLAlchemyError as e:
                logger.critical(f"Error truncating table '{table_name}': {e}")
                session.rollback()
        else:
            logger.error(f"Table '{table_name}' not found in table_mapping.")



    def sales_price_validation(self, from_date, to_date):
        join_query = self.Session.query(SalesKBBIO, BusyPricingKBBIO).outerjoin(
            BusyPricingKBBIO, and_(
                SalesKBBIO.party_type == BusyPricingKBBIO.customer_type,
                SalesKBBIO.item_details == BusyPricingKBBIO.item_name,
            ))

        results = join_query.filter(
            and_(
                SalesKBBIO.date.between(from_date, to_date),
                func.abs(cast((SalesKBBIO.main_price + SalesKBBIO.discount_amt), Numeric(10,2)) - cast(BusyPricingKBBIO.selling_price, Numeric(10,2))) > 1,
                SalesKBBIO.party_type == "Dealer", BusyPricingKBBIO.selling_price != 0
            )
        ).with_entities(SalesKBBIO.date, SalesKBBIO.voucher_no, SalesKBBIO.dealer_code, 
                        SalesKBBIO.particulars, SalesKBBIO.item_details,           
            cast(SalesKBBIO.main_price + SalesKBBIO.discount_amt, Numeric(10,2)).label('total_price'),
            SalesKBBIO.main_price, BusyPricingKBBIO.selling_price, SalesKBBIO.discount_amt, 
            SalesKBBIO.main_qty, SalesKBBIO.main_unit , SalesKBBIO.material_centre,
        ).all()

        # Convert results to DataFrame
        df_results = pd.DataFrame(results, columns=['Date', 'Invoice No', 'Dealer Code', 'Particulars',
                                                    'Sales_Item_Name', 'Total Price', 'Sales_Price', 
                                                    'Price_List', 'Discount_Amt', 'Qty', 'Unit', 
                                                    'Material Centre', 
                                                    ])

        return df_results


    # def test_import_data(self, table_name, df: pd.DataFrame, commit):
  
    #     if df is not None and not df.empty:
    #         row_count_before = self.get_row_count(table_name)
    #         row_count_after = None

    #         try:
    #             table = tables.get(table_name)
    #             if table is None:
    #                 logger.error(f"Table '{table_name}' not found in table_mapping.")
    #                 return

    #             with self.Session() as session:
    #                 connection = session.connection()
    #                 trans = connection.begin()

    #                 try:
    #                     records = df.to_dict(orient='records')
    #                     session.execute(insert(table), records)
    #                     row_count_after = self.get_row_count(table_name)

    #                     # Print session state for debugging (uncomment if needed)
    #                     print(f"Session state after import: {session.is_active}")

    #                     if commit:
    #                         trans.commit()
    #                         session.commit()
    #                         logger.info("Changes committed to the database.")
    #                     else:
    #                         trans.rollback()
    #                         logger.info("Changes rolled back due to commit=False.")

    #                 except Exception as e:
    #                     trans.rollback()
    #                     logger.error(f"Rolling back changes in {table_name} due to import error: {e}")
    #                     raise

    #         except SQLAlchemyError as e:
    #             logger.critical(f"Error inserting data into {table_name}: {e}")
    #             raise

    #         except Exception as e:
    #             logger.critical(f"Unknown error occurred: {e}")
    #             raise

    #         finally:
    #         # Ensure session is closed (already done by context manager, but explicit for clarity)
    #             session.close()

    #         if row_count_before is not None and row_count_after is not None:
    #             rows_inserted = row_count_after - row_count_before
    #             logger.info(f"Data imported into {table_name}. {rows_inserted} rows inserted.")
    #         else:
    #             logger.error("Failed to determine rows inserted.")

    #         # Additional check for debugging (uncomment if needed)
    #         separate_connection = self.engine.connect()
    #         try:
    #           result = separate_connection.execute(f"SELECT COUNT(*) FROM {table_name}")
    #           count = result.fetchone()[0]
    #           print(f"Data count in table after import (separate connection): {count}")
    #         finally:
    #           separate_connection.close()