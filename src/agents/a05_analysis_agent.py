"""
A05: Payroll Analysis Agent (Insight Layer)
"""
from typing import Dict, Any, List
from src.config.constants import AgentID, AnomalyClass
from src.core.deterministic_rules import DeterministicCoreEngine

class PayrollAnalysisAgent:
    def __init__(self):
        self.agent_id = AgentID.A05_ANALYSIS.value
        self.name = "Payroll Analysis Agent"

    def assess_risk(self, anomalies: List[Dict[str, Any]], total_lines: int) -> Dict[str, Any]:
        """
        W04 / CP03: Computes mathematical risk score and risk band.
        """
        return DeterministicCoreEngine.calculate_period_risk_score(anomalies, total_lines)

    def explain_calculation(self, pay_item: Dict[str, Any]) -> Dict[str, Any]:
        """
        W06: Grounded gross-to-net pay breakdown trace.
        """
        return DeterministicCoreEngine.explain_pay_math(pay_item)

    def diagnose_root_cause_and_sor(self, anomaly: Dict[str, Any]) -> Dict[str, Any]:
        """
        W07 & W08: Identifies upstream root cause and system of record.
        """
        anom_class = anomaly.get("anomaly_class")

        diagnoses = {
            AnomalyClass.LEAVER_STILL_PAID.value: {
                "root_cause": "Termination event recorded in HCM after payroll cut-off or broken batch feed between HCM and Payroll.",
                "system_of_record": "HCM -> Payroll Interface",
                "failure_process_area": "Offboarding Synchronization"
            },
            AnomalyClass.JOINER_NOT_PAID.value: {
                "root_cause": "New joiner onboarding checklist incomplete or bank details submitted post cut-off.",
                "system_of_record": "HCM Onboarding / First-Pay Gate",
                "failure_process_area": "Onboarding Enrolment"
            },
            AnomalyClass.UNEXPLAINED_VARIANCE.value: {
                "root_cause": "Manual base pay adjustment entered directly in payroll without HCM compensation workflow approval.",
                "system_of_record": "HCM Compensation / Payroll Entry",
                "failure_process_area": "Compensation Administration"
            },
            AnomalyClass.MISSING_TAX_CODE.value: {
                "root_cause": "HMRC P6/P45 tax notice not received or failed automated ingestion into payroll statutory tax table.",
                "system_of_record": "HMRC RTI / Payroll Statutory Table",
                "failure_process_area": "Statutory Tax Ingestion"
            },
            AnomalyClass.NEGATIVE_NET_PAY.value: {
                "root_cause": "Voluntary deductions (e.g. salary sacrifice or loan repayment) exceed total monthly gross pay.",
                "system_of_record": "Benefits / Payroll Deductions Engine",
                "failure_process_area": "Benefits Deduction Limits"
            },
            AnomalyClass.DUPLICATE_PAY_RECORD.value: {
                "root_cause": "Re-run of interface batch script created duplicate payroll line for worker.",
                "system_of_record": "Payroll Interface Staging",
                "failure_process_area": "Batch Interface Idempotency"
            },
            AnomalyClass.UNAPPROVED_PAY_CHANGE.value: {
                "root_cause": "Direct database update or unapproved operator override on pay item fields without workflow sign-off.",
                "system_of_record": "Payroll Master Audit Log",
                "failure_process_area": "Security & Change Control"
            }
        }

        default_diag = {
            "root_cause": "Operational variance requiring SME review.",
            "system_of_record": "Payroll Engine",
            "failure_process_area": "General Payroll Operations"
        }

        return diagnoses.get(anom_class, default_diag)
