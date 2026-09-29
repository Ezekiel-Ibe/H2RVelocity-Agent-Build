# Payroll Assurance BFF

A thin, read-only **backend-for-frontend** that serves the workspace's `/api/*`
endpoints. It is the **only** tier that connects to Microsoft Fabric (and, later,
Microsoft Foundry). The React frontend holds no Fabric/Foundry credentials.

Two modes (set `DATA_SOURCE` in `.env`):

- `sample` — built-in demo data. Runs with no Fabric access. Use this to prove
  the frontend ↔ BFF wiring immediately.
- `fabric` — read-only queries against the Fabric SQL endpoint. Only `SELECT`
  statements are issued; nothing in Fabric is changed.

## Prerequisites

- Python 3.10+
- **ODBC Driver 18 for SQL Server** (needed for `fabric` mode):
  https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server
- For `fabric` mode, be signed in with an identity that can read the warehouse
  (Azure CLI `az login`, VS Code Azure sign-in, or a managed identity — picked up
  automatically by `DefaultAzureCredential`).

## Run

```powershell
cd bff
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env        # then edit .env
uvicorn app.main:app --reload --port 8000
```

Check it: http://localhost:8000/health  → `{"status":"ok","dataSource":"sample"}`

## Point the frontend at it

In the frontend project, create `.env.local`:

```
VITE_API_BASE_URL=http://localhost:8000
VITE_USE_MOCKS=false
```

Restart `npm run dev`. The app now loads from the BFF.

## Switching to live Fabric

1. In `bff/.env` set:
   ```
   DATA_SOURCE=fabric
   FABRIC_SQL_ENDPOINT=<your>.datawarehouse.fabric.microsoft.com
   FABRIC_DATABASE=edm_wh_dev
   ```
2. Confirm the schema (read-only): `GET http://localhost:8000/api/_schema`.
3. Adjust the object/column mappings in `app/fabric_data.py` to match the real
   Silver/Gold names (they are marked with `TODO`).

## Endpoints

`GET /api/dashboard`, `GET /api/cases`, `GET /api/cases/{id}`,
`POST /api/cases/{id}/decision`, `GET /api/exceptions`, `GET /api/audit`,
`POST /api/agent/messages` (Foundry placeholder), `GET /api/_schema`, `GET /health`.

`POST /api/run-assurance` — invokes the **payroll-assurance-af** Foundry hosted
agent synchronously and returns its closure summary. Body: `{ "payrollRunId": "PR-2026-06", "periodId": "2026-06" }`.
The response is the agent's typed summary (`case_id`, `case_state`, `total_anomalies`,
`risk_score`, `manifest_hash`, `signoff_token`, …) plus a top-level `runId` alias
equal to `case_id`. The agent owns all `silver.*` write-back; the BFF stays read-only.

- **Auth:** no new secrets. An Entra token is acquired per request via
  `DefaultAzureCredential` for audience `https://ai.azure.com/.default`. The BFF
  managed identity (deployed) or your `az login` user (local) needs the
  **`Foundry User`** role on the `velocity-h2r-proj` project — already granted.
- **Config:** `FOUNDRY_ENDPOINT`, `FOUNDRY_AUDIENCE`, `FOUNDRY_RESPONSES_API_VERSION`
  (defaults point at the deployed project / `2025-11-15-preview`). Runs synchronously
  (client timeout 180s).
- **Smoke test:** `RUN_LIVE_ASSURANCE=1 pytest -k test_run_assurance_smoke -s`
  (⚠️ performs a real closure run with live `silver.*` writes).
