"""Client for the payroll-assurance-af Foundry hosted agent.

Invokes the agent synchronously through the Foundry Responses endpoint. The agent
parses the natural-language input to extract payroll_run_id + period_id, runs its
own run_payroll_assurance tool (which owns all silver.* write-back), and returns a
JSON closure summary embedded in the response's output_text.

Auth uses DefaultAzureCredential with the Foundry data-plane audience
(https://ai.azure.com/.default) — local dev = az login user token, deployed = the
BFF managed identity (needs the "Foundry User" role on velocity-h2r-proj). No secrets.
The BFF itself stays read-only against Fabric.
"""
from __future__ import annotations

import json
import logging
import urllib.error
import urllib.request
from typing import Any

from .config import settings

log = logging.getLogger("bff.assurance")

# Foundry runs synchronously: workflow runs usually 10-20s; allow ample headroom.
_TIMEOUT_SECONDS = 180


def _token() -> str:
    from azure.identity import DefaultAzureCredential

    cred = DefaultAzureCredential(
        exclude_managed_identity_credential=settings.exclude_managed_identity
    )
    return cred.get_token(settings.foundry_audience).token


def _output_text(response: dict[str, Any]) -> str:
    """Pull the assistant's output_text from a Responses API payload.

    Accepts either a flat top-level `output_text` or the nested
    output[].content[] shape.
    """
    flat = response.get("output_text")
    if isinstance(flat, str) and flat.strip():
        return flat
    parts: list[str] = []
    for item in response.get("output", []):
        if item.get("type") != "message":
            continue
        for part in item.get("content", []):
            if part.get("type") == "output_text" and part.get("text"):
                parts.append(part["text"])
    return "\n".join(parts)


def _extract_json(text: str) -> dict[str, Any] | None:
    """Skip the wrapper's narration prefix and parse the first balanced { } object.

    For run_payroll_assurance the JSON summary follows a one-line narration, so a
    plain json.loads on the whole text fails.
    """
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            esc = (ch == "\\") and not esc
            if ch == '"' and not esc:
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start : i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def _post_agent(payload: dict[str, Any]) -> dict[str, Any]:
    """POST to the hosted agent's dedicated Responses endpoint and return parsed JSON.

    Hosted agents (unlike prompt agents) must be called through their own agent
    endpoint: .../agents/<agent>/endpoint/protocols/openai/responses — the agent is
    identified by the URL path, so no model/agent_reference field is sent.
    """
    base = settings.foundry_project_endpoint.rstrip("/")
    agent = settings.assurance_agent_model
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
    with urllib.request.urlopen(req, timeout=_TIMEOUT_SECONDS) as resp:
        return json.loads(resp.read().decode())


def run_assurance(
    payroll_run_id: str, period_id: str, actor: str | None = None
) -> dict[str, Any]:
    """Invoke payroll-assurance-af and return the parsed closure summary.

    Calls the hosted agent's dedicated agent endpoint. On success returns the
    agent's typed summary; on failure {"success": False, ...}.
    """
    prompt = f"Run assurance for {payroll_run_id} period {period_id}"
    if actor:
        prompt += f", triggered by {actor}"

    try:
        response = _post_agent({"input": prompt})
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode()[:400]
        log.warning("run_assurance HTTP %s: %s", exc.code, detail)
        return {"success": False, "error": f"HTTP {exc.code}", "detail": detail}
    except Exception as exc:  # noqa: BLE001
        log.warning("run_assurance failed: %s", exc)
        return {"success": False, "error": str(exc)}

    status = response.get("status")
    if status and status != "completed":
        log.warning("run_assurance did not complete: %s", status)
        return {"success": False, "error": "not-completed", "status": status}

    text = _output_text(response)
    if not text:
        return {"success": False, "error": "empty output_text", "status": status}
    parsed = _extract_json(text)
    if parsed is None:
        log.warning("run_assurance: no JSON object found in output_text")
        return {"success": False, "error": "non-json output_text", "outputText": text[:400]}
    return parsed
