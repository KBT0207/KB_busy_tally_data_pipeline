import pandas as pd
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import delete
from logging_config import logger
from database.models.busy_models import (SalesKBBIO, SalesReturnKBBIO, 
                                         SalesOrderKBBIO, MITPKBBIO, MRFPKBBIO,
                                         BusyAccountsKBBIO, BusyAccounts100x, BusyAccountsAgri,
                                         BusyAccountsGreenEra, BusyAccountsNewAge,
                                         )



tables = {'busy_sales': SalesKBBIO, 'busy_sales_order': SalesOrderKBBIO,
          'busy_sales_return': SalesReturnKBBIO, "busy_mitp": MITPKBBIO,
          "busy_mrfp": MRFPKBBIO, 
         "busy_acc_kbbio": BusyAccountsKBBIO,
          "busy_acc_100x": BusyAccounts100x, "busy_acc_agri": BusyAccountsAgri,
          "busy_acc_greenera": BusyAccountsGreenEra, "busy_acc_newage": BusyAccountsNewAge,
        }


class DatabaseCrud:
    def __init__(self, db_connector) -> None:
        self.db_connector = db_connector
        self.Session = scoped_session(sessionmaker(bind=self.db_connector.engine))

    
    def delete_date_query(self, table_name, *dates):
        table_class = tables.get(table_name)
        if table_class:
            if dates:
                date_condition = table_class.date.in_(dates)
            else:
                logger.critical("No dates provided for deletion.")
                return
            
            delete_query = delete(table_class).where(date_condition)
            
            with self.Session() as session:
                result = session.execute(delete_query)
                deleted_count = result.rowcount
                session.commit()
                logger.info(f"Deleted {deleted_count} rows in {table_name} with date in {dates}.")
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
    
    
    def import_data(self, table_name, df:pd.DataFrame):
        if df is not None:
            row_count_before = self.get_row_count(table_name)
            row_count_after = None
            
            try:
                df.to_sql(table_name, self.db_connector.engine, if_exists='append', index=False, method='multi', chunksize=500)
                row_count_after = self.get_row_count(table_name)
            except Exception as e:
                logger.critical(f"Error inserting data into {table_name}: {e}")

            if (row_count_before is not None) and (row_count_after is not None):
                rows_inserted = row_count_after - row_count_before
                logger.info(f"Data imported into {table_name}. {rows_inserted} rows inserted.")
            else:
                logger.error("Failed to determine rows inserted.")
        else:
            logger.error(f"Empty Dataframe hence 0 rows imported in {table_name}")


    def truncate_table(self, table_name):
        table_class = tables.get(table_name)
        if table_class:
            truncate_query = delete(table_class)
            with self.Session() as session:
                session.execute(truncate_query)
                session.commit()
                logger.info(f"Table '{table_name}' truncated successfully.")
        else:
            logger.error(f"Table '{table_name}' not found in table_mapping.")