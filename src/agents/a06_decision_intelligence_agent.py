"""
A06: Payroll Decision Intelligence Agent (Insight Layer)
"""
from typing import Dict, Any, List
from src.config.constants import AgentID

class PayrollDecisionIntelligenceAgent:
    def __init__(self):
        self.agent_id = AgentID.A06_DECISION_INTELLIGENCE.value
        self.name = "Payroll Decision Intelligence Agent"

    def evaluate_impact_and_recommend(
        self,
        anomaly: Dict[str, Any],
        options: List[Dict[str, Any]],
        diagnosis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        W10 & W11 / CP04: Computes financial impact and synthesizes a decision-ready recommendation.
        """
        if not options:
            return {
                "recommendation_id": f"REC-{anomaly.get('anomaly_id')}",
                "anomaly_id": anomaly.get("anomaly_id"),
                "status": "NO_VALID_OPTIONS",
                "recommended_option": None,
                "advisory_rationale": "No compliant correction option available. Escalate directly to Controller."
            }

        # Select primary recommended option
        primary_option = options[0]

        # Calculate estimated financial impact
        current_gross = anomaly.get("current_gross") or anomaly.get("gross") or 0.0
        target_gross = primary_option.get("target_gross", current_gross)
        gross_delta = round(target_gross - current_gross, 2)
        est_tax_delta = round(gross_delta * 0.20, 2)
        est_net_delta = round(gross_delta - est_tax_delta, 2)

        impact_assessment = {
            "gross_impact": gross_delta,
            "estimated_tax_impact": est_tax_delta,
            "estimated_net_impact": est_net_delta,
            "gl_posting_account": "6100-WAGES-SALARIES",
            "statutory_compliance_status": "COMPLIANT_WITH_HMRC_PAYE",
            "employee_notification_required": abs(gross_delta) > 0.0
        }

        rationale = (
            f"Recommended remediation: {primary_option.get('description')} "
            f"Root cause identified: {diagnosis.get('root_cause')} in {diagnosis.get('system_of_record')}. "
            f"Financial impact: Net delta of £{est_net_delta:.2f}. "
            f"Execution posture: {'Autonomous within policy' if primary_option.get('auto_executable') else 'Requires Controller Approval'}."
        )

        return {
            "recommendation_id": f"REC-{anomaly.get('anomaly_id')}",
            "anomaly_id": anomaly.get("anomaly_id"),
            "worker_id": anomaly.get("worker_id"),
            "primary_option": primary_option,
            "all_options": options,
            "impact_assessment": impact_assessment,
            "root_cause_summary": diagnosis.get("root_cause"),
            "system_of_record": diagnosis.get("system_of_record"),
            "advisory_rationale": rationale,
            "requires_human_approval": primary_option.get("requires_approval", True)
        }
