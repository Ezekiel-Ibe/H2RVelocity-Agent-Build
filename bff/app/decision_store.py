"""Records human approval decisions (A09 / CP05) made in the app.

The BFF reads Fabric read-only, so approval decisions are not written back to the
warehouse here. They are persisted to a local JSON file so decisions survive
restarts and are reflected in the case list, case detail and approvals queue.
Replace this with the governed A09 write service when available.
"""
from __future__ import annotations

import json
import logging
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

log = logging.getLogger("bff.decisions")

_LOCK = threading.Lock()
_PATH = Path(__file__).resolve().parent.parent / ".decisions.json"

# Decision action -> resulting case status shown in the UI.
STATUS_FOR_ACTION = {"Approve": "Approved", "Reject": "Closed", "Escalate": "Escalated"}


def _load() -> dict[str, Any]:
    try:
        return json.loads(_PATH.read_text(encoding="utf-8")) if _PATH.exists() else {}
    except Exception as exc:  # noqa: BLE001
        log.warning("decision store read failed: %s", exc)
        return {}


def _save(data: dict[str, Any]) -> None:
    try:
        _PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        log.warning("decision store write failed: %s", exc)


def all_decisions() -> dict[str, Any]:
    with _LOCK:
        return _load()


def get(case_id: str) -> dict[str, Any] | None:
    with _LOCK:
        return _load().get(case_id)


def record(
    case_id: str,
    action: str,
    rationale: str,
    decided_by: str = "KPMG User (Payroll Controller)",
) -> dict[str, Any]:
    decision = {
        "action": action,
        "rationale": rationale,
        "decidedBy": decided_by,
        "decidedOn": datetime.now(timezone.utc).strftime("%d %b %Y %H:%M"),
    }
    with _LOCK:
        data = _load()
        data[case_id] = decision
        _save(data)
    return decision


def clear() -> int:
    """Remove all recorded decisions (demo reset). Returns how many were cleared."""
    with _LOCK:
        count = len(_load())
        try:
            if _PATH.exists():
                _PATH.unlink()
        except Exception as exc:  # noqa: BLE001
            log.warning("decision store clear failed: %s", exc)
        return count
