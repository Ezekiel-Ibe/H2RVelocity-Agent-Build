"""Live smoke test for the payroll-assurance-af Foundry hosted agent.

This hits the LIVE agent, which performs a real assurance closure (writes to
silver.* in Fabric). It is skipped unless RUN_LIVE_ASSURANCE=1 so it never runs
by accident in CI or a normal `pytest` sweep.

Prerequisites:
  - `az login` for the mbsukdemo.com tenant (local), OR a managed identity with
    the "Foundry User" role on the velocity-h2r-proj project (deployed).

Run:
  RUN_LIVE_ASSURANCE=1 pytest -k test_run_assurance_smoke -s        # bash
  $env:RUN_LIVE_ASSURANCE=1; pytest -k test_run_assurance_smoke -s  # PowerShell
"""
import os

import pytest

from app import assurance_client


@pytest.mark.skipif(
    os.getenv("RUN_LIVE_ASSURANCE") != "1",
    reason="Set RUN_LIVE_ASSURANCE=1 to hit the live Foundry agent (performs real silver.* writes).",
)
def test_run_assurance_smoke():
    summary = assurance_client.run_assurance("PR-2026-06", "2026-06")
    assert summary.get("success") is not False, summary
    assert summary.get("case_state") == "CLOSED", summary
    assert len(summary.get("manifest_hash", "")) == 64, summary
