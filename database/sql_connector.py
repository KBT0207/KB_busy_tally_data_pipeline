from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv('.env')

class DatabaseConnector:
    def __init__(self, username, password, host, port, database) -> None:
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.engine = create_engine(self.get_db_string())

    def get_db_string(self):
        return f'mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
    


USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
DATABASE = os.getenv('DATABASE')


db_connector = DatabaseConnector(USERNAME, PASSWORD, HOST, PORT, DATABASE)

db_engine = db_connector.engine