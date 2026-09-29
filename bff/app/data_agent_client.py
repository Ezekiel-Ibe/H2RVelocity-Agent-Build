"""Client for the Fabric Data Agent that powers the agent-chat panel.

The data agent (`a01_workspace_agent`) is a governed, read-only conversational
layer over the H2R payroll data in Fabric. It only issues SELECT/DAX/KQL *read*
queries and returns summarised natural-language answers.

Consumption path (external BFF): the published data agent exposes an OpenAI
Assistants-compatible endpoint. We authenticate with `DefaultAzureCredential`
(the same Azure CLI / managed identity used for the SQL connection) and drive the
standard threads/runs flow. Set `FABRIC_DATA_AGENT_URL` to the published endpoint
to enable it; without it the panel returns a clear "not connected" message.
"""
from __future__ import annotations

import logging
from typing import Any

from .config import settings

log = logging.getLogger("bff.data_agent")

_NOT_CONNECTED = (
    "The Fabric data agent is not connected yet. Set FABRIC_DATA_AGENT_URL to the "
    "published a01_workspace_agent endpoint (Fabric \u2192 open the data agent \u2192 "
    "Publish) to enable live answers."
)


def _token() -> str:
    from azure.identity import DefaultAzureCredential

    cred = DefaultAzureCredential(
        exclude_managed_identity_credential=settings.exclude_managed_identity
    )
    return cred.get_token(settings.data_agent_scope).token


def _client():
    from openai import OpenAI

    token = _token()
    return OpenAI(
        base_url=settings.data_agent_url.rstrip("/") + "/openai",
        api_key=token,
        default_headers={"Authorization": f"Bearer {token}"},
    )


def _answer_text(messages: Any) -> str:
    for m in messages.data:
        if m.role != "assistant":
            continue
        for part in m.content:
            if getattr(part, "type", "") == "text":
                return part.text.value
    return ""


def ask(prompt: str) -> dict[str, Any]:
    """Query the data agent. Returns {answer, citations, grounded}."""
    if not settings.use_data_agent:
        return {"answer": _NOT_CONNECTED, "citations": [], "grounded": False}
    try:
        client = _client()
        assistant = client.beta.assistants.create(model=settings.data_agent_name)
        thread = client.beta.threads.create()
        client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=assistant.id
        )
        if run.status != "completed":
            log.warning("data agent run did not complete: %s", run.status)
            return {
                "answer": "The data agent could not complete this request. Please rephrase and try again.",
                "citations": [],
                "grounded": False,
            }
        messages = client.beta.threads.messages.list(thread_id=thread.id, order="desc")
        answer = _answer_text(messages)
        return {"answer": answer or "No answer was returned.", "citations": [], "grounded": bool(answer)}
    except Exception as exc:  # noqa: BLE001
        log.warning("data agent call failed: %s", exc)
        return {
            "answer": f"The data agent is unavailable right now ({type(exc).__name__}).",
            "citations": [],
            "grounded": False,
        }
