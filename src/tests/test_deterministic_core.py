"""
Unit Tests for Deterministic Calculation and Governance Cores.
Aligned with KPMG Agent Factory Stage 6B / Stage 7A Test Catalogue.
"""
import pytest
from src.core.deterministic_rules import DeterministicCoreEngine
from src.core.governance_core import GovernanceCore
from src.config.constants import AnomalyClass, Severity
from src.fabric.repository import fabric_repo

def test_ut01_input_completeness_valid():
    """UT-01: Valid dataset passes completeness check."""
    fixture = fabric_repo.fetch_payroll_assurance_dataset("PR-2026-06", "2026-06")
    res = DeterministicCoreEngine.validate_input_completeness(fixture)
    assert res["is_valid"] is True
    assert len(res["blocking_errors"]) == 0

def test_ut02_input_completeness_missing_data():
    """UT-02: Missing worker id or pay items blocks analysis."""
    bad_data = {"workers": [{"worker_id": None}], "current_pay": []}
    res = DeterministicCoreEngine.validate_input_completeness(bad_data)
    assert res["is_valid"] is False
    assert len(res["blocking_errors"]) > 0

def test_ut03_detect_all_seven_anomalies():
    """UT-03: Verifies exact detection of all 7 core anomaly classes."""
    fixture = fabric_repo.fetch_payroll_assurance_dataset("PR-2026-06", "2026-06")
    anomalies = DeterministicCoreEngine.detect_anomalies(
        workers=fixture["workers"],
        current_pay=fixture["current_pay"],
        prior_pay=fixture["prior_pay"],
        period_id="2026-06"
    )

    detected_classes = set(a["anomaly_class"] for a in anomalies)

    assert AnomalyClass.LEAVER_STILL_PAID.value in detected_classes
    assert AnomalyClass.JOINER_NOT_PAID.value in detected_classes
    assert AnomalyClass.UNEXPLAINED_VARIANCE.value in detected_classes
    assert AnomalyClass.MISSING_TAX_CODE.value in detected_classes
    assert AnomalyClass.NEGATIVE_NET_PAY.value in detected_classes
    assert AnomalyClass.DUPLICATE_PAY_RECORD.value in detected_classes
    assert AnomalyClass.UNAPPROVED_PAY_CHANGE.value in detected_classes

def test_ut04_calculate_risk_score():
    """UT-04: Verifies deterministic risk scoring and threshold classification."""
    fixture = fabric_repo.fetch_payroll_assurance_dataset("PR-2026-06", "2026-06")
    anomalies = DeterministicCoreEngine.detect_anomalies(
        workers=fixture["workers"],
        current_pay=fixture["current_pay"],
        prior_pay=fixture["prior_pay"],
        period_id="2026-06"
    )
    total_lines = len(fixture["current_pay"])
    risk = DeterministicCoreEngine.calculate_period_risk_score(anomalies, total_lines)

    assert risk["risk_score"] > 0.50
    assert risk["risk_band"] in ("HIGH", "MEDIUM")
    assert risk["total_anomalies"] == len(anomalies)

def test_ut05_explain_pay_math():
    """UT-05: Exact gross-to-net arithmetic check."""
    pay_item = {
        "worker_id": "W-001",
        "base_pay": 4000.0,
        "allowances": 200.0,
        "overtime": 0.0,
        "tax": 800.0,
        "ni": 350.0,
        "pension": 210.0,
        "other_deductions": 0.0,
        "net": 2840.0,
        "tax_code": "1257L",
        "ni_category": "A"
    }
    trace = DeterministicCoreEngine.explain_pay_math(pay_item)
    assert trace["arithmetic_match"] is True
    assert trace["computed_net"] == 2840.0
    assert trace["gross"] == 4200.0

def test_ut06_post_correction_validation_outcome():
    """UT-06: CP07 post-correction validation."""
    pass_res = DeterministicCoreEngine.validate_recalculation_outcome(100.0, 500.0, 500.0)
    assert pass_res["is_valid"] is True

    fail_res = DeterministicCoreEngine.validate_recalculation_outcome(100.0, 500.0, 480.0)
    assert fail_res["is_valid"] is False

def test_ut07_sod_preparer_cannot_approve():
    """UT-07: CP06 Segregation of duties blocks self-approval."""
    res = GovernanceCore.verify_segregation_of_duties(
        actor_identity="controller.jane@mbsukdemo.com",
        actor_role="PAYROLL_CONTROLLER",
        action="APPROVE",
        preparer_identity="controller.jane@mbsukdemo.com"
    )
    assert res["is_compliant"] is False
    assert "Segregation of duties violation" in res["violations"][0]

def test_ut08_sod_agent_cannot_approve():
    """UT-08: CP05 AI Agent is strictly prohibited from approving pay."""
    res = GovernanceCore.verify_segregation_of_duties(
        actor_identity="AGENT_A06_DECISION_INTEL",
        actor_role="AI_AGENT",
        action="APPROVE",
        preparer_identity="USER_ANALYST"
    )
    assert res["is_compliant"] is False
    assert "AI Agent is strictly prohibited" in res["violations"][0]

def test_ut09_immutable_audit_manifest_hash():
    """UT-09: CP08 generates cryptographic SHA-256 hash for audit pack."""
    pack = GovernanceCore.assemble_audit_manifest(
        case_id="CASE-001",
        payroll_run_id="PR-2026-06",
        anomalies=[{"anomaly_id": "A1"}],
        decisions=[{"decision": "APPROVED"}],
        validation_results=[{"is_valid": True}],
        governance_logs=[{"event": "START"}]
    )
    assert len(pack["manifest_hash"]) == 64
    assert pack["is_attested"] is True
