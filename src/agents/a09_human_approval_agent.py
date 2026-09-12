"""
A09: Human Approval Control Agent (Control Layer)
"""
import uuid
from datetime import datetime
from typing import Dict, Any, List
from src.config.constants import AgentID
from src.core.governance_core import GovernanceCore

class HumanApprovalControlAgent:
    def __init__(self):
        self.agent_id = AgentID.A09_HUMAN_APPROVAL.value
        self.name = "Human Approval Control Agent"

    def authorize_correction(
        self,
        case_id: str,
        anomaly_id: str,
        correction_id: str,
        action: str,
        actor_identity: str,
        actor_role: str,
        preparer_identity: str,
        rationale: str
    ) -> Dict[str, Any]:
        """
        W13, W14, W15 / CP05 & CP06: Enforces SoD, validates human credentials, and issues single-use commit tokens.
        """
        # 1. Verify Segregation of Duties
        sod_check = GovernanceCore.verify_segregation_of_duties(
            actor_identity=actor_identity,
            actor_role=actor_role,
            action=action,
            preparer_identity=preparer_identity
        )

        if not sod_check["is_compliant"]:
            return {
                "authorized": False,
                "commit_token": None,
                "reason": f"Segregation of Duties failure: {'; '.join(sod_check['violations'])}",
                "sod_check": sod_check
            }

        # 2. Check Action Type
        if action.upper() == "APPROVE":
            commit_token = f"TOKEN-{uuid.uuid4().hex[:16].upper()}"
            return {
                "authorized": True,
                "commit_token": commit_token,
                "action": "APPROVED",
                "case_id": case_id,
                "anomaly_id": anomaly_id,
                "correction_id": correction_id,
                "approver_identity": actor_identity,
                "approver_role": actor_role,
                "rationale": rationale,
                "authorized_at": datetime.utcnow().isoformat(),
                "sod_check": sod_check
            }
        elif action.upper() == "REJECT":
            return {
                "authorized": False,
                "commit_token": None,
                "action": "REJECTED",
                "case_id": case_id,
                "anomaly_id": anomaly_id,
                "correction_id": correction_id,
                "approver_identity": actor_identity,
                "rationale": rationale,
                "status": "CORRECTION_REJECTED_REWORK_REQUIRED"
            }
        elif action.upper() == "ESCALATE":
            return {
                "authorized": False,
                "commit_token": None,
                "action": "ESCALATED",
                "case_id": case_id,
                "anomaly_id": anomaly_id,
                "escalated_to": "HEAD_OF_PAYROLL",
                "approver_identity": actor_identity,
                "rationale": rationale
            }
        else:
            return {
                "authorized": False,
                "commit_token": None,
                "action": action,
                "error": f"Unknown approval action '{action}'."
            }

    def sign_off_payroll_period(
        self,
        payroll_run_id: str,
        signoff_identity: str,
        signoff_role: str,
        declaration_text: str
    ) -> Dict[str, Any]:
        """
        Signs off the entire payroll period for compliance filing.
        """
        if signoff_role.upper() not in ("PAYROLL_CONTROLLER", "FINANCE_DIRECTOR"):
            return {
                "signed_off": False,
                "error": "Only Payroll Controller or Finance Director can sign off the payroll period."
            }

        return {
            "signed_off": True,
            "payroll_run_id": payroll_run_id,
            "signoff_identity": signoff_identity,
            "signoff_role": signoff_role,
            "declaration": declaration_text,
            "signed_off_at": datetime.utcnow().isoformat(),
            "signoff_token": f"SIGNOFF-{uuid.uuid4().hex[:12].upper()}"
        }
