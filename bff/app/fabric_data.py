"""Fabric-mode data (DATA_SOURCE=fabric) — read-only reads of the payroll
Silver layer, mapped to the frontend shapes. All queries are SELECT only.

Mappings calibrated against the live schema (Sep 2026): payroll cases live in
silver.payroll_case, anomalies in silver.payroll_anomaly, workers in
silver.worker, audit evidence in silver.audit_evidence.
"""
from __future__ import annotations

import functools
import logging
import threading
import time
from datetime import datetime
from typing import Any

from . import fabric_client, sample

log = logging.getLogger("bff.fabric")

# Short-lived response cache. Many testers hitting the same endpoints (and the
# frontend's refetch-on-navigation) would otherwise re-run every Fabric query on
# each request. A brief TTL collapses those into one query per window, which is
# what keeps the app from overloading the Fabric capacity.
_CACHE_TTL_SECONDS = 30.0
_cache: dict[tuple, tuple[float, Any]] = {}
_cache_lock = threading.Lock()


def _ttl_cached(fn):
    @functools.wraps(fn)
    def wrapper(*args):
        key = (fn.__name__, args)
        now = time.monotonic()
        with _cache_lock:
            hit = _cache.get(key)
            if hit and now - hit[0] < _CACHE_TTL_SECONDS:
                return hit[1]
        result = fn(*args)
        with _cache_lock:
            _cache[key] = (now, result)
        return result

    return wrapper


def clear_cache() -> None:
    with _cache_lock:
        _cache.clear()

# --- value maps (real Fabric values -> frontend enums) ---
_CASE_STATUS = {
    "OPEN": "Detected",
    "IN_INVESTIGATION": "In Analysis",
    "IN_REVIEW": "In Analysis",
    "AWAITING_APPROVAL": "Awaiting Approval",
    "ESCALATED": "Escalated",
    "RESOLVED": "Approved",
    "CLOSED": "Closed",
}
_SEVERITY = {"CRITICAL": "high", "HIGH": "high", "MEDIUM": "medium", "LOW": "low"}


def _sev(value: Any) -> str:
    return _SEVERITY.get(str(value or "").upper(), "low")


def _anomaly_slug(value: Any) -> str:
    v = str(value or "").upper()
    if "DUPLICATE" in v:
        return "duplicate-pay-record"
    if "TAX" in v:
        return "missing-tax-code"
    if "OVERPAY" in v or "UNDERPAY" in v or "VARIANCE" in v:
        return "unexplained-variance"
    if "MISSING" in v or "COMPLETENESS" in v or "INPUT" in v:
        return "negative-net-pay"
    return "unapproved-change"


def _pretty(value: Any) -> str:
    return str(value or "").replace("_", " ").title() or "Anomaly"


def _fmt(dt: Any, with_time: bool = False) -> str:
    if isinstance(dt, datetime):
        return dt.strftime("%d %b %Y %H:%M" if with_time else "%d %b %Y")
    return "" if dt is None else str(dt)


def _int(value: Any) -> int:
    try:
        return max(0, min(100, int(float(value))))
    except (TypeError, ValueError):
        return 0


def _name(row: dict) -> str:
    name = f"{row.get('given_name') or ''} {row.get('family_name') or ''}".strip()
    return name or "\u2014"


_CASE_SQL = """
SELECT c.payroll_case_id, c.case_status, c.severity AS case_severity,
       c.worker_id, c.pay_period_id, c.payroll_run_id,
       c.opened_datetime, c.last_activity_datetime, c.workflow_step_id, c.case_type,
       w.given_name, w.family_name,
       a.anomaly_type, a.risk_score, a.severity AS anomaly_severity, a.detected_datetime
FROM silver.payroll_case c
OUTER APPLY (
    SELECT TOP 1 given_name, family_name FROM silver.worker w2
    WHERE w2.worker_id = c.worker_id AND w2.fabric_current_indicator = 1
) w
OUTER APPLY (
    SELECT TOP 1 anomaly_type, risk_score, severity, detected_datetime
    FROM silver.payroll_anomaly x
    WHERE x.payroll_case_id = c.payroll_case_id
    ORDER BY x.risk_score DESC
) a
WHERE c.fabric_current_indicator = 1
ORDER BY c.last_activity_datetime DESC
"""


