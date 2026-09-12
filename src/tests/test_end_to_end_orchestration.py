"""
End-to-End Orchestration Integration Test across A01 to A09 (W01 - W20).
"""
import pytest
from src.orchestration.workflow_runner import workflow_runner
from src.config.constants import CaseState

def test_full_payroll_assurance_workflow_execution():
    """
    Executes the entire multi-agent assurance pipeline from data ingestion to case closure.
    """
    result = workflow_runner.run_full_assurance_cycle(
        payroll_run_id="PR-2026-06",
        period_id="2026-06",
        human_approver_identity="payroll.controller@mbsukdemo.com",
        human_approver_role="PAYROLL_CONTROLLER"
    )

    assert result["success"] is True
    assert result["case_state"] == CaseState.CLOSED.value
    assert result["total_anomalies"] >= 7
    assert len(result["audit_manifest_hash"]) == 64
    assert result["period_signoff"]["signed_off"] is True
    assert result["closure_gate"]["success"] is True
