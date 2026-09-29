"""Selects sample vs Fabric data based on DATA_SOURCE."""
from __future__ import annotations

from typing import Any

from . import decision_store, fabric_data, sample
from .config import settings


def dashboard(period: str | None = None, frm: str | None = None, to: str | None = None) -> dict[str, Any]:
    return fabric_data.get_dashboard(period, frm, to) if settings.use_fabric else sample.DASHBOARD


def cases() -> list[dict[str, Any]]:
    rows = fabric_data.get_cases() if settings.use_fabric else sample.CASES
    decisions = decision_store.all_decisions()
    if not decisions:
        return rows
    # Reflect recorded human decisions in the case status.
    return [
        {**c, "status": decision_store.STATUS_FOR_ACTION.get(decisions[c["id"]]["action"], c["status"])}
        if c["id"] in decisions
        else c
        for c in rows
    ]


def case_detail(case_id: str) -> dict[str, Any] | None:
    detail = (
        fabric_data.get_case_detail(case_id)
        if settings.use_fabric
        else sample.case_detail(case_id)
    )
    if detail is None:
        return None
    recorded = decision_store.get(case_id)
    if recorded:
        detail = {
            **detail,
            "decision": recorded,
            "allowedActions": [],
            "status": decision_store.STATUS_FOR_ACTION.get(recorded["action"], detail.get("status")),
        }
    return detail


def exceptions() -> list[dict[str, Any]]:
    return fabric_data.get_exceptions() if settings.use_fabric else sample.EXCEPTIONS


def audit() -> list[dict[str, Any]]:
    events = fabric_data.get_audit() if settings.use_fabric else list(sample.AUDIT)
    decisions = decision_store.all_decisions()
    if not decisions:
        return events
    # Surface recorded human decisions (CP05) at the top of the governance log.
    decision_events = [
        {
            "id": f"DEC-{case_id}",
            "timestamp": d["decidedOn"],
            "caseRef": case_id,
            "actor": d["decidedBy"],
            "action": f"Human decision recorded: {d['action']}",
            "control": "CP05",
            "detail": d["rationale"],
        }
        for case_id, d in decisions.items()
    ]
    return decision_events + events


def insights(period: str | None = None, frm: str | None = None, to: str | None = None) -> dict[str, Any]:
    return fabric_data.get_insights(period, frm, to) if settings.use_fabric else sample.INSIGHTS


def periods() -> list[dict[str, Any]]:
    return fabric_data.get_periods() if settings.use_fabric else sample.PERIODS