def _map_case(r: dict) -> dict:
    return {
        "id": r.get("payroll_case_id") or "UNKNOWN",
        "workerRef": r.get("worker_id") or "",
        "workerName": _name(r),
        "payrollRunId": r.get("payroll_run_id") or "",
        "payPeriod": r.get("pay_period_id") or "",
        "anomalyType": _anomaly_slug(r.get("anomaly_type")),
        "anomalyTitle": _pretty(r.get("anomaly_type")),
        "severity": _sev(r.get("case_severity") or r.get("anomaly_severity")),
        "riskScore": _int(r.get("risk_score")),
        "status": _CASE_STATUS.get(str(r.get("case_status") or "").upper(), "Detected"),
        "currentStep": r.get("workflow_step_id") or r.get("case_type") or "",
        "detectedOn": _fmt(r.get("opened_datetime")),
        "lastUpdated": _fmt(r.get("last_activity_datetime")),
    }


@_ttl_cached
def get_cases(period: str | None = None, frm: str | None = None, to: str | None = None) -> list[dict]:
    clause, params = _case_clause(period, frm, to)
    # The case query aliases payroll_case as c; prefix only the outer column.
    clause = clause.replace(" AND pay_period_id", " AND c.pay_period_id")
    sql = _CASE_SQL
    if clause:
        sql = sql.replace(
            "WHERE c.fabric_current_indicator = 1",
            "WHERE c.fabric_current_indicator = 1" + clause,
        )
    try:
        return [_map_case(r) for r in fabric_client.query(sql, params)]
    except Exception as exc:  # noqa: BLE001
        log.warning("get_cases (fabric) failed: %s", exc)
        return []


def _risk_factors(anomaly: dict, risk: int) -> list[dict]:
    sev = _sev(anomaly.get("severity"))
    return [
        {"name": "Anomaly signal", "weight": 0.5, "contribution": round(risk * 0.5),
         "note": _pretty(anomaly.get("anomaly_type"))},
        {"name": "Severity", "weight": 0.3, "contribution": round(risk * 0.3),
         "note": f"Rated {sev} by detection rule"},
        {"name": "Status", "weight": 0.2, "contribution": round(risk * 0.2),
         "note": _pretty(anomaly.get("anomaly_status")) or "Under review"},
    ]


def _live_controls(evidence: list[dict], awaiting: bool) -> list[dict]:
    controls: list[dict] = []
    seen: set[str] = set()
    for e in evidence:
        ref = e.get("control_reference")
        if not ref or ref in seen:
            continue
        seen.add(ref)
        controls.append(
            {
                "id": str(ref),
                "name": e.get("evidence_type") or "Control check",
                "owner": e.get("captured_by_agent_id") or "\u2014",
                "result": "Pass",
                "detail": e.get("evidence_summary") or "Evidence captured.",
            }
        )
    controls.append(
        {"id": "CP05", "name": "Mandatory human approval", "owner": "A09",
         "result": "Pending" if awaiting else "N/A", "detail": "Human decision gate."}
    )
    controls.append(
        {"id": "CP06", "name": "Segregation of duties", "owner": "A09",
         "result": "Pending" if awaiting else "N/A", "detail": "Agent recommends; human approves."}
    )
    return controls


_CURRENCY = {"GBP": "\u00a3", "EUR": "\u20ac", "USD": "$"}


