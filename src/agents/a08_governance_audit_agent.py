"""
A08: Payroll Governance & Audit Agent (AgentOps / Control Layer)
"""
from typing import Dict, Any, List
import uuid
from datetime import datetime
from src.config.constants import AgentID
from src.core.governance_core import GovernanceCore
from src.fabric.repository import fabric_repo

class PayrollGovernanceAuditAgent:
    def __init__(self):
        self.agent_id = AgentID.A08_GOVERNANCE_AUDIT.value
        self.name = "Payroll Governance & Audit Agent (AgentOps)"
        self.repo = fabric_repo
        self._governance_events: List[Dict[str, Any]] = []

    def log_governance_event(
        self,
        case_id: str,
        correlation_id: str,
        workflow_step: str,
        acting_agent: str,
        action_type: str,
        actor_identity: str,
        actor_role: str,
        input_hash: str,
        output_hash: str,
        sod_ok: bool = True,
        details: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        W19 / CP09: Records structured governance event with cryptographic input/output hashes.
        """
        event = {
            "log_id": f"LOG-{uuid.uuid4().hex[:12].upper()}",
            "case_id": case_id,
            "correlation_id": correlation_id,
            "workflow_step": workflow_step,
            "agent_id": acting_agent,
            "action_type": action_type,
            "actor_identity": actor_identity,
            "actor_role": actor_role,
            "input_hash": input_hash,
            "output_hash": output_hash,
            "sod_check_result": sod_ok,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        self._governance_events.append(event)
        self.repo.write_governance_log(event)
        return event

    def compile_audit_evidence_pack(
        self,
        case_id: str,
        payroll_run_id: str,
        anomalies: List[Dict[str, Any]],
        decisions: List[Dict[str, Any]],
        validation_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        W18 / CP08: Compiles immutable evidence pack and generates cryptographic manifest.
        """
        audit_pack = GovernanceCore.assemble_audit_manifest(
            case_id=case_id,
            payroll_run_id=payroll_run_id,
            anomalies=anomalies,
            decisions=decisions,
            validation_results=validation_results,
            governance_logs=self._governance_events
        )
        return audit_pack

    def attest_closure_readiness(
        self,
        anomalies: List[Dict[str, Any]],
        decisions: List[Dict[str, Any]],
        validation_results: List[Dict[str, Any]],
        audit_pack: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        W20: Prepares closure attestation for the Orchestrator.
        """
        gate = GovernanceCore.validate_case_closure_gate(
            anomalies=anomalies,
            decisions=decisions,
            validation_results=validation_results,
            audit_pack=audit_pack
        )
        return {
            "is_ready_for_closure": gate["can_close"],
            "manifest_hash": audit_pack.get("manifest_hash"),
            "unresolved_items": gate["unresolved_items"],
            "attested_at": datetime.utcnow().isoformat(),
            "attested_by": self.agent_id
        }
