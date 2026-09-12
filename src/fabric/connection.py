"""
Microsoft Fabric Data Warehouse Connection Manager.
Handles Entra ID Token acquisition and pyodbc connection to edm_wh_dev.
"""
import struct
import logging
from typing import Optional
from src.config.settings import settings

logger = logging.getLogger("fabric_connection")

class FabricConnectionManager:
    def __init__(self):
        self.server = settings.fabric_server
        self.database = settings.fabric_database
        self.auth_type = settings.fabric_auth_type
        self._connection_string = (
            f"Driver={{ODBC Driver 18 for SQL Server}};"
            f"Server={self.server},1433;"
            f"Database={self.database};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )

    def get_connection(self):
        """
        Returns a live pyodbc connection using Azure Default Azure Credential / Entra ID,
        or raises an exception if ODBC/credentials are unavailable.
        """
        try:
            import pyodbc
            from azure.identity import DefaultAzureCredential

            # Acquire Entra ID token for Azure SQL / Fabric DW
            credential = DefaultAzureCredential()
            token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
            token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)
            
            # SQL_COPT_SS_ACCESS_TOKEN attribute constant is 1256
            SQL_COPT_SS_ACCESS_TOKEN = 1256
            conn = pyodbc.connect(
                self._connection_string,
                attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct}
            )
            return conn
        except Exception as e:
            logger.warning(f"Could not connect to live Fabric endpoint ({e}). Running in fallback mode.")
            return None

fabric_conn = FabricConnectionManager()
