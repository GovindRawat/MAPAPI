import os
import logging
import json
import pyodbc
import configparser
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, vault_url=None, secret_name=None):
        """
        Initialize the DatabaseManager with optional Azure Key Vault details.
        """
        self.vault_url = vault_url
        self.secret_name = secret_name
        self.credentials = None
        self.connection = None
        self.cursor = None

    def load_db_config(self):
        """
        Load database configuration from settings.ini file.
        """
        try:
            config = configparser.ConfigParser()
            config.read('config/settings.ini')
            self.server = config['database']['server']
            self.database = config['database']['database']
            self.username = config['database']['username']
            self.password = config['database']['password']
        except Exception as e:
            logger.error("Error reading database configuration: %s", e, exc_info=True)
            raise

    def local_connect(self):
        """
        Connect to the database using local credentials.
        """
        connection_string = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'UID={self.username};'
            f'PWD={self.password};'
            f'Authentication=ActiveDirectoryPassword;'
        )
        try:
            self.connection = pyodbc.connect(connection_string)
            self.cursor = self.connection.cursor()
            logger.info("Local database connection established.")
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}", exc_info=True)
            raise

    def fetch_credentials_from_key_vault(self):
        """
        Fetch database credentials from Azure Key Vault.
        """
        try:
            logger.info("Initializing Azure Key Vault client...")
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=self.vault_url, credential=credential)
            
            logger.info(f"Fetching secret: {self.secret_name}...")
            secret = client.get_secret(self.secret_name)
            
            if not secret.value:
                raise ValueError(f"Secret '{self.secret_name}' has no value!")
            
            logger.info(f"Successfully retrieved secret: {self.secret_name}")
            self.credentials = json.loads(secret.value)
        except Exception as e:
            logger.error(f"Error retrieving secret '{self.secret_name}': {e}", exc_info=True)
            raise

    def build_connection_string(self):
        """
        Build a connection string using the fetched credentials for Microsoft SQL Server.
        """
        if not self.credentials:
            raise ValueError("Credentials not fetched. Call fetch_credentials_from_key_vault() first.")
        
        try:
            logger.info("Building connection string...")
            username = self.credentials.get("username")
            password = self.credentials.get("password")
            host = self.credentials.get("host")
            port = self.credentials.get("port", "1433")  # Default SQL Server port is 1433
            database_name = self.credentials.get("database_name")
            
            if not all([username, password, host, database_name]):
                raise ValueError("One or more required connection parameters are missing.")
            
            connection_string = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={host},{port};"
                f"DATABASE={database_name};"
                f"UID={username};"
                f"PWD={password}"
            )
            logger.info("Connection string built successfully.")
            return connection_string
        except Exception as e:
            logger.error(f"Error building connection string: {e}", exc_info=True)
            raise

    def setup_environment_and_connect(self):
        """
        Determine the environment and connect to the database.
        """
        if os.getenv('BUILD_ID') or os.getenv('SYSTEM_TEAMPROJECT'):
            logger.info("Running in Azure Pipeline")
            if not self.vault_url or not self.secret_name:
                raise ValueError("Key Vault URL and secret name must be provided for Azure Pipeline.")
            self.fetch_credentials_from_key_vault()
            connection_string = self.build_connection_string()
            self.connect_to_database(connection_string)
        else:
            logger.info("Running locally")
            self.load_db_config()
            self.local_connect()

    def connect_to_database(self, connection_string):
        """
        Connect to the database using the provided connection string.
        """
        try:
            logger.info("Connecting to the database...")
            self.connection = pyodbc.connect(connection_string)
            self.cursor = self.connection.cursor()
            logger.info("Database connection established.")
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}", exc_info=True)
            raise

    def close(self):
        """
        Close the database connection and cursor.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("Database connection closed.")

    def fetch_user_emails(self):
        """
        Fetch user emails from the database.
        """
        try:
            self.cursor.execute(
                "SELECT UM.UserEmail FROM MAP.User_Master UM "
                "JOIN MAP.User_Access UA ON UM.UserID = UA.UserID;"
            )
            rows = self.cursor.fetchall()
            if not rows:
                raise ValueError("No user emails found.")
            return [row[0] for row in rows]
        except Exception as e:
            logger.error(f"Error fetching user emails: {e}", exc_info=True)
            raise

    def fetch_field_name(self):
        """
        Fetch field name from the database.
        """
        try:
            self.cursor.execute("SELECT Field_Name FROM MAP.Field_Master")
            result = self.cursor.fetchone()
            if result is None:
                raise ValueError("No field name found.")
            return result[0]
        except Exception as e:
            logger.error(f"Error fetching field name: {e}", exc_info=True)
            raise
