from app import fabric_client as f

for tbl in ("payroll_case", "payroll_anomaly", "payroll_line", "payroll_run"):
    try:
        rows = f.query(
            f"SELECT DISTINCT TOP 6 pay_period_id FROM silver.{tbl} ORDER BY pay_period_id"
        )
        print(tbl, "pay_period_id:", [r["pay_period_id"] for r in rows])
    except Exception as e:  # noqa: BLE001
        print(tbl, "ERR", e)

# Do cases for PP-2026-05 reference runs/workers we can count?
print("cases PP-2026-05 runs:", [r["payroll_run_id"] for r in f.query(
    "SELECT DISTINCT payroll_run_id FROM silver.payroll_case WHERE fabric_current_indicator=1 AND pay_period_id='PP-2026-05'")])
print("payroll_line rows for PP-2026-05:", f.query(
    "SELECT COUNT(*) c FROM silver.payroll_line WHERE pay_period_id='PP-2026-05'")[0]["c"])
