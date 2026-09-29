# API Contracts

The frontend consumes a small set of JSON endpoints through a **governed
backend-for-frontend (BFF)**. The BFF is the only tier that connects to
Microsoft Fabric and Microsoft Foundry; it holds all credentials. The frontend
holds none and never calls Fabric or Foundry directly.

```
React app ──HTTPS──► BFF API ──► Microsoft Fabric (warehouse / lakehouse tables)
                        └───────► Microsoft Foundry (Payroll Assurance Agent)
```

The frontend swaps from mock to real data by setting `VITE_API_BASE_URL` and
`VITE_USE_MOCKS=false`. Endpoint paths are centralised in
`src/services/endpoints.ts`; response shapes are validated at the boundary with
the Zod contracts in `src/contracts/schemas.ts`.

## Endpoints

| Method | Path | Contract (Zod) | Backing data source (via BFF) |
|--------|------|----------------|-------------------------------|
| GET | `/api/dashboard` | `dashboardSchema` | Aggregated from Fabric payroll-run + assurance-result tables |
| GET | `/api/cases` | `casesResponseSchema` | `gold.vw_agent_payroll_case` (case_id, worker_id, payroll_run_id) |
| GET | `/api/exceptions` | `exceptionsResponseSchema` | Anomaly register from A04 (seven approved classes) |
| POST | `/api/agent/messages` | `agentRequestSchema` → `agentResponseSchema` | Microsoft Foundry Payroll Assurance Agent (A01/A05/A06 narrative) |

### Notes for the BFF implementation

- **Fabric access**: the BFF queries Fabric (e.g. the warehouse endpoint) using a
  managed identity / service principal with least-privilege, read-only access to
  the required tables. Field names and joins are owned by the data model, not the
  frontend — the frontend consumes only the shapes above.
- **Foundry agent**: `/api/agent/messages` proxies to the Foundry agent. The BFF
  is responsible for auth, thread/session management, evidence citations, and
  redaction. The frontend renders replies and the AI-accuracy notice; it performs
  no authoritative payroll reasoning.
- **Authoritative operations** (approvals, corrections, closures) must be
  dedicated, governed BFF endpoints with server-side authorisation — never
  computed or decided in the frontend.
- **Contract changes**: when real field names are confirmed, update the Zod
  schemas first, then the fixtures, so the mock and real paths stay aligned.

## Open items

Real Fabric table/column names, the Foundry agent/session API shape, and the
auth model are not yet confirmed — tracked in `docs/open-questions.md`
(OQ-003/004/005).