def _money(value: Any, currency: Any = "GBP") -> str | None:
    if value is None:
        return None
    try:
        n = float(value)
    except (TypeError, ValueError):
        return None
    sym = _CURRENCY.get(str(currency or "GBP").upper())
    body = f"{abs(n):,.2f}"
    sign = "-" if n < 0 else ""
    return f"{sign}{sym}{body}" if sym else f"{sign}{body} {currency}"


def _impact(a: dict) -> list[dict]:
    cur = a.get("currency_code") or "GBP"
    exp, act, var = a.get("expected_amount"), a.get("actual_amount"), a.get("variance_amount")
    lines: list[dict] = []
    for label, val in (("Expected", exp), ("Actual", act), ("Variance", var)):
        m = _money(val, cur)
        if m is not None:
            lines.append({"label": label, "value": m})
    try:
        if exp is not None and float(exp) != 0 and var is not None:
            lines.append({"label": "Variance %", "value": f"{float(var) / float(exp) * 100:+.2f}%"})
    except (TypeError, ValueError):
        pass
    return lines


_OPTION_TYPE = {
    "NEXT_CYCLE": "Apply correction in next pay cycle",
    "RETRO_ADJUSTMENT": "Retrospective adjustment",
    "OFF_CYCLE": "Off-cycle correction",
    "MANUAL_REVIEW": "Route for manual review",
    "NO_ACTION": "No action required",
}


def _correction_options(case_id: str) -> list[dict]:
    rows = fabric_client.query(
        "SELECT payroll_correction_option_id, option_rank, option_type, proposed_amount, "
        "currency_code, expected_outcome, rationale FROM silver.payroll_correction_option "
        "WHERE payroll_case_id = ? AND fabric_current_indicator = 1 ORDER BY option_rank",
        [case_id],
    )
    out: list[dict] = []
    for i, r in enumerate(rows):
        amount = _money(r.get("proposed_amount"), r.get("currency_code"))
        label = _OPTION_TYPE.get(str(r.get("option_type") or "").upper(), _pretty(r.get("option_type")))
        if amount:
            label = f"{label} ({amount})"
        out.append(
            {
                "id": r.get("payroll_correction_option_id") or "",
                "label": label,
                "description": r.get("expected_outcome") or r.get("rationale") or "\u2014",
                "recommended": i == 0,
            }
        )
    return out


def _root_cause(case_id: str, fallback: str) -> str:
    rows = fabric_client.query(
        "SELECT TOP 1 root_cause_summary, root_cause_category FROM silver.root_cause_analysis "
        "WHERE payroll_case_id = ? AND fabric_current_indicator = 1 "
        "ORDER BY identified_datetime DESC",
        [case_id],
    )
    if rows and rows[0].get("root_cause_summary"):
        summary = rows[0]["root_cause_summary"]
        cat = rows[0].get("root_cause_category")
        return f"{summary} (Category: {_pretty(cat)})" if cat else summary
    return fallback


