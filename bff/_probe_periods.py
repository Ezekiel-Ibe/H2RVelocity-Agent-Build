"""Temporary probe: discover period/date columns and distinct pay periods."""
from app import fabric_client

# Columns that look like period/date across silver tables
cols = fabric_client.query(
    "SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
    "WHERE TABLE_SCHEMA='silver' AND ("
    " LOWER(COLUMN_NAME) LIKE '%period%' OR LOWER(COLUMN_NAME) LIKE '%date%' "
    " OR LOWER(COLUMN_NAME) LIKE '%run_id%') "
    "ORDER BY TABLE_NAME, COLUMN_NAME"
)
print("=== period/date columns (silver) ===")
for c in cols:
    print(f"{c['TABLE_NAME']}.{c['COLUMN_NAME']} ({c['DATA_TYPE']})")

print("\n=== distinct pay_period_id on payroll_case ===")
try:
    for r in fabric_client.query(
        "SELECT DISTINCT pay_period_id FROM silver.payroll_case "
        "WHERE fabric_current_indicator=1 ORDER BY pay_period_id"
    ):
        print(r["pay_period_id"])
except Exception as e:
    print("ERR", e)

print("\n=== payroll_run sample ===")
try:
    for r in fabric_client.query("SELECT TOP 5 * FROM silver.payroll_run"):
        print({k: r[k] for k in list(r)[:8]})
except Exception as e:
    print("ERR", e)
