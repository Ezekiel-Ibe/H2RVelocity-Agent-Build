# Deploy brief — "H2R-style" React SPA + FastAPI BFF + Foundry agents on Azure

Hand this to another team. They paste it to their Copilot (or an azure-deploy agent);
it interviews them about *their* app/agents/materials, then deploys in the same proven
shape. It bakes in the gotchas we hit so they don't repeat them.

---

You are helping me deploy a web app to Azure using a proven pattern. First ASK me the
questions below, then scaffold + deploy. Don't assume answers — confirm before each deploy.

## Target architecture (use this exact shape)
- **Frontend**: React (Vite) SPA → **Azure Static Web Apps (Standard)**.
- **BFF**: FastAPI (Python), the ONLY tier holding Fabric/Foundry creds, read-only against
  Fabric → **Azure Container Apps** (custom image). Uses `DefaultAzureCredential` (managed
  identity in Azure, `az login` locally). Exposes `/health` + `/api/*`.
- **AI**: REUSE an existing Microsoft Foundry project + agents (don't provision new ones).
- **Data**: Microsoft Fabric warehouse, read-only SELECTs via ODBC Driver 18.
- **Supporting**: Log Analytics + App Insights + a user-assigned managed identity (AcrPull).
- **IaC**: Bicep, deployed via `az deployment sub create` (NOT azd). Frontend via `swa deploy`.

## Questions to ask me first
1. App name + one-line purpose?
2. Azure subscription + region? (SWA has no control plane in some regions — pick a nearby one.)
3. Your **Foundry project endpoint** + the **agent name(s)** the chat/BFF should call?
4. Your **Fabric SQL endpoint** host + database name? Read-only? Which `silver.*`/schema tables?
5. Any **write/workflow agent** (like a run-assurance action)? If yes, it MUST be a button, not chat.
6. Scale: demo/pilot or production? Expected concurrent users?
7. What materials do you have (existing frontend? BFF? agent definitions? sample data)?

## Build + deploy steps
1. Scaffold `frontend/`, `bff/` (with a **Dockerfile**), `infra/` (Bicep: SWA, Container App +
   env, ACR Basic, user-assigned MI + AcrPull, Log Analytics, App Insights).
2. `az deployment sub create` (placeholder image) → `az acr build` the BFF → redeploy with the
   real image → build the SPA (bake `VITE_API_BASE_URL` = BFF URL) → `swa deploy`.
3. Health-check `/health` and the SPA root.

## Gotchas to bake in from the start (we learned these the hard way)
- **Dockerfile**: install `msodbcsql18` via the canonical Microsoft apt steps; do NOT
  `apt purge`/`autoremove` afterward (it strips a driver runtime dep -> ODBC "can't open lib").
- **Container App**: `cpu: 1.0`, `memory: 2Gi`, `minReplicas: 1`, `maxReplicas: 5`, and an HTTP
  scale rule at ~4 concurrent/replica. 1 GiB OOMs under concurrent LLM calls; scale-to-zero
  adds cold-start lag.
- **Fabric load**: reuse the credential (module-level) + `pyodbc.pooling=True`, and add a ~30s
  in-memory cache on read endpoints — otherwise many testers throttle the Fabric capacity
  (`CapacityLimitExceeded` / TCP 10054), and the app silently falls back to sample data.
- **CORS**: BFF must allow the SWA origin (env `CORS_ORIGINS`).
- **SPA routing**: add `staticwebapp.config.json` with a `navigationFallback` to `/index.html`,
  or deep-link refreshes 404.
- **Any user state** (approvals/decisions): keep it **client-side (sessionStorage)** or in shared
  storage — a local file in the container is per-replica and breaks under scale-out.
- **Foundry RBAC**: the BFF's managed identity needs **`Foundry User` at the PROJECT scope**
  (account-scope inheritance is NOT enough for the hosted-agent `/responses` endpoint -> 404).
  Note many tenants have a policy that only allows role assignments to **groups**, not users.
- **Governance**: keep the chat panel **read-only** (never let free-form chat invoke a write
  workflow). Write actions = explicit buttons with the actor captured for audit.

Now ask me the questions, wait for my answers, and proceed one confirmed step at a time.
