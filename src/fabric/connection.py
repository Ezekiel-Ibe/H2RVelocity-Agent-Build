"""
Microsoft Fabric Data Warehouse Connection Manager.
Handles Entra ID Token acquisition and pyodbc connection to edm_wh_dev.
"""
import struct
import logging
from typing import Optional
from src.config.settings import settings

logger = logging.getLogger("fabric_connection")

# Preferred ODBC driver order when settings.fabric_odbc_driver == "auto"
_DRIVER_PREFERENCE = [
    "ODBC Driver 18 for SQL Server",
    "ODBC Driver 17 for SQL Server",
    "SQL Server",
]

class FabricConnectionManager:
    def __init__(self):
        self.server = settings.fabric_server
        self.database = settings.fabric_database
        self.auth_type = settings.fabric_auth_type
        self.driver = self._resolve_driver(settings.fabric_odbc_driver)
        self._connection_string = (
            f"Driver={{{self.driver}}};"
            f"Server={self.server},1433;"
            f"Database={self.database};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )

    @staticmethod
    def _resolve_driver(configured: str) -> str:
        """Pick a concrete ODBC driver name; auto-detects the newest one installed."""
        if configured and configured.lower() != "auto":
            return configured
        try:
            import pyodbc
            installed = set(pyodbc.drivers())
            for candidate in _DRIVER_PREFERENCE:
                if candidate in installed:
                    return candidate
        except Exception as e:
            logger.warning("Could not enumerate installed ODBC drivers: %s", e)
        return _DRIVER_PREFERENCE[0]

    def get_connection(self):
        """
        Returns a live pyodbc connection using Azure Default Azure Credential / Entra ID,
        or None if ODBC/credentials are unavailable.
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
            logger.info("Connected to live Fabric warehouse %s using %s.", self.database, self.driver)
            return conn
        except Exception as e:
            logger.warning(f"Could not connect to live Fabric endpoint ({e}). Running in fallback mode.")
            return None

fabric_conn = FabricConnectionManager()