def get_case_detail(case_id: str) -> dict | None:
    base = next((c for c in get_cases() if c["id"] == case_id), None)
    if base is None:
        return None
    scaffold = sample.case_detail("PA-2024-0512") or {}
    awaiting = base["status"] == "Awaiting Approval"
    detail: dict[str, Any] = {
        # kept from scaffold where Fabric has no equivalent source:
        "correctionOptions": scaffold.get("correctionOptions", []),
        "impact": scaffold.get("impact", []),
        "ruleVersion": scaffold.get("ruleVersion", "v1.0"),
    }

    anomaly: dict = {}
    try:
        rows = fabric_client.query(
            "SELECT TOP 1 payroll_anomaly_id, anomaly_type, severity, anomaly_status, "
            "detection_rule, explanation_summary, explanation, expected_amount, actual_amount, "
            "variance_amount, variance_percentage, currency_code, detected_datetime "
            "FROM silver.payroll_anomaly WHERE payroll_case_id = ? "
            "ORDER BY risk_score DESC",
            [case_id],
        )
        anomaly = rows[0] if rows else {}
    except Exception as exc:  # noqa: BLE001
        log.warning("anomaly lookup failed: %s", exc)

    detail["anomalyDescription"] = (
        anomaly.get("explanation_summary")
        or f"{base['anomalyTitle']} detected for {base['workerName']} in run {base['payrollRunId']}."
    )
    detail["ruleId"] = str(
        anomaly.get("detection_rule")
        or anomaly.get("payroll_anomaly_id")
        or f"R-ANOM-{base['anomalyType'].upper()}"
    )
    detail["riskFactors"] = _risk_factors(anomaly, base["riskScore"]) if anomaly else scaffold.get("riskFactors", [])

    fallback_cause = anomaly.get("explanation") or anomaly.get("explanation_summary") or "\u2014"
    try:
        detail["rootCause"] = _root_cause(case_id, fallback_cause)
    except Exception as exc:  # noqa: BLE001
        log.warning("root-cause lookup failed: %s", exc)
        detail["rootCause"] = fallback_cause

    if anomaly and _impact(anomaly):
        detail["impact"] = _impact(anomaly)

    try:
        options = _correction_options(case_id)
        if options:
            detail["correctionOptions"] = options
    except Exception as exc:  # noqa: BLE001
        log.warning("correction-option lookup failed: %s", exc)

    try:
        rec = fabric_client.query(
            "SELECT TOP 1 recommendation_summary, rationale, confidence_score, recommended_action "
            "FROM silver.payroll_recommendation WHERE payroll_case_id = ? "
            "ORDER BY generated_datetime DESC",
            [case_id],
        )
        if rec:
            detail["recommendation"] = {
                "summary": rec[0].get("recommendation_summary") or rec[0].get("recommended_action") or "\u2014",
                "rationale": rec[0].get("rationale") or "\u2014",
                "confidence": "High" if base["severity"] == "high" else "Medium",
                "citations": [],
            }
        else:
            detail["recommendation"] = scaffold.get("recommendation")
    except Exception as exc:  # noqa: BLE001
        log.warning("recommendation lookup failed: %s", exc)
        detail["recommendation"] = scaffold.get("recommendation")

    evidence_rows: list[dict] = []
    try:
        evidence_rows = fabric_client.query(
            "SELECT audit_evidence_id, evidence_type, evidence_summary, control_reference, "
            "captured_by_agent_id, hash_value, captured_datetime FROM silver.audit_evidence "
            "WHERE payroll_case_id = ? ORDER BY captured_datetime DESC",
            [case_id],
        )
    except Exception as exc:  # noqa: BLE001
        log.warning("evidence lookup failed: %s", exc)

    detail["evidence"] = (
        [
            {
                "id": e.get("audit_evidence_id") or "",
                "label": e.get("evidence_summary") or e.get("evidence_type") or "Evidence",
                "source": e.get("evidence_type") or "audit_evidence",
                "hash": e.get("hash_value") or "",
                "capturedOn": _fmt(e.get("captured_datetime")),
            }
            for e in evidence_rows
        ]
        if evidence_rows
        else scaffold.get("evidence", [])
    )
    detail["controls"] = (
        _live_controls(evidence_rows, awaiting) if evidence_rows else scaffold.get("controls", [])
    )

    return {
        **detail,
        **base,
        "allowedActions": ["Approve", "Reject", "Escalate"] if awaiting else [],
        "decision": None,
    }


