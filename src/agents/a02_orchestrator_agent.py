"""
A02: Payroll Assurance Orchestrator Agent (Orchestration Layer)
"""
from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime
from src.config.constants import AgentID, CaseState, WorkflowStep
from src.core.governance_core import GovernanceCore

class PayrollAssuranceOrchestratorAgent:
    def __init__(self):
        self.agent_id = AgentID.A02_ORCHESTRATOR.value
        self.name = "Payroll Assurance Orchestrator"

    def initialize_case(self, payroll_run_id: str, period_id: str) -> Dict[str, Any]:
        """
        Initializes workflow case with correlation tokens and initial state.
        """
        case_id = f"CASE-{payroll_run_id}-{uuid.uuid4().hex[:8].upper()}"
        correlation_id = str(uuid.uuid4())
        idempotency_key = f"IDEMP-{case_id}"

        return {
            "case_id": case_id,
            "payroll_run_id": payroll_run_id,
            "period_id": period_id,
            "case_state": CaseState.INITIATED.value,
            "current_step": WorkflowStep.W01_COLLECT_DATA.value,
            "correlation_id": correlation_id,
            "idempotency_key": idempotency_key,
            "created_at": datetime.utcnow().isoformat(),
            "history": [
                {
                    "step": WorkflowStep.W01_COLLECT_DATA.value,
                    "state": CaseState.INITIATED.value,
                    "timestamp": datetime.utcnow().isoformat()
                }
            ]
        }

    def transition_state(self, case_record: Dict[str, Any], next_state: str, next_step: str) -> Dict[str, Any]:
        """
        Authoritatively updates the case state and appends to the history trail.
        """
        case_record["case_state"] = next_state
        case_record["current_step"] = next_step
        case_record["history"].append({
            "step": next_step,
            "state": next_state,
            "timestamp": datetime.utcnow().isoformat()
        })
        return case_record

    def execute_closure_gate(
        self,
        case_record: Dict[str, Any],
        anomalies: List[Dict[str, Any]],
        decisions: List[Dict[str, Any]],
        validation_results: List[Dict[str, Any]],
        audit_pack: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        W20 / CP10: Evaluates final closure gate before completing workflow.
        """
        gate_result = GovernanceCore.validate_case_closure_gate(
            anomalies=anomalies,
            decisions=decisions,
            validation_results=validation_results,
            audit_pack=audit_pack
        )

        if gate_result["can_close"]:
            self.transition_state(case_record, CaseState.CLOSED.value, WorkflowStep.W20_CLOSE_CASE.value)
            case_record["closed_at"] = datetime.utcnow().isoformat()
            return {
                "success": True,
                "case_id": case_record["case_id"],
                "status": "CLOSED",
                "gate_result": gate_result
            }
        else:
            self.transition_state(case_record, CaseState.HELD_FOR_REVIEW.value, WorkflowStep.W20_CLOSE_CASE.value)
            return {
                "success": False,
                "case_id": case_record["case_id"],
                "status": "HELD_OPEN",
                "gate_result": gate_result
            }
