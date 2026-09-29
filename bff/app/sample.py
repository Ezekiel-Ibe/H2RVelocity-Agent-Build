"""Built-in sample payloads (DATA_SOURCE=sample). Shapes match the frontend Zod
contracts so the app renders end-to-end before Fabric columns are confirmed.
Synthetic development data only."""

CASES = [
    {
        "id": "PA-2024-0512",
        "workerRef": "WKR-10233",
        "workerName": "A. Okafor",
        "payrollRunId": "PR-2024-05-UK",
        "payPeriod": "May 2024",
        "anomalyType": "leaver-still-paid",
        "anomalyTitle": "Leaver still paid",
        "severity": "high",
        "riskScore": 88,
        "status": "Awaiting Approval",
        "currentStep": "W13 Review Recommendation",
        "detectedOn": "27 May 2024",
        "lastUpdated": "28 May 2024",
    },
    {
        "id": "PA-2024-0509",
        "workerRef": "WKR-10044",
        "workerName": "S. Kaur",
        "payrollRunId": "PR-2024-05-UK",
        "payPeriod": "May 2024",
        "anomalyType": "duplicate-pay-record",
        "anomalyTitle": "Duplicate pay record",
        "severity": "medium",
        "riskScore": 61,
        "status": "Awaiting Approval",
        "currentStep": "W14 Approve, Reject or Escalate",
        "detectedOn": "26 May 2024",
        "lastUpdated": "27 May 2024",
    },
    {
        "id": "PA-2024-0498",
        "workerRef": "WKR-10120",
        "workerName": "L. Chen",
        "payrollRunId": "PR-2024-04-UK",
        "payPeriod": "Apr 2024",
        "anomalyType": "joiner-not-paid",
        "anomalyTitle": "Joiner not paid",
        "severity": "high",
        "riskScore": 74,
        "status": "Closed",
        "currentStep": "W20 Close Case",
        "detectedOn": "29 Apr 2024",
        "lastUpdated": "30 Apr 2024",
    },
]

DASHBOARD = {
    "stats": [
        {"id": "payrolls", "label": "Payrolls Processed", "value": "24", "caption": "This period", "icon": "payrolls", "trend": {"direction": "up", "value": "20%", "label": "vs last period"}},
        {"id": "employees", "label": "Employees Covered", "value": "3,842", "caption": "This period", "icon": "employees", "trend": {"direction": "up", "value": "15%", "label": "vs last period"}},
        {"id": "exceptions", "label": "Exceptions Identified", "value": "56", "caption": "This period", "icon": "exceptions", "trend": {"direction": "down", "value": "10%", "label": "vs last period"}},
        {"id": "score", "label": "Assurance Score", "value": "92%", "caption": "This period", "icon": "score", "trend": {"direction": "up", "value": "8%", "label": "vs last period"}},
    ],
    "overview": {
        "score": 92,
        "total": 56,
        "breakdown": [
            {"level": "high", "label": "High Risk", "count": 7, "percentage": 12},
            {"level": "medium", "label": "Medium Risk", "count": 18, "percentage": 32},
            {"level": "low", "label": "Low Risk", "count": 31, "percentage": 56},
        ],
    },
    "exceptions": [
        {"id": "exc-1", "anomalyType": "leaver-still-paid", "severity": "high", "title": "Leaver still paid", "employeesAffected": 3, "count": 3},
        {"id": "exc-2", "anomalyType": "unexplained-variance", "severity": "high", "title": "Unexplained variance", "employeesAffected": 5, "count": 5},
        {"id": "exc-3", "anomalyType": "missing-tax-code", "severity": "medium", "title": "Missing tax code", "employeesAffected": 6, "count": 6},
    ],
    "cases": CASES,
}

EXCEPTIONS = [
    {"id": "EXC-0512", "anomalyType": "leaver-still-paid", "severity": "high", "title": "Leaver still paid", "description": "Terminated worker paid in the current run.", "employeesAffected": 3, "count": 3, "caseRef": "PA-2024-0512", "workerName": "A. Okafor", "payPeriod": "May 2024", "status": "Open", "detectedOn": "27 May 2024"},
    {"id": "EXC-0508", "anomalyType": "unexplained-variance", "severity": "high", "title": "Unexplained variance", "description": "Gross pay varies beyond the 45% tolerance.", "employeesAffected": 5, "count": 5, "caseRef": "PA-2024-0508", "workerName": "M. Rossi", "payPeriod": "May 2024", "status": "Open", "detectedOn": "26 May 2024"},
    {"id": "EXC-0505", "anomalyType": "missing-tax-code", "severity": "medium", "title": "Missing tax code", "description": "Required tax code absent for affected workers.", "employeesAffected": 6, "count": 6, "caseRef": "PA-2024-0505", "workerName": "T. Adeyemi", "payPeriod": "May 2024", "status": "Open", "detectedOn": "25 May 2024"},
]

AUDIT = [
    {"id": "AUD-1041", "timestamp": "30 Apr 2024 16:20", "caseRef": "PA-2024-0498", "actor": "A08 Governance & Audit", "action": "Audit evidence pack assembled", "control": "CP08", "detail": "Manifest EV-01…EV-04 hashed and stored."},
    {"id": "AUD-1040", "timestamp": "30 Apr 2024 15:58", "caseRef": "PA-2024-0498", "actor": "KPMG User (Payroll Controller)", "action": "Decision recorded: Approve", "control": "CP05", "detail": "Joiner payment authorised."},
    {"id": "AUD-1038", "timestamp": "27 May 2024 22:03", "caseRef": "PA-2024-0512", "actor": "A04 Exception Processing", "action": "Anomaly detected", "control": "CP02", "detail": "Rule R-ANOM-LEAVER-STILL-PAID v3.2 matched."},
]