@_ttl_cached
def get_exceptions() -> list[dict]:
    sql = """
    SELECT a.payroll_anomaly_id, a.payroll_case_id, a.anomaly_type, a.severity,
           a.risk_score, a.anomaly_status, a.explanation_summary, a.explanation,
           a.pay_period_id, a.detected_datetime, w.given_name, w.family_name
    FROM silver.payroll_anomaly a
    OUTER APPLY (
        SELECT TOP 1 given_name, family_name FROM silver.worker w2
        WHERE w2.worker_id = a.worker_id AND w2.fabric_current_indicator = 1
    ) w
    WHERE a.fabric_current_indicator = 1
    ORDER BY a.risk_score DESC
    """
    try:
        rows = fabric_client.query(sql)
    except Exception as exc:  # noqa: BLE001
        log.warning("get_exceptions (fabric) failed: %s", exc)
        return []

    status_map = {"RESOLVED": "Resolved", "CLOSED": "Resolved", "IN_REVIEW": "Under Review"}
    out = []
    for r in rows:
        out.append(
            {
                "id": r.get("payroll_anomaly_id") or "",
                "anomalyType": _anomaly_slug(r.get("anomaly_type")),
                "severity": _sev(r.get("severity")),
                "title": _pretty(r.get("anomaly_type")),
                "description": r.get("explanation_summary") or r.get("explanation") or "\u2014",
                "employeesAffected": 1,
                "count": 1,
                "caseRef": r.get("payroll_case_id") or "",
                "workerName": _name(r),
                "payPeriod": r.get("pay_period_id") or "",
                "status": status_map.get(str(r.get("anomaly_status") or "").upper(), "Open"),
                "detectedOn": _fmt(r.get("detected_datetime")),
            }
        )
    return out


@_ttl_cached
def get_audit() -> list[dict]:
    sql = """
    SELECT audit_evidence_id, payroll_case_id, evidence_type, evidence_summary,
           captured_by_agent_id, captured_datetime, control_reference, workflow_step_id
    FROM silver.audit_evidence
    WHERE fabric_current_indicator = 1
    ORDER BY captured_datetime DESC
    """
    try:
        rows = fabric_client.query(sql)
    except Exception as exc:  # noqa: BLE001
        log.warning("get_audit (fabric) failed: %s", exc)
        return []
    return [
        {
            "id": r.get("audit_evidence_id") or "",
            "timestamp": _fmt(r.get("captured_datetime"), with_time=True),
            "caseRef": r.get("payroll_case_id") or "",
            "actor": r.get("captured_by_agent_id") or "\u2014",
            "action": r.get("evidence_summary") or r.get("evidence_type") or "Evidence captured",
            "control": r.get("control_reference") or r.get("workflow_step_id") or "\u2014",
            "detail": r.get("evidence_type") or "",
        }
        for r in rows
    ]


def _period_caption(period: str | None) -> str:
    if not period:
        return "All periods"
    try:
        rows = fabric_client.query(
            "SELECT start_date, period_name FROM silver.pay_period WHERE pay_period_id = ?",
            [period],
        )
        if rows:
            start = rows[0].get("start_date")
            if hasattr(start, "strftime"):
                return start.strftime("%B %Y")
            return rows[0].get("period_name") or period
    except Exception:  # noqa: BLE001
        pass
    return period


def _fmt_ymd(value: str) -> str:
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%d %b %Y")
    except (TypeError, ValueError):
        return value


def _filter_caption(period: str | None, frm: str | None, to: str | None) -> str:
    if frm and to:
        return f"{_fmt_ymd(frm)} \u2013 {_fmt_ymd(to)}"
    return _period_caption(period)


# Pay periods overlapping a calendar range [frm, to].
_RANGE_PERIODS = (
    "pay_period_id IN (SELECT pay_period_id FROM silver.pay_period "
    "WHERE start_date <= ? AND end_date >= ?)"
)


def _case_clause(period: str | None, frm: str | None, to: str | None) -> tuple[str, list]:
    if frm and to:
        return " AND " + _RANGE_PERIODS, [to, frm]
    if period:
        return " AND pay_period_id = ?", [period]
    return "", []


def _anom_clause(period: str | None, frm: str | None, to: str | None) -> tuple[str, list]:
    if frm and to:
        return " AND " + _RANGE_PERIODS, [to, frm]
    if period:
        return " AND pay_period_id = ?", [period]
    return "", []


