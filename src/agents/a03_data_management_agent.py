"""
A03: Payroll Data Management Agent (Task Layer)
"""
import hashlib
import json
from typing import Dict, Any, List
from src.config.constants import AgentID
from src.fabric.repository import fabric_repo

class PayrollDataManagementAgent:
    def __init__(self):
        self.agent_id = AgentID.A03_DATA_MANAGEMENT.value
        self.name = "Payroll Data Management Agent"
        self.repo = fabric_repo

    def collect_payroll_dataset(self, payroll_run_id: str, period_id: str) -> Dict[str, Any]:
        """
        W01: Extracts Silver workforce & payroll tables from Fabric and computes a snapshot hash.
        """
        raw_dataset = self.repo.fetch_payroll_assurance_dataset(payroll_run_id, period_id)
        
        # Compute SHA-256 snapshot hash for lineage
        dataset_str = json.dumps(raw_dataset, sort_keys=True, default=str)
        snapshot_hash = hashlib.sha256(dataset_str.encode("utf-8")).hexdigest()

        return {
            "payroll_run_id": payroll_run_id,
            "period_id": period_id,
            "snapshot_hash": snapshot_hash,
            "workers": raw_dataset.get("workers", []),
            "current_pay": raw_dataset.get("current_pay", []),
            "prior_pay": raw_dataset.get("prior_pay", []),
            "source": raw_dataset.get("source", "UNKNOWN")
        }

    def execute_recalculation_and_commit(
        self,
        correction_id: str,
        worker_id: str,
        target_gross: float,
        target_tax_code: str,
        commit_token: str
    ) -> Dict[str, Any]:
        """
        W15 / W16: Performs authorized payroll recalculation upon valid commit token.
        """
        if not commit_token or not commit_token.startswith("TOKEN-"):
            raise PermissionError("Recalculation blocked: Invalid or missing commit token.")

        # Standard UK PAYE / NI / Pension recalculation logic (deterministic)
        calc_gross = round(target_gross, 2)
        if calc_gross <= 0:
            calc_tax = 0.0
            calc_ni = 0.0
            calc_pension = 0.0
            calc_net = 0.0
        else:
            calc_tax = round(calc_gross * 0.20, 2) # Standard basic rate simulation
            calc_ni = round(calc_gross * 0.08, 2)
            calc_pension = round(calc_gross * 0.05, 2)
            calc_net = round(calc_gross - (calc_tax + calc_ni + calc_pension), 2)

        return {
            "recalculation_id": f"RECALC-{correction_id}",
            "correction_id": correction_id,
            "worker_id": worker_id,
            "recalculated_gross": calc_gross,
            "recalculated_tax": calc_tax,
            "recalculated_ni": calc_ni,
            "recalculated_pension": calc_pension,
            "recalculated_net": calc_net,
            "applied_tax_code": target_tax_code or "1257L",
            "receipt_ref": f"REC-FABRIC-{hashlib.sha256(f'{worker_id}{calc_net}'.encode()).hexdigest()[:12].upper()}",
            "status": "COMMITTED_RECALCULATED"
        }