INSIGHTS = {
    "assuranceScore": 92,
    "summary": {
        "totalCases": 56,
        "openCases": 25,
        "resolvedCases": 31,
        "totalAnomalies": 56,
        "evidencePacks": 48,
    },
    "funnel": [
        {"stage": "Detected", "count": 12},
        {"stage": "In Analysis", "count": 9},
        {"stage": "Awaiting Approval", "count": 4},
        {"stage": "Escalated", "count": 2},
        {"stage": "Resolved / Closed", "count": 31},
    ],
    "anomalyTypes": [
        {"type": "Unexplained variance", "count": 14, "maxRisk": 91},
        {"type": "Unapproved change", "count": 8, "maxRisk": 55},
        {"type": "Missing tax code", "count": 12, "maxRisk": 62},
        {"type": "Duplicate pay record", "count": 9, "maxRisk": 70},
        {"type": "Leaver still paid", "count": 7, "maxRisk": 88},
        {"type": "Joiner not paid", "count": 6, "maxRisk": 74},
    ],
    "severityMix": [
        {"level": "high", "label": "High Risk", "count": 7, "percentage": 12},
        {"level": "medium", "label": "Medium Risk", "count": 18, "percentage": 32},
        {"level": "low", "label": "Low Risk", "count": 31, "percentage": 56},
    ],
    "topRiskCases": [
        {"id": "PA-2024-0512", "workerName": "A. Okafor", "anomalyTitle": "Leaver still paid", "severity": "high", "riskScore": 88, "status": "Awaiting Approval"},
        {"id": "PA-2024-0498", "workerName": "L. Chen", "anomalyTitle": "Joiner not paid", "severity": "high", "riskScore": 74, "status": "Closed"},
        {"id": "PA-2024-0509", "workerName": "S. Kaur", "anomalyTitle": "Duplicate pay record", "severity": "medium", "riskScore": 61, "status": "Awaiting Approval"},
    ],
    "controlActivity": [
        {"control": "CP02 Anomaly detection", "count": 56},
        {"control": "CP05 Human approval", "count": 31},
        {"control": "CP08 Evidence pack", "count": 48},
        {"control": "CP10 Case closure", "count": 31},
    ],
}

PERIODS = [
    {"id": "PP-2024-05", "name": "May 2024", "start": "2024-05-01", "end": "2024-05-31", "status": "CLOSED"},
    {"id": "PP-2024-04", "name": "April 2024", "start": "2024-04-01", "end": "2024-04-30", "status": "CLOSED"},
]


def case_detail(case_id: str) -> dict | None:
    base = next((c for c in CASES if c["id"] == case_id), None)
    if base is None:
        return None
    awaiting = base["status"] == "Awaiting Approval"
    return {
        **base,
        "anomalyDescription": f"{base['anomalyTitle']} detected for {base['workerName']} in run {base['payrollRunId']}.",
        "ruleId": f"R-ANOM-{base['anomalyType'].upper()}",
        "ruleVersion": "v3.2",
        "riskFactors": [
            {"name": "Primary indicator", "weight": 0.5, "contribution": round(base["riskScore"] * 0.5), "note": "Matched anomaly rule"},
            {"name": "Amount", "weight": 0.3, "contribution": round(base["riskScore"] * 0.3), "note": "Within materiality review"},
            {"name": "History", "weight": 0.2, "contribution": round(base["riskScore"] * 0.2), "note": "Recurrence considered"},
        ],
        "rootCause": "Root-cause assessment produced by the Analysis Agent (A05).",
        "correctionOptions": [
            {"id": "OPT-1", "label": "Apply recommended correction", "description": "Deterministic correction per policy.", "recommended": True},
            {"id": "OPT-2", "label": "Route for manual investigation", "description": "Escalate to SME review.", "recommended": False},
        ],
        "impact": [
            {"label": "Gross", "value": "£3,420.00"},
            {"label": "Net", "value": "£2,388.60"},
            {"label": "Cost centre", "value": "CC-4021"},
        ],
        "recommendation": {
            "summary": "Recover the overpayment and stop future payments.",
            "rationale": "Advisory recommendation from deterministic analysis; human approval required.",
            "confidence": "High" if base["severity"] == "high" else "Medium",
            "citations": ["EV-01", "EV-02"],
        },
        "controls": [
            {"id": "CP01", "name": "Input completeness", "owner": "A07", "result": "Pass", "detail": "Required records present."},
            {"id": "CP03", "name": "Risk and severity", "owner": "A05", "result": "Pass", "detail": f"Risk {base['riskScore']}."},
            {"id": "CP05", "name": "Mandatory human approval", "owner": "A09", "result": "Pending" if awaiting else "N/A", "detail": "Human decision gate."},
            {"id": "CP06", "name": "Segregation of duties", "owner": "A09", "result": "Pending" if awaiting else "N/A", "detail": "Agent recommends; human approves."},
        ],
        "evidence": [
            {"id": "EV-01", "label": "Source record", "source": "HRIS", "hash": "sha256:aa11…22b", "capturedOn": base["detectedOn"]},
            {"id": "EV-02", "label": "Payroll line", "source": "silver.payroll_line", "hash": "sha256:cc33…44d", "capturedOn": base["detectedOn"]},
        ],
        "allowedActions": ["Approve", "Reject", "Escalate"] if awaiting else [],
        "decision": None,
    }
