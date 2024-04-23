import pytest
from sqlalchemy import inspect
from database.sql_connector import DatabaseConnector

# Define test data
USERNAME = 'test_username'
PASSWORD = 'test_password'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'test_database'

def test_db_connector_init():
    # Initialize DatabaseConnector with test data
    db_connector = DatabaseConnector(USERNAME, PASSWORD, HOST, PORT, DATABASE)

    # Assert that the engine is created
    assert db_connector.engine is not None

def test_db_connector_attributes():
    # Initialize DatabaseConnector with test data
    db_connector = DatabaseConnector(USERNAME, PASSWORD, HOST, PORT, DATABASE)

    # Check that the attributes are set correctly
    assert db_connector.username == USERNAME
    assert db_connector.password == PASSWORD
    assert db_connector.host == HOST
    assert db_connector.port == PORT
    assert db_connector.database == DATABASE

def test_db_string():
    # Initialize DatabaseConnector with test data
    db_connector = DatabaseConnector(USERNAME, PASSWORD, HOST, PORT, DATABASE)

    # Get the database connection string
    db_string = db_connector.get_db_string()

    # Assert that the database connection string is correctly formatted
    assert db_string == f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

def test_db_engine():
    # Initialize DatabaseConnector with test data
    db_connector = DatabaseConnector(USERNAME, PASSWORD, HOST, PORT, DATABASE)

    # Get the database engine
    db_engine = db_connector.engine

    # Assert that the engine is created and connected
    assert db_engine is not None
    assert inspect(db_engine).is_connected()

# Optionally, you can include more tests as needed

