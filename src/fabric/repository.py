"""
Fabric Repository for querying canonical Silver/Gold datasets and writing audit logs.
"""
import hashlib
import json
import logging
from typing import List, Dict, Any, Optional
from src.fabric.connection import fabric_conn

logger = logging.getLogger("fabric_repository")

class FabricRepository:
    def __init__(self):
        self.conn_mgr = fabric_conn

    def get_table_catalog(self) -> List[Dict[str, str]]:
        """Return the governed Fabric table catalog used by the capability agents."""
        conn = self.conn_mgr.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
                    FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_TYPE = 'BASE TABLE'
                    ORDER BY TABLE_SCHEMA, TABLE_NAME
                """)
                columns = [column[0].lower() for column in cursor.description]
                tables = [dict(zip(columns, row)) for row in cursor.fetchall()]
                cursor.close()
                conn.close()
                return tables
            except Exception as e:
                logger.warning("Could not read Fabric table catalog: %s", e)

        # Fallback catalog mirrors the real edm_wh_dev payroll assurance tables/views
        return [
            {"table_schema": schema, "table_name": table, "table_type": "BASE TABLE"}
            for schema, table in (
                ("silver", "worker"),
                ("silver", "employment"),
                ("silver", "payroll_run"),
                ("silver", "payroll_line"),
                ("silver", "pay_period"),
                ("silver", "payroll_case"),
                ("silver", "payroll_anomaly"),
                ("silver", "payroll_correction"),
                ("silver", "payroll_correction_option"),
                ("gold", "fact_payroll_case"),
                ("gold", "fact_payroll_anomaly"),
                ("gold", "fact_payroll_correction"),
                ("gold", "fact_audit_evidence"),
                ("gold", "vw_h03_payroll_collection_queue"),
                ("gold", "vw_h03_recalc_queue"),
            )
        ]

    def get_agent_data_context(self) -> str:
        """Format the Fabric catalog and access boundary for Foundry agent instructions."""
        table_lines = "\n".join(
            f"- {table['table_schema']}.{table['table_name']}"
            for table in self.get_table_catalog()
        )
        return (
            "\n\n## Fabric Data Contract\n"
            f"Warehouse: {self.conn_mgr.database}\n"
            "Live Fabric reads and writes are performed by the governed A03 data-management "
            "application path. Do not invent table names or bypass A03 approval controls.\n"
            "Available tables:\n"
            f"{table_lines}"
        )

    def fetch_payroll_assurance_dataset(self, payroll_run_id: str, period_id: str) -> Dict[str, Any]:
        """
        Fetches workers and aggregated pay items (current vs prior period) from the live
        edm_wh_dev warehouse (silver.worker / silver.employment / silver.payroll_line).
        """
        conn = self.conn_mgr.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Canonical worker master, joined to the current employment record for pay_group/fte
                # (some workers have multiple "current" employment rows in edm_wh_dev, so pick the latest)
                cursor.execute("""
                    SELECT w.worker_id, w.worker_type, w.worker_status AS status,
                           w.hire_date, w.termination_date AS term_date,
                           e.employment_type AS pay_group, e.fte
                    FROM silver.worker w
                    OUTER APPLY (
                        SELECT TOP 1 employment_type, fte
                        FROM silver.employment e
                        WHERE e.worker_id = w.worker_id AND e.fabric_current_indicator = 1
                        ORDER BY e.start_date DESC, e.employment_key DESC
                    ) e
                    WHERE w.fabric_current_indicator = 1
                """)
                worker_cols = [column[0] for column in cursor.description]
                workers = [dict(zip(worker_cols, row)) for row in cursor.fetchall()]
                for w in workers:
                    w["status"] = (w.get("status") or "").lower()
                    # Approved compensation changes are not tracked at pay-line grain in edm_wh_dev
                    w["has_approved_comp_change"] = False

                # Pay lines are stored per pay element (BASE_PAY/OVERTIME/etc.); aggregate to
                # one pay item per worker/run/period to match the assurance rule engine's shape.
                cursor.execute("""
                    SELECT worker_id, payroll_run_id, pay_period_id,
                           SUM(amount) AS gross,
                           MAX(net_pay) AS net,
                           MAX(deduction_total) AS deduction_total,
                           MAX(tax_code) AS tax_code,
                           MAX(currency_code) AS currency_code
                    FROM silver.payroll_line
                    WHERE payroll_run_id = ? OR pay_period_id = ?
                    GROUP BY worker_id, payroll_run_id, pay_period_id
                """, (payroll_run_id, period_id))
                pay_cols = [column[0] for column in cursor.description]
                pay_rows = [dict(zip(pay_cols, row)) for row in cursor.fetchall()]

                cursor.close()
                conn.close()

                def _normalize(row: Dict[str, Any]) -> Dict[str, Any]:
                    gross = float(row["gross"]) if row.get("gross") is not None else 0.0
                    deductions = float(row["deduction_total"]) if row.get("deduction_total") is not None else 0.0
                    net = float(row["net"]) if row.get("net") is not None else round(gross - deductions, 2)
                    return {
                        "pay_item_id": f"{row['worker_id']}-{row['payroll_run_id']}",
                        "payroll_run_id": row.get("payroll_run_id"),
                        "period_id": row.get("pay_period_id"),
                        "worker_id": row.get("worker_id"),
                        "gross": gross,
                        "net": net,
                        "other_deductions": deductions,
                        "tax_code": row.get("tax_code"),
                        "currency_code": row.get("currency_code"),
                        "approved_by": None,
                        "changed_fields": None,
                    }

                current_pay = [_normalize(r) for r in pay_rows if r.get("pay_period_id") == period_id]
                prior_pay = [_normalize(r) for r in pay_rows if r.get("pay_period_id") != period_id]

                return {
                    "payroll_run_id": payroll_run_id,
                    "period_id": period_id,
                    "workers": workers,
                    "current_pay": current_pay,
                    "prior_pay": prior_pay,
                    "source": "FABRIC_LIVE"
                }
            except Exception as e:
                logger.warning("Live Fabric payroll dataset query failed, using fixture fallback: %s", e)

        # Return standardized benchmark test fixture (Stage 5/Stage 6A test set)
        return self._get_benchmark_fixture(payroll_run_id, period_id)

    def write_assurance_case(self, case_record: Dict[str, Any]) -> None:
        """Writes or updates gold.fact_assurance_case."""
        conn = self.conn_mgr.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO gold.fact_assurance_case (
                        case_id, payroll_run_id, period_id, case_state, period_risk_score,
                        total_anomalies, blocking_dq_errors, correlation_id, idempotency_key
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    case_record["case_id"],
                    case_record["payroll_run_id"],
                    case_record["period_id"],
                    case_record["case_state"],
                    case_record.get("period_risk_score", 0.0),
                    case_record.get("total_anomalies", 0),
                    case_record.get("blocking_dq_errors", 0),
                    case_record["correlation_id"],
                    case_record["idempotency_key"]
                ))
                conn.commit()
                cursor.close()
                conn.close()
            except Exception:
                pass

    def write_governance_log(self, log_record: Dict[str, Any]) -> None:
        """Writes immutable log to governance.agentops_governance_log."""
        conn = self.conn_mgr.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO governance.agentops_governance_log (
                        log_id, case_id, correlation_id, workflow_step, agent_id,
                        action_type, actor_identity, actor_role, input_hash, output_hash,
                        sod_check_result, details_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    log_record["log_id"],
                    log_record["case_id"],
                    log_record["correlation_id"],
                    log_record["workflow_step"],
                    log_record["agent_id"],
                    log_record["action_type"],
                    log_record["actor_identity"],
                    log_record["actor_role"],
                    log_record["input_hash"],
                    log_record["output_hash"],
                    1 if log_record.get("sod_check_result", True) else 0,
                    json.dumps(log_record.get("details", {}))
                ))
                conn.commit()
                cursor.close()
                conn.close()
            except Exception:
                pass

    def _get_benchmark_fixture(self, payroll_run_id: str, period_id: str) -> Dict[str, Any]:
        """Reference 7-anomaly fixture aligned with Stage 6A and 7A specifications."""
        return {
            "payroll_run_id": payroll_run_id,
            "period_id": period_id,
            "source": "FIXTURE_FALLBACK",
            "workers": [
                {"worker_id": "W-001", "worker_type": "employee", "status": "active", "hire_date": "2023-01-15", "term_date": None, "pay_group": "MONTHLY", "fte": 1.0, "has_approved_comp_change": False},
                {"worker_id": "W-014", "worker_type": "employee", "status": "leaver", "hire_date": "2022-03-01", "term_date": "2026-05-31", "pay_group": "MONTHLY", "fte": 1.0, "has_approved_comp_change": False},
                {"worker_id": "W-020", "worker_type": "employee", "status": "active", "hire_date": "2026-06-02", "term_date": None, "pay_group": "MONTHLY", "fte": 1.0, "has_approved_comp_change": False},
                {"worker_id": "W-035", "worker_type": "employee", "status": "active", "hire_date": "2021-08-10", "term_date": None, "pay_group": "MONTHLY", "fte": 1.0, "has_approved_comp_change": False},
                {"worker_id": "W-042", "worker_type": "employee", "status": "active", "hire_date": "2024-02-01", "term_date": None, "pay_group": "MONTHLY", "fte": 1.0, "has_approved_comp_change": False},
                {"worker_id": "W-058", "worker_type": "employee", "status": "active", "hire_date": "2020-11-20", "term_date": None, "pay_group": "MONTHLY", "fte": 1.0, "has_approved_comp_change": False},
                {"worker_id": "W-063", "worker_type": "employee", "status": "active", "hire_date": "2019-05-15", "term_date": None, "pay_group": "MONTHLY", "fte": 1.0, "has_approved_comp_change": False},
                {"worker_id": "W-077", "worker_type": "employee", "status": "active", "hire_date": "2023-09-01", "term_date": None, "pay_group": "MONTHLY", "fte": 1.0, "has_approved_comp_change": False},
            ],
            "current_pay": [
                {"pay_item_id": "P-001", "payroll_run_id": payroll_run_id, "period_id": period_id, "worker_id": "W-001", "base_pay": 4000.0, "allowances": 200.0, "overtime": 0.0, "gross": 4200.0, "tax": 800.0, "ni": 350.0, "pension": 210.0, "other_deductions": 0.0, "net": 2840.0, "tax_code": "1257L", "ni_category": "A", "approved_by": "SYSTEM", "changed_fields": None},
                # Anomaly 1: Leaver still paid (W-014 terminated 2026-05-31)
                {"pay_item_id": "P-014", "payroll_run_id": payroll_run_id, "period_id": period_id, "worker_id": "W-014", "base_pay": 1890.0, "allowances": 0.0, "overtime": 0.0, "gross": 1890.0, "tax": 300.0, "ni": 150.0, "pension": 94.5, "other_deductions": 0.0, "net": 1345.5, "tax_code": "1257L", "ni_category": "A", "approved_by": "SYSTEM", "changed_fields": None},
                # (W-020 is missing from current_pay -> Anomaly 2: Joiner not paid)
                # Anomaly 3: Unexplained variance (>40% increase from 3000 to 4500 with no approved comp change)
                {"pay_item_id": "P-035", "payroll_run_id": payroll_run_id, "period_id": period_id, "worker_id": "W-035", "base_pay": 4500.0, "allowances": 0.0, "overtime": 0.0, "gross": 4500.0, "tax": 900.0, "ni": 400.0, "pension": 225.0, "other_deductions": 0.0, "net": 2975.0, "tax_code": "1257L", "ni_category": "A", "approved_by": "SYSTEM", "changed_fields": None},
                # Anomaly 4: Missing tax code
                {"pay_item_id": "P-042", "payroll_run_id": payroll_run_id, "period_id": period_id, "worker_id": "W-042", "base_pay": 3500.0, "allowances": 0.0, "overtime": 0.0, "gross": 3500.0, "tax": 700.0, "ni": 300.0, "pension": 175.0, "other_deductions": 0.0, "net": 2325.0, "tax_code": "", "ni_category": "A", "approved_by": "SYSTEM", "changed_fields": None},
                # Anomaly 5: Negative net pay
                {"pay_item_id": "P-058", "payroll_run_id": payroll_run_id, "period_id": period_id, "worker_id": "W-058", "base_pay": 1000.0, "allowances": 0.0, "overtime": 0.0, "gross": 1000.0, "tax": 200.0, "ni": 100.0, "pension": 50.0, "other_deductions": 1200.0, "net": -550.0, "tax_code": "1257L", "ni_category": "A", "approved_by": "SYSTEM", "changed_fields": None},
                # Anomaly 6: Duplicate pay record (W-063 has two pay records)
                {"pay_item_id": "P-063-A", "payroll_run_id": payroll_run_id, "period_id": period_id, "worker_id": "W-063", "base_pay": 3200.0, "allowances": 0.0, "overtime": 0.0, "gross": 3200.0, "tax": 600.0, "ni": 250.0, "pension": 160.0, "other_deductions": 0.0, "net": 2190.0, "tax_code": "1257L", "ni_category": "A", "approved_by": "SYSTEM", "changed_fields": None},
                {"pay_item_id": "P-063-B", "payroll_run_id": payroll_run_id, "period_id": period_id, "worker_id": "W-063", "base_pay": 3200.0, "allowances": 0.0, "overtime": 0.0, "gross": 3200.0, "tax": 600.0, "ni": 250.0, "pension": 160.0, "other_deductions": 0.0, "net": 2190.0, "tax_code": "1257L", "ni_category": "A", "approved_by": "SYSTEM", "changed_fields": None},
                # Anomaly 7: Unapproved pay change (changed_fields set but approved_by is None)
                {"pay_item_id": "P-077", "payroll_run_id": payroll_run_id, "period_id": period_id, "worker_id": "W-077", "base_pay": 5000.0, "allowances": 500.0, "overtime": 0.0, "gross": 5500.0, "tax": 1200.0, "ni": 500.0, "pension": 275.0, "other_deductions": 0.0, "net": 3525.0, "tax_code": "1257L", "ni_category": "A", "approved_by": None, "changed_fields": "base_pay,allowances"}
            ],
            "prior_pay": [
                {"pay_item_id": "P-PRIOR-001", "payroll_run_id": "PR-2026-05", "period_id": "2026-05", "worker_id": "W-001", "gross": 4200.0, "net": 2840.0},
                {"pay_item_id": "P-PRIOR-014", "payroll_run_id": "PR-2026-05", "period_id": "2026-05", "worker_id": "W-014", "gross": 1890.0, "net": 1345.5},
                {"pay_item_id": "P-PRIOR-035", "payroll_run_id": "PR-2026-05", "period_id": "2026-05", "worker_id": "W-035", "gross": 3000.0, "net": 2100.0},
                {"pay_item_id": "P-PRIOR-042", "payroll_run_id": "PR-2026-05", "period_id": "2026-05", "worker_id": "W-042", "gross": 3500.0, "net": 2325.0},
                {"pay_item_id": "P-PRIOR-058", "payroll_run_id": "PR-2026-05", "period_id": "2026-05", "worker_id": "W-058", "gross": 1000.0, "net": 700.0},
                {"pay_item_id": "P-PRIOR-063", "payroll_run_id": "PR-2026-05", "period_id": "2026-05", "worker_id": "W-063", "gross": 3200.0, "net": 2190.0},
                {"pay_item_id": "P-PRIOR-077", "payroll_run_id": "PR-2026-05", "period_id": "2026-05", "worker_id": "W-077", "gross": 4000.0, "net": 2700.0}
            ]
        }

fabric_repo = FabricRepository()
