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

    def test_connection(self, connection_string):
        """
        Test the database connection using the provided connection string.
        """
        try:
            logger.info("Testing database connection...")
            with pyodbc.connect(connection_string, timeout=5) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")  # Simple query to verify the connection
                result = cursor.fetchone()
                if result and result[0] == 1:
                    logger.info("Successfully connected to the database.")
                else:
                    raise ValueError("Test query did not return expected result.")
        except Exception as e:
            logger.error(f"Error testing database connection: {e}")
            raise

    def connect(self):
        """
        Full process to fetch credentials, build connection string, and test the connection.
        """
        self.fetch_credentials()
        connection_string = self.build_connection_string()
        self.test_connection(connection_string)

if __name__ == "__main__":
    try:
        # Read environment variables
        vault_url = os.getenv("AZURE_KEY_VAULT_URL")
        secret_name = os.getenv("DATABASE_SECRET_NAME")

        # Initialize and run the connector
        connector = AzureDatabaseConnector(vault_url, secret_name)
        connector.connect()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