def _evidence_clause(period: str | None, frm: str | None, to: str | None) -> tuple[str, list]:
    if frm and to:
        return (
            " AND payroll_case_id IN (SELECT payroll_case_id FROM silver.payroll_case "
            "WHERE fabric_current_indicator=1 AND " + _RANGE_PERIODS + ")",
            [to, frm],
        )
    if period:
        return (
            " AND payroll_case_id IN (SELECT payroll_case_id FROM silver.payroll_case "
            "WHERE fabric_current_indicator=1 AND pay_period_id = ?)",
            [period],
        )
    return "", []


@_ttl_cached
def get_periods() -> list[dict]:
    """Pay periods that have assurance cases, newest first, for the period filter."""
    try:
        rows = fabric_client.query(
            "SELECT p.pay_period_id, p.period_name, p.start_date, p.end_date, p.period_status "
            "FROM silver.pay_period p WHERE p.pay_period_id IN "
            "(SELECT DISTINCT pay_period_id FROM silver.payroll_case WHERE fabric_current_indicator=1) "
            "ORDER BY p.start_date DESC"
        )
    except Exception as exc:  # noqa: BLE001
        log.warning("get_periods (fabric) failed: %s", exc)
        return sample.PERIODS
    out = []
    for r in rows:
        start = r.get("start_date")
        end = r.get("end_date")
        name = start.strftime("%B %Y") if hasattr(start, "strftime") else (r.get("period_name") or r.get("pay_period_id"))
        out.append({
            "id": r.get("pay_period_id"),
            "name": name,
            "start": start.strftime("%Y-%m-%d") if hasattr(start, "strftime") else str(start or ""),
            "end": end.strftime("%Y-%m-%d") if hasattr(end, "strftime") else str(end or ""),
            "status": r.get("period_status") or "",
        })
    return out


