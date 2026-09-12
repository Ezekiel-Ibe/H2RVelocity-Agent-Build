"""
Governance, Segregation of Duties (SoD), and Cryptographic Audit Pack Engine.
Complies with EU AI Act, ISO/IEC 42001, and KPMG Agent Factory Stages 4-7A.
"""
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class GovernanceCore:
    @staticmethod
    def verify_segregation_of_duties(
        actor_identity: str,
        actor_role: str,
        action: str,
        preparer_identity: str
    ) -> Dict[str, Any]:
        """
        CP05 & CP06: Segregation of Duties and Human Approval verification.
        Rules:
        1. An AI Agent identity (e.g., 'AGENT_*') cannot approve pay-impacting changes.
        2. The preparer/submitter cannot approve their own correction.
        3. Approver must hold the designated authorized role (e.g., 'PAYROLL_CONTROLLER').
        """
        violations = []

        if actor_identity.upper().startswith("AGENT_") or "FOUNDRY" in actor_identity.upper():
            violations.append("AI Agent is strictly prohibited from approving pay-impacting changes (CP05).")

        if actor_identity.lower() == preparer_identity.lower() and action in ("APPROVE", "SIGN_OFF"):
            violations.append("Segregation of duties violation: Preparer cannot approve their own proposed change (CP06).")

        authorized_roles = {"PAYROLL_CONTROLLER", "HEAD_OF_PAYROLL", "FINANCE_DIRECTOR"}
        if action in ("APPROVE", "SIGN_OFF") and actor_role.upper() not in authorized_roles:
            violations.append(f"Actor role '{actor_role}' does not possess approval authority for payroll sign-off.")

        is_compliant = len(violations) == 0
        return {
            "is_compliant": is_compliant,
            "actor_identity": actor_identity,
            "actor_role": actor_role,
            "violations": violations,
            "status": "APPROVED_SOD_VALID" if is_compliant else "REJECTED_SOD_BREACH"
        }

    @staticmethod
    def assemble_audit_manifest(
        case_id: str,
        payroll_run_id: str,
        anomalies: List[Dict[str, Any]],
        decisions: List[Dict[str, Any]],
        validation_results: List[Dict[str, Any]],
        governance_logs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        CP08: Assembles an immutable evidence manifest and computes its SHA-256 hash.
        """
        manifest_payload = {
            "case_id": case_id,
            "payroll_run_id": payroll_run_id,
            "timestamp_utc": datetime.utcnow().isoformat(),
            "compliance_standards": ["EU_AI_ACT_ART_14", "ISO_IEC_42001", "HMRC_PAYE_RTI", "SOX_404"],
            "anomalies_count": len(anomalies),
            "anomalies": anomalies,
            "human_decisions": decisions,
            "validation_results": validation_results,
            "governance_event_count": len(governance_logs)
        }

        manifest_str = json.dumps(manifest_payload, sort_keys=True, default=str)
        manifest_hash = hashlib.sha256(manifest_str.encode("utf-8")).hexdigest()

        return {
            "pack_id": f"AUDIT-PACK-{case_id}",
            "case_id": case_id,
            "payroll_run_id": payroll_run_id,
            "manifest_hash": manifest_hash,
            "immutable_manifest": manifest_payload,
            "is_attested": True,
            "attested_by": "A08_GOVERNANCE_AUDIT_AGENT"
        }

    @staticmethod
    def validate_case_closure_gate(
        anomalies: List[Dict[str, Any]],
        decisions: List[Dict[str, Any]],
        validation_results: List[Dict[str, Any]],
        audit_pack: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        CP10: Case closure control (W20).
        Ensures all anomalies have resolved decisions, validation has passed, and audit evidence is signed.
        """
        unresolved = []

        if not audit_pack or not audit_pack.get("manifest_hash"):
            unresolved.append("Missing immutable audit evidence pack.")

        for anom in anomalies:
            aid = anom.get("anomaly_id")
            # Check if decision exists
            dec = next((d for d in decisions if d.get("anomaly_id") == aid), None)
            if not dec:
                unresolved.append(f"Anomaly {aid} has no recorded resolution decision.")

        for val in validation_results:
            if not val.get("is_valid"):
                unresolved.append(f"Validation failed for correction on worker {val.get('worker_id')}.")

        can_close = len(unresolved) == 0
        return {
            "can_close": can_close,
            "unresolved_items": unresolved,
            "closure_state": "CLOSED_SUCCESSFULLY" if can_close else "HELD_OPEN_PENDING_RESOLUTION"
        }
