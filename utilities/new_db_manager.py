import os
import logging
import json
import pyodbc
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AzureDatabaseConnector:
    def __init__(self, vault_url, secret_name):
        """
        Initialize the AzureDatabaseConnector with Key Vault details.
        """
        if not vault_url or not secret_name:
            raise ValueError("Both vault_url and secret_name must be provided.")
        
        self.vault_url = vault_url
        self.secret_name = secret_name
        self.credentials = None

    def fetch_credentials(self):
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
            logger.error(f"Error retrieving secret '{self.secret_name}': {e}")
            raise

    def build_connection_string(self):
        """
        Build a connection string using the fetched credentials for Microsoft SQL Server.
        """
        if not self.credentials:
            raise ValueError("Credentials not fetched. Call fetch_credentials() first.")
        
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
            logger.error(f"Error building connection string: {e}")
            raise

    def connect(self):
        """
        Full process to fetch credentials, build connection string, and test the connection.
        """
        self.fetch_credentials()
        connection_string = self.build_connection_string()
        self.test_connection(connection_string)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.logger.info('Database connection closed.')

    def fetch_user_emails(self):
        try:
            self.cursor.execute("SELECT UM.UserEmail FROM MAP.User_Master UM JOIN MAP.User_Access UA ON UM.UserID = "
                                "UA.UserID;")
            rows = self.cursor.fetchall()
            if not rows:
                raise ValueError("No user emails found.")
            return [row[0] for row in rows]
        except Exception as e:
            self.logger.error(f"Error fetching user emails: {e}", exc_info=True)
            raise
        finally:
            self.close()

    def fetch_field_name(self):
        try:
            self.cursor.execute("SELECT Field_Name FROM MAP.Field_Master")
            result = self.cursor.fetchone()
            if result is None:
                raise ValueError("No field name found.")
            return result[0]
        except Exception as e:
            self.logger.error(f"Error fetching field name: {e}", exc_info=True)
            raise
        finally:
            self.close()