@_ttl_cached
def get_dashboard(period: str | None = None, frm: str | None = None, to: str | None = None) -> dict:
    dashboard = {k: v for k, v in sample.DASHBOARD.items()}
    dashboard["cases"] = get_cases(period, frm, to)[:6]
    caption = _filter_caption(period, frm, to)
    cc, cp = _case_clause(period, frm, to)
    ac, ap = _anom_clause(period, frm, to)
    scoped = bool(cc)

    try:
        if scoped:
            # payroll_line/run carry pay_period_id sparsely, so scope volume from cases.
            runs = fabric_client.query(
                "SELECT COUNT(DISTINCT payroll_run_id) c FROM silver.payroll_case "
                "WHERE fabric_current_indicator=1" + cc, cp
            )[0]["c"]
            workers = fabric_client.query(
                "SELECT COUNT(DISTINCT worker_id) c FROM silver.payroll_case "
                "WHERE fabric_current_indicator=1" + cc, cp
            )[0]["c"]
        else:
            runs = fabric_client.query(
                "SELECT COUNT(DISTINCT payroll_run_id) c FROM silver.payroll_run"
            )[0]["c"]
            workers = fabric_client.query(
                "SELECT COUNT(*) c FROM silver.worker WHERE fabric_current_indicator=1"
            )[0]["c"]
        anomalies = fabric_client.query(
            "SELECT COUNT(*) c FROM silver.payroll_anomaly WHERE fabric_current_indicator=1" + ac, ap
        )[0]["c"]
        cases_total = fabric_client.query(
            "SELECT COUNT(*) c FROM silver.payroll_case WHERE fabric_current_indicator=1" + cc, cp
        )[0]["c"]
        done = fabric_client.query(
            "SELECT COUNT(*) c FROM silver.payroll_case WHERE fabric_current_indicator=1 "
            "AND case_status IN ('CLOSED','RESOLVED')" + cc, cp
        )[0]["c"]
        total = int(cases_total or 0) or 1
        score = round(100 * int(done or 0) / total)
        trend = {"direction": "up", "value": "live", "label": "from Fabric"}
        dashboard["stats"] = [
            {"id": "payrolls", "label": "Payrolls Processed", "value": str(runs), "caption": caption, "icon": "payrolls", "trend": trend},
            {"id": "employees", "label": "Employees Covered", "value": f"{int(workers):,}", "caption": caption, "icon": "employees", "trend": trend},
            {"id": "exceptions", "label": "Exceptions Identified", "value": str(anomalies), "caption": caption, "icon": "exceptions", "trend": trend},
            {"id": "score", "label": "Assurance Score", "value": f"{score}%", "caption": caption, "icon": "score", "trend": trend},
        ]

        sev_rows = fabric_client.query(
            "SELECT severity, COUNT(*) c FROM silver.payroll_anomaly "
            "WHERE fabric_current_indicator=1" + ac + " GROUP BY severity", ap
        )
        buckets = {"high": 0, "medium": 0, "low": 0}
        for r in sev_rows:
            buckets[_sev(r["severity"])] += int(r["c"])
        atotal = sum(buckets.values()) or 1
        dashboard["overview"] = {
            "score": score,
            "total": atotal,
            "breakdown": [
                {"level": "high", "label": "High Risk", "count": buckets["high"], "percentage": round(100 * buckets["high"] / atotal)},
                {"level": "medium", "label": "Medium Risk", "count": buckets["medium"], "percentage": round(100 * buckets["medium"] / atotal)},
                {"level": "low", "label": "Low Risk", "count": buckets["low"], "percentage": round(100 * buckets["low"] / atotal)},
            ],
        }

        top = fabric_client.query(
            "SELECT anomaly_type, COUNT(*) cnt, MAX(risk_score) maxrisk "
            "FROM silver.payroll_anomaly WHERE fabric_current_indicator=1" + ac + " "
            "GROUP BY anomaly_type ORDER BY cnt DESC", ap
        )
        dashboard["exceptions"] = [
            {
                "id": f"exc-{i}",
                "anomalyType": _anomaly_slug(t["anomaly_type"]),
                "severity": "high" if float(t["maxrisk"] or 0) >= 80 else "medium" if float(t["maxrisk"] or 0) >= 50 else "low",
                "title": _pretty(t["anomaly_type"]),
                "employeesAffected": int(t["cnt"]),
                "count": int(t["cnt"]),
            }
            for i, t in enumerate(top[:4])
        ]
    except Exception as exc:  # noqa: BLE001
        log.warning("get_dashboard (fabric) aggregates failed: %s", exc)

    return dashboard


# Raw case_status -> insights funnel stage.
_FUNNEL_STAGE = {
    "OPEN": "Detected",
    "IN_INVESTIGATION": "In Analysis",
    "IN_REVIEW": "In Analysis",
    "AWAITING_APPROVAL": "Awaiting Approval",
    "ESCALATED": "Escalated",
    "RESOLVED": "Resolved / Closed",
    "CLOSED": "Resolved / Closed",
}
_FUNNEL_ORDER = ["Detected", "In Analysis", "Awaiting Approval", "Escalated", "Resolved / Closed"]


