from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, key_vault_name):
        """
        Initialize the DatabaseManager with Azure Key Vault name.
        """
        if not key_vault_name:
            raise ValueError("Key Vault name must be provided.")
        
        self.key_vault_url = f"https://{key_vault_name}.vault.azure.net"
        self.credentials = DefaultAzureCredential()
        self.secret_client = SecretClient(vault_url=self.key_vault_url, credential=self.credentials)
        self.connection = None
        self.cursor = None

    def fetch_secrets(self):
        """
        Fetch the database secrets from Azure Key Vault.
        """
        try:
            logger.info("Fetching secrets from Azure Key Vault...")
            self.vault_url = self.secret_client.get_secret("vault-url").value
            self.secret_name = self.secret_client.get_secret("secret-name").value
            
            logger.info("Successfully fetched secrets.")
        except Exception as e:
            logger.error(f"Error fetching secrets: {e}", exc_info=True)
            raise

    def connect_to_database(self):
    """
    Connect to the database using details fetched from Azure Key Vault.
    """
    try:
        logger.info("Fetching database connection details from Azure Key Vault...")
        
        # Fetch necessary details from Azure Key Vault
        server = self.secret_client.get_secret("db-server").value
        database = self.secret_client.get_secret("db-database").value
        username = self.secret_client.get_secret("db-username").value
        password = self.secret_client.get_secret("db-password").value
        authentication = self.secret_client.get_secret("db-authentication").value  # Optional if needed

        logger.info("Successfully fetched database details. Constructing connection string...")
        
        # Construct the connection string
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            f"Authentication={authentication}"
        )
        
        logger.info("Connecting to the database...")
        
        # Establish the database connection
        self.connection = pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()
        
        logger.info("Database connection established successfully.")
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}", exc_info=True)
        raise


    def close_connection(self):
        """
        Close the database connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("Database connection closed.")
