"""
AgentOps Telemetry & OpenTelemetry Tracer.
Monitors multi-agent execution, token usage, drift detection, and EU AI Act audit trails.
"""
import time
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("agentops_telemetry")

class AgentOpsTracer:
    def __init__(self):
        self.active_traces: Dict[str, Any] = {}
        self.metrics = {
            "total_runs": 0,
            "total_tokens": 0,
            "total_cost_gbp": 0.0,
            "drift_alerts": 0,
            "sod_violations": 0
        }

    def start_span(self, workflow_step: str, agent_id: str, case_id: str) -> str:
        """Starts a tracked telemetry span."""
        span_id = f"SPAN-{workflow_step}-{agent_id}-{int(time.time()*1000)}"
        self.active_traces[span_id] = {
            "workflow_step": workflow_step,
            "agent_id": agent_id,
            "case_id": case_id,
            "start_time": time.time()
        }
        return span_id

    def end_span(
        self,
        span_id: str,
        tokens: int = 0,
        cost_gbp: float = 0.0,
        success: bool = True,
        drift_signal: bool = False
    ) -> Dict[str, Any]:
        """Ends span and aggregates metrics."""
        span = self.active_traces.pop(span_id, None)
        if not span:
            return {}

        duration_ms = (time.time() - span["start_time"]) * 1000
        self.metrics["total_runs"] += 1
        self.metrics["total_tokens"] += tokens
        self.metrics["total_cost_gbp"] += cost_gbp
        if drift_signal:
            self.metrics["drift_alerts"] += 1

        record = {
            "span_id": span_id,
            "workflow_step": span["workflow_step"],
            "agent_id": span["agent_id"],
            "case_id": span["case_id"],
            "duration_ms": round(duration_ms, 2),
            "tokens": tokens,
            "cost_gbp": cost_gbp,
            "success": success,
            "drift_detected": drift_signal
        }
        return record

    def get_fleet_telemetry_summary(self) -> Dict[str, Any]:
        """Returns fleet metrics summary for A08 Governance Agent."""
        return {
            "fleet_metrics": self.metrics,
            "active_spans_count": len(self.active_traces),
            "iso_42001_conformance": "CONFORMANT" if self.metrics["drift_alerts"] == 0 else "ATTENTION_REQUIRED"
        }

agentops = AgentOpsTracer()
