"""Read-only access to the Microsoft Fabric SQL endpoint.

Authentication uses azure-identity (DefaultAzureCredential), so no secrets are
stored here — it picks up your Azure CLI / VS Code / managed-identity login.
Only SELECT statements are issued; nothing in Fabric is modified.
"""
from __future__ import annotations

import struct
import threading
from typing import Any

from .config import settings

# ODBC attribute for passing an Entra access token to SQL Server / Fabric.
_SQL_COPT_SS_ACCESS_TOKEN = 1256
_TOKEN_SCOPE = "https://database.windows.net/.default"

# Build the credential once. azure-identity caches the token internally, so
# repeated requests reuse it instead of re-running the whole credential chain
# (and re-hitting IMDS for the managed identity) on every query.
_credential = None
_cred_lock = threading.Lock()


def _credential_instance():
    global _credential
    if _credential is None:
        with _cred_lock:
            if _credential is None:
                from azure.identity import DefaultAzureCredential

                _credential = DefaultAzureCredential(
                    exclude_managed_identity_credential=settings.exclude_managed_identity,
                )
    return _credential


def _access_token_struct() -> bytes:
    token = _credential_instance().get_token(_TOKEN_SCOPE).token
    token_bytes = token.encode("utf-16-le")
    return struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)


def _connect():
    import pyodbc

    # Reuse physical connections via the ODBC driver manager's pool, so bursts of
    # requests don't open a fresh TCP connection to Fabric every time.
    pyodbc.pooling = True

    if not settings.fabric_sql_endpoint:
        raise RuntimeError("FABRIC_SQL_ENDPOINT is not configured.")

    conn_str = (
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server={settings.fabric_sql_endpoint};"
        f"Database={settings.fabric_database};"
        "Encrypt=yes;TrustServerCertificate=no;"
    )
    return pyodbc.connect(
        conn_str,
        attrs_before={_SQL_COPT_SS_ACCESS_TOKEN: _access_token_struct()},
        timeout=30,
    )


def query(sql: str, params: list[Any] | None = None) -> list[dict[str, Any]]:
    """Run a read-only SELECT and return rows as dicts."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params or [])
        columns = [c[0] for c in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
