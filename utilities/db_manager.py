import pyodbc
import configparser
import logging


class DatabaseManager:
    def __init__(self):
        self.logger = self.setup_logger()
        self.load_db_config()
        self.connection = None
        self.cursor = None

    def load_db_config(self):
        config = configparser.ConfigParser()
        config.read('config/settings.ini')

        self.server = config['database']['server']
        self.database = config['database']['database']
        self.username = config['database']['username']
        self.password = config['database']['password']

    def setup_logger(self):
        logger = logging.getLogger('DatabaseManager')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('database_manager.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def connect(self):
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password};Authentication=ActiveDirectoryPassword;'
        try:
            self.connection = pyodbc.connect(connection_string)
            self.cursor = self.connection.cursor()
            self.logger.info('Database connection established.')
        except Exception as e:
            self.logger.error(f"Error connecting to the database: {e}", exc_info=True)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.logger.info('Database connection closed.')

    # Add your methods for fetching data, etc. here

    #TODO modify the query
    def fetch_user_emails(self):
        self.cursor.execute("SELECT email FROM users")
        return [row[0] for row in self.cursor.fetchall()]

    #TODO modify the query
    def fetch_field_name(self):
        self.cursor.execute("SELECT field_name FROM fields")
        return self.cursor.fetchone()[0]
