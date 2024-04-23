from database.sql_connector import db_connector


class ImportExcel:
    def __init__(self, db_connector) -> None:
        self.db_connector = db_connector
