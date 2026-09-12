"""
A07: Payroll Quality Control Agent (Control Layer)
"""
from typing import Dict, Any
from src.config.constants import AgentID
from src.core.deterministic_rules import DeterministicCoreEngine

class PayrollQualityControlAgent:
    def __init__(self):
        self.agent_id = AgentID.A07_QUALITY_CONTROL.value
        self.name = "Payroll Quality Control Agent"

    def validate_input_data(self, dataset: Dict[str, Any]) -> Dict[str, Any]:
        """
        W02 / CP01: Input completeness and schema validation.
        """
        return DeterministicCoreEngine.validate_input_completeness(dataset)

    def validate_post_correction_outcome(
        self,
        worker_id: str,
        original_net: float,
        expected_net: float,
        actual_recalculated_net: float
    ) -> Dict[str, Any]:
        """
        W17 / CP07: Post-recalculation outcome verification.
        """
        result = DeterministicCoreEngine.validate_recalculation_outcome(
            original_net=original_net,
            expected_net=expected_net,
            actual_recalc_net=actual_recalculated_net
        )
        result["worker_id"] = worker_id
        result["attested_by"] = self.agent_id
        return result
