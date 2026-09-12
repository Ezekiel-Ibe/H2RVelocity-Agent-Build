"""
A01: Payroll Assurance Workspace Agent (Experience Layer)
"""
from typing import Dict, Any, List
from src.config.constants import AgentID, ApprovalAction

class PayrollAssuranceWorkspaceAgent:
    def __init__(self):
        self.agent_id = AgentID.A01_WORKSPACE.value
        self.name = "Payroll Assurance Workspace Agent"

    def render_case_overview(
        self,
        case_id: str,
        payroll_run_id: str,
        risk_profile: Dict[str, Any],
        anomalies: List[Dict[str, Any]],
        recommendations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        W13: Formats and presents the full assurance workspace dashboard to the Controller.
        """
        return {
            "case_id": case_id,
            "payroll_run_id": payroll_run_id,
            "risk_score": risk_profile.get("risk_score"),
            "risk_band": risk_profile.get("risk_band"),
            "total_anomalies": len(anomalies),
            "anomalies_summary": [
                {
                    "anomaly_id": a.get("anomaly_id"),
                    "worker_id": a.get("worker_id"),
                    "class": a.get("anomaly_class"),
                    "severity": a.get("severity"),
                    "details": a.get("details")
                } for a in anomalies
            ],
            "recommendations": recommendations,
            "allowed_actions": [a.value for a in ApprovalAction],
            "requires_mandatory_rationale": True
        }

    def capture_controller_decision(
        self,
        case_id: str,
        anomaly_id: str,
        selected_option_id: str,
        action: str,
        approver_identity: str,
        approver_role: str,
        rationale: str
    ) -> Dict[str, Any]:
        """
        W14: Captures user review decision and rationale for submission to A09 approval control.
        """
        if not rationale or len(rationale.strip()) < 10:
            return {
                "success": False,
                "error": "A substantive business rationale (minimum 10 characters) is mandatory."
            }

        return {
            "success": True,
            "case_id": case_id,
            "anomaly_id": anomaly_id,
            "selected_option_id": selected_option_id,
            "action": action,
            "approver_identity": approver_identity,
            "approver_role": approver_role,
            "rationale": rationale.strip()
        }
