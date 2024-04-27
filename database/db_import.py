import pandas as pd
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import delete 
from database.models import SalesKBBIO, SalesReturnKBBIO, SalesOrderKBBIO, MITPKBBIO, MRFPKBBIO



tables = {'busy_sales': SalesKBBIO, 'busy_sales_order': SalesOrderKBBIO,
          'busy_sales_return': SalesReturnKBBIO, "busy_mitp": MITPKBBIO,
          "busy_mrfp": MRFPKBBIO,
        }


class ImportExcel:
    def __init__(self, db_connector) -> None:
        self.db_connector = db_connector
        self.Session = scoped_session(sessionmaker(bind=self.db_connector.engine))

    
    def delete_date_query(self, table_name, *dates):
        table_class = tables.get(table_name)
        if table_class:
            if dates:
                date_condition = table_class.date.in_(dates)
            else:
                print("No dates provided for deletion.")
                return
            
            delete_query = delete(table_class).where(date_condition)
            
            with self.Session() as session:
                result = session.execute(delete_query)
                deleted_count = result.rowcount
                #session.commit()
                print(f"Deleted {deleted_count} rows with date in {dates}.")
        else:
            print(f"Table '{table_name}' not found in table_mapping.")

    
    
    def import_data(self, table_name, df:pd.DataFrame):
        if df is not None:
            df.to_sql(table_name, self.db_connector.engine, if_exists='append', index= False)
        else:
            print("Empty Dataframe")