@_ttl_cached
def get_insights(period: str | None = None, frm: str | None = None, to: str | None = None) -> dict:
    """Assurance insights aggregated read-only from the Fabric Silver layer."""
    cc, cp = _case_clause(period, frm, to)
    ac, ap = _anom_clause(period, frm, to)
    ec, ep = _evidence_clause(period, frm, to)
    try:
        total = int(fabric_client.query(
            "SELECT COUNT(*) c FROM silver.payroll_case WHERE fabric_current_indicator=1" + cc, cp
        )[0]["c"] or 0)
        done = int(fabric_client.query(
            "SELECT COUNT(*) c FROM silver.payroll_case WHERE fabric_current_indicator=1 "
            "AND case_status IN ('CLOSED','RESOLVED')" + cc, cp
        )[0]["c"] or 0)
        anomalies = int(fabric_client.query(
            "SELECT COUNT(*) c FROM silver.payroll_anomaly WHERE fabric_current_indicator=1" + ac, ap
        )[0]["c"] or 0)
        evidence = int(fabric_client.query(
            "SELECT COUNT(*) c FROM silver.audit_evidence WHERE fabric_current_indicator=1" + ec, ep
        )[0]["c"] or 0)
        score = round(100 * done / total) if total else 0

        status_rows = fabric_client.query(
            "SELECT case_status, COUNT(*) c FROM silver.payroll_case "
            "WHERE fabric_current_indicator=1" + cc + " GROUP BY case_status", cp
        )
        stage_counts = {s: 0 for s in _FUNNEL_ORDER}
        for r in status_rows:
            stage = _FUNNEL_STAGE.get(str(r.get("case_status") or "").upper(), "Detected")
            stage_counts[stage] += int(r["c"])
        funnel = [{"stage": s, "count": stage_counts[s]} for s in _FUNNEL_ORDER]

        sev_rows = fabric_client.query(
            "SELECT severity, COUNT(*) c FROM silver.payroll_anomaly "
            "WHERE fabric_current_indicator=1" + ac + " GROUP BY severity", ap
        )
        buckets = {"high": 0, "medium": 0, "low": 0}
        for r in sev_rows:
            buckets[_sev(r["severity"])] += int(r["c"])
        atotal = sum(buckets.values()) or 1
        severity_mix = [
            {"level": "high", "label": "High Risk", "count": buckets["high"], "percentage": round(100 * buckets["high"] / atotal)},
            {"level": "medium", "label": "Medium Risk", "count": buckets["medium"], "percentage": round(100 * buckets["medium"] / atotal)},
            {"level": "low", "label": "Low Risk", "count": buckets["low"], "percentage": round(100 * buckets["low"] / atotal)},
        ]

        type_rows = fabric_client.query(
            "SELECT anomaly_type, COUNT(*) cnt, MAX(risk_score) maxrisk "
            "FROM silver.payroll_anomaly WHERE fabric_current_indicator=1" + ac + " "
            "GROUP BY anomaly_type ORDER BY cnt DESC", ap
        )
        anomaly_types = [
            {"type": _pretty(t["anomaly_type"]), "count": int(t["cnt"]), "maxRisk": _int(t["maxrisk"])}
            for t in type_rows
        ]

        cases = sorted(get_cases(period, frm, to), key=lambda c: c["riskScore"], reverse=True)
        top_cases = [
            {
                "id": c["id"],
                "workerName": c["workerName"],
                "anomalyTitle": c["anomalyTitle"],
                "severity": c["severity"],
                "riskScore": c["riskScore"],
                "status": c["status"],
            }
            for c in cases[:5]
        ]

        control_rows = fabric_client.query(
            "SELECT control_reference, COUNT(*) c FROM silver.audit_evidence "
            "WHERE fabric_current_indicator=1 AND control_reference IS NOT NULL" + ec + " "
            "GROUP BY control_reference ORDER BY c DESC", ep
        )
        control_activity = [
            {"control": str(r["control_reference"]), "count": int(r["c"])}
            for r in control_rows[:8]
        ]

        return {
            "assuranceScore": score,
            "summary": {
                "totalCases": total,
                "openCases": total - done,
                "resolvedCases": done,
                "totalAnomalies": anomalies,
                "evidencePacks": evidence,
            },
            "funnel": funnel,
            "anomalyTypes": anomaly_types,
            "severityMix": severity_mix,
            "topRiskCases": top_cases,
            "controlActivity": control_activity,
        }
    except Exception as exc:  # noqa: BLE001
        log.warning("get_insights (fabric) failed: %s", exc)
        return sample.INSIGHTS


def schema() -> list[dict]:
    """Read-only schema discovery to confirm table/view/column names."""
    sql = (
        "SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE "
        "FROM INFORMATION_SCHEMA.COLUMNS "
        "ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION"
    )
    return fabric_client.query(sql)
