from app import fabric_client as f

print("payroll_line worker-ish cols:")
for c in f.query(
    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
    "WHERE TABLE_SCHEMA='silver' AND TABLE_NAME='payroll_line' "
    "AND (LOWER(COLUMN_NAME) LIKE '%worker%' OR LOWER(COLUMN_NAME) LIKE '%employee%' "
    "OR LOWER(COLUMN_NAME) LIKE '%person%' OR LOWER(COLUMN_NAME) LIKE '%party%')"
):
    print("  ", c["COLUMN_NAME"])

print("pay_period sample:")
for r in f.query(
    "SELECT TOP 3 pay_period_id, period_name, start_date, end_date, pay_date, period_status "
    "FROM silver.pay_period ORDER BY pay_period_id"
):
    print("  ", dict(r))
