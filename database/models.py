from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
#from database.sql_connector import db_connector, db_engine


# metadata = MetaData()
# base = declarative_base(metadata)


# class SalesKBBIO(base):
#     __tablename__ = 'sales_kbbio'

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     address = Column(String)
#     email = Column(String)

#base.metadata.create_all(db_engine, checkfirst=True)