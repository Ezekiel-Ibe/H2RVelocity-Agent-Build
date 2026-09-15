"""
A04: Payroll Exception Processing Agent (Task Layer)
"""
from typing import Dict, Any, List, Optional
from src.config.constants import AgentID, AnomalyClass
from src.core.deterministic_rules import DeterministicCoreEngine

class PayrollExceptionProcessingAgent:
    def __init__(self):
        self.agent_id = AgentID.A04_EXCEPTION_PROCESSING.value
        self.name = "Payroll Exception Processing Agent"

    def detect_exceptions(self, validated_dataset: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        W03 / CP02: Executes 7-class deterministic anomaly detection.
        """
        workers = validated_dataset.get("workers", [])
        current_pay = validated_dataset.get("current_pay", [])
        prior_pay = validated_dataset.get("prior_pay", [])
        period_id = validated_dataset.get("period_id", "CURRENT")

        return DeterministicCoreEngine.detect_anomalies(
            workers=workers,
            current_pay=current_pay,
            prior_pay=prior_pay,
            period_id=period_id
        )

    def generate_resolution_options(self, anomaly: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        W09: Generates compliant remediation options.
        """
        return DeterministicCoreEngine.generate_correction_options(anomaly)

    def trigger_lifecycle_handover(self, anomaly: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Cross-capability handover to Onboarding & Lifecycle Agent for joiner/leaver anomalies.
        """
        anom_class = anomaly.get("anomaly_class")
        if anom_class in (AnomalyClass.LEAVER_STILL_PAID.value, AnomalyClass.JOINER_NOT_PAID.value):
            return {
                "handover_id": f"HO-LIFECYCLE-{anomaly.get('worker_id')}",
                "target_agent": "Onboarding & Lifecycle Agent",
                "worker_id": anomaly.get("worker_id"),
                "event_type": "LEAVER_SYNC" if anom_class == AnomalyClass.LEAVER_STILL_PAID.value else "JOINER_ENROL",
                "status": "DISPATCHED_TO_LIFECYCLE"
            }
        return None
