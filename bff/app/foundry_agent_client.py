"""Client for the Microsoft Foundry hosted agent that powers the agent-chat panel.

The chat panel targets the `payroll-assurance-af` hosted orchestrator agent in the
Foundry project `velocity-h2r-proj`. Being a *hosted* agent, it is invoked through
its dedicated agent endpoint (.../agents/<agent>/endpoint/protocols/openai/responses),
not the prompt-agent `agent_reference` shape. Auth uses `DefaultAzureCredential`.

Multi-turn context is preserved with `previous_response_id`: each call returns a
`response_id`; the frontend echoes it back (as conversationId) on the next turn.
"""
from __future__ import annotations

import json
import logging
import re
import time
import urllib.error
import urllib.request
from typing import Any

from .config import settings

log = logging.getLogger("bff.foundry_agent")

# Inline citation markers the agent embeds in text, e.g. "【6:0†source】".
_CITATION_MARKER = re.compile(r"【[^】]*】")

_NOT_CONNECTED = (
    "The Foundry agent is not connected yet. Set FOUNDRY_PROJECT_ENDPOINT and "
    "FOUNDRY_AGENT_NAME to the deployed prompt agent to enable live answers."
)

# Phrases the orchestrator emits when a sub-agent's Fabric query transiently fails
# (usually capacity throttling). A single fresh retry normally succeeds.
_TRANSIENT_MARKERS = (
    "data query failed",
    "couldn't retrieve",
    "could not retrieve",
    "please try again in a moment",
)


def _token() -> str:
    from azure.identity import DefaultAzureCredential

    cred = DefaultAzureCredential(
        exclude_managed_identity_credential=settings.exclude_managed_identity
    )
    return cred.get_token(settings.foundry_scope).token


