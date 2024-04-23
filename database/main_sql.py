from sqlalchemy.ext.declarative import declarative_base
from database.sql_connector import db_engine

from database.models import metadata, base, SalesKBBIO


def main_sql():    
    base.metadata = metadata

    base.metadata.create_all(db_engine)

