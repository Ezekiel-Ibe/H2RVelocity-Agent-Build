"""Payroll Assurance BFF — serves the frontend /api/* endpoints.

Data comes from built-in samples (DATA_SOURCE=sample) or a read-only Microsoft
Fabric SQL connection (DATA_SOURCE=fabric). The frontend never talks to Fabric or
Foundry directly — this tier is the only one holding those connections.
"""
from __future__ import annotations

import json
import logging
import time

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from . import provider
from . import data_agent_client
from . import foundry_agent_client
from . import assurance_client
from . import decision_store
from .config import settings

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Payroll Assurance BFF", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "dataSource": settings.data_source}


@app.get("/api/dashboard")
def get_dashboard(
    period: str | None = None,
    date_from: str | None = Query(None, alias="from"),
    date_to: str | None = Query(None, alias="to"),
) -> dict:
    return provider.dashboard(period, date_from, date_to)


@app.get("/api/cases")
def get_cases() -> list:
    return provider.cases()


@app.get("/api/cases/{case_id}")
def get_case(case_id: str) -> dict:
    detail = provider.case_detail(case_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Not found")
    return detail


class DecisionRequest(BaseModel):
    action: str
    rationale: str = Field(min_length=10)


@app.post("/api/cases/{case_id}/decision")
def post_decision(case_id: str, body: DecisionRequest) -> dict:
    if body.action not in {"Approve", "Reject", "Escalate"}:
        raise HTTPException(status_code=400, detail="Invalid action")
    decision = decision_store.record(case_id, body.action, body.rationale.strip())
    routed = {
        "Approve": "approved and routed to Data Management (A03) for the governed commit",
        "Reject": "rejected — no pay-impacting change will be made",
        "Escalate": "escalated for senior review",
    }.get(body.action, "recorded")
    return {
        "caseId": case_id,
        "action": body.action,
        "outcome": f"Decision recorded: {body.action}. Case {routed}.",
        "recordedAt": decision["decidedOn"],
    }


@app.get("/api/exceptions")
def get_exceptions() -> list:
    return provider.exceptions()


@app.get("/api/audit")
def get_audit() -> list:
    return provider.audit()


@app.post("/api/admin/reset")
def reset_demo() -> dict:
    # Demo helper: clears recorded human decisions so the app returns to its
    # initial state. Does not touch Fabric or Foundry.
    cleared = decision_store.clear()
    return {"status": "ok", "clearedDecisions": cleared}


@app.get("/api/insights")
def get_insights(
    period: str | None = None,
    date_from: str | None = Query(None, alias="from"),
    date_to: str | None = Query(None, alias="to"),
) -> dict:
    return provider.insights(period, date_from, date_to)


@app.get("/api/periods")
def get_periods() -> list:
    return provider.periods()


class RunAssuranceRequest(BaseModel):
    payrollRunId: str = Field(min_length=1)
    periodId: str = Field(min_length=1)
    actor: str | None = None


@app.post("/api/run-assurance")
def post_run_assurance(body: RunAssuranceRequest) -> dict:
    # Explicit UI action (never chat): invokes the payroll-assurance-af hosted agent,
    # which owns all silver.* write-back. The BFF stays read-only against Fabric.
    actor = body.actor or "SYSTEM_UI_TRIGGER"
    summary = assurance_client.run_assurance(body.payrollRunId, body.periodId, actor)
    # runId alias = case_id so the frontend needn't know the field name.
    return {"runId": summary.get("case_id"), **summary}


class AgentRequest(BaseModel):
    prompt: str = Field(min_length=1)
    conversationId: str | None = None


@app.post("/api/agent/messages")
def post_agent(body: AgentRequest) -> dict:
    # Primary path: the Foundry prompt agent (a01-workspace). Only fall back to
    # the Fabric Data Agent if Foundry is not connected, and flag it to the UI.
    source = "foundry"
    notice: str | None = None

    result = foundry_agent_client.ask(body.prompt, body.conversationId)

    if not result.get("connected", False):
        if settings.use_data_agent:
            fabric = data_agent_client.ask(body.prompt)
            result = {**fabric, "conversationId": body.conversationId}
            source = "fabric"
            notice = "Foundry agent not connected — answered using the Fabric data agent fallback."
        else:
            source = "none"
            notice = "Foundry agent is not connected. Check the Foundry endpoint, sign-in, and permissions."

    return {
        "id": f"agent-{int(time.time() * 1000)}",
        "author": "agent",
        "body": result["answer"],
        "timestamp": "Just now",
        "evidenceStatus": "grounded" if result["grounded"] else "insufficient_evidence",
        "citations": result["citations"],
        "conversationId": result.get("conversationId"),
        "source": source,
        "notice": notice,
    }


@app.post("/api/agent/stream")
def post_agent_stream(body: AgentRequest) -> StreamingResponse:
    # Streams the orchestrator's tokens (narration first, then answer) as SSE so
    # the UI shows which sub-agent is consulted before the full answer arrives.
    def event_stream():
        for evt in foundry_agent_client.ask_stream(body.prompt, body.conversationId):
            yield f"data: {json.dumps(evt)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/_schema")
def get_schema() -> list:
    """Read-only Fabric schema discovery (fabric mode only)."""
    if not settings.use_fabric:
        raise HTTPException(status_code=400, detail="Set DATA_SOURCE=fabric to inspect the schema.")
    from . import fabric_data

    return fabric_data.schema()