def _post_agent(payload: dict[str, Any]) -> dict[str, Any]:
    """POST to the hosted agent's dedicated Responses endpoint and return parsed JSON."""
    base = settings.foundry_project_endpoint.rstrip("/")
    agent = settings.foundry_agent_name
    url = (
        f"{base}/agents/{agent}/endpoint/protocols/openai/responses"
        f"?api-version={settings.foundry_responses_api_version}"
    )
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {_token()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    # Orchestrator answers are multi-hop (router -> sub-agent -> Fabric); deep
    # diagnosis/analysis turns can run ~3 min, so allow generous headroom.
    with urllib.request.urlopen(req, timeout=280) as resp:
        return json.loads(resp.read().decode())


def _extract(response: dict[str, Any]) -> tuple[str, list[str]]:
    """Pull assistant text and citation labels out of a Responses API payload."""
    answer_parts: list[str] = []
    citations: list[str] = []
    for item in response.get("output", []):
        if item.get("type") != "message" or item.get("role") != "assistant":
            continue
        for part in item.get("content", []):
            if part.get("type") == "output_text":
                text = part.get("text", "")
                if text:
                    answer_parts.append(_CITATION_MARKER.sub("", text).strip())
                for ann in part.get("annotations", []):
                    label = ann.get("title") or ann.get("filename") or ann.get("url")
                    if label and label not in citations:
                        citations.append(label)
    return "\n\n".join(p for p in answer_parts if p), citations


def ask(prompt: str, conversation_id: str | None = None) -> dict[str, Any]:
    """Query the Foundry hosted agent. Returns {answer, citations, grounded, conversationId, connected}.

    `conversation_id` carries the previous turn's response_id for multi-turn context.
    """
    if not settings.use_foundry_agent:
        return {
            "answer": _NOT_CONNECTED,
            "citations": [],
            "grounded": False,
            "conversationId": None,
            "connected": False,
        }
    payload: dict[str, Any] = {"input": prompt}
    if conversation_id:
        payload["previous_response_id"] = conversation_id
    start = time.monotonic()
    result: dict[str, Any] | None = None
    for attempt in range(2):
        try:
            response = _post_agent(payload)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode()[:300]
            log.warning("foundry agent HTTP %s: %s", exc.code, detail)
            return {
                "answer": f"The agent is unavailable right now (HTTP {exc.code}).",
                "citations": [],
                "grounded": False,
                "conversationId": conversation_id,
                "connected": False,
            }
        except Exception as exc:  # noqa: BLE001
            log.warning("foundry agent call failed: %s", exc)
            return {
                "answer": f"The agent is unavailable right now ({type(exc).__name__}).",
                "citations": [],
                "grounded": False,
                "conversationId": conversation_id,
                "connected": False,
            }
        status = response.get("status")
        if status and status != "completed":
            log.warning("foundry agent run did not complete: %s", status)
            return {
                "answer": "The agent could not complete this request. Please rephrase and try again.",
                "citations": [],
                "grounded": False,
                "conversationId": response.get("response_id") or conversation_id,
                "connected": True,
            }
        answer, citations = _extract(response)
        result = {
            "answer": answer or "No answer was returned.",
            "citations": citations,
            "grounded": bool(answer),
            "conversationId": response.get("response_id") or conversation_id,
            "connected": True,
        }
        transient = any(m in (answer or "").lower() for m in _TRANSIENT_MARKERS)
        if transient and attempt == 0 and (time.monotonic() - start) < 90:
            log.warning("foundry agent transient sub-agent failure; retrying once")
            continue
        return result
    return result


def ask_stream(prompt: str, conversation_id: str | None = None):
    """Yield incremental events from a streamed agent run.

    Events (dicts): {"type": "delta", "text": ...} for each token as it arrives,
    then {"type": "done", "conversationId": ...}; or {"type": "error", "message": ...}.
    The orchestrator emits its "Asking the A05 agent…" narration first, so the
    caller sees which sub-agent is consulted before the answer streams in.
    """
    if not settings.use_foundry_agent:
        yield {"type": "error", "message": _NOT_CONNECTED}
        return
    payload: dict[str, Any] = {"input": prompt, "stream": True}
    if conversation_id:
        payload["previous_response_id"] = conversation_id
    base = settings.foundry_project_endpoint.rstrip("/")
    agent = settings.foundry_agent_name
    url = (
        f"{base}/agents/{agent}/endpoint/protocols/openai/responses"
        f"?api-version={settings.foundry_responses_api_version}"
    )
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {_token()}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        method="POST",
    )
    response_id = conversation_id
    seen_tool = False
    try:
        with urllib.request.urlopen(req, timeout=280) as resp:
            for raw in resp:
                line = raw.decode("utf-8", "ignore").strip()
                if not line.startswith("data:"):
                    continue
                data = line[len("data:") :].strip()
                if not data or data == "[DONE]":
                    continue
                try:
                    evt = json.loads(data)
                except json.JSONDecodeError:
                    continue
                etype = evt.get("type")
                if etype == "response.output_item.added":
                    # A tool call marks the boundary: text before it is the
                    # orchestrator's narration, text after it is the answer.
                    itype = (evt.get("item") or {}).get("type", "")
                    if "call" in itype:
                        seen_tool = True
                elif etype == "response.output_text.delta":
                    delta = evt.get("delta", "")
                    if delta:
                        yield {"type": "delta" if seen_tool else "status", "text": delta}
                elif etype in ("response.completed", "response.incomplete", "response.failed"):
                    r = evt.get("response") or {}
                    response_id = r.get("response_id") or r.get("id") or response_id
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode()[:200]
        log.warning("foundry agent stream HTTP %s: %s", exc.code, detail)
        yield {"type": "error", "message": f"HTTP {exc.code}"}
        return
    except Exception as exc:  # noqa: BLE001
        log.warning("foundry agent stream failed: %s", exc)
        yield {"type": "error", "message": type(exc).__name__}
        return
    yield {"type": "done", "conversationId": response_id}
