# Development & Integration Roadmap

Status: **Prototype** (React/Fluent workspace, synthetic fixtures only).
This roadmap turns the current build into a governed, Fabric/Foundry-integrated
Payroll Assurance workspace. It is sequenced by dependency — earlier phases
unblock later ones.

Cross-references: [open-questions.md](open-questions.md) (OQ-###),
[decision-log.md](decision-log.md) (ADR-###), [api-contracts.md](api-contracts.md),
[security-boundaries.md](security-boundaries.md), [traceability-matrix.md](traceability-matrix.md).

---

## Current state (baseline)

| Area | Built | Not built |
|------|-------|-----------|
| Shell / nav | Fixed shell, collapsible panels, responsive, a11y baseline | Header help/notifications/profile menu |
| Home | KPIs, assurance donut, recent exceptions/cases, quick actions (visual) | Live metrics, working quick actions |
| Cases | List + detail (risk factors, recommendation, impact, CP01–CP10, evidence) | Pagination, search, live state |
| Approvals | Awaiting-approval list → detail | Real authority checks |
| Decision | Approve/Reject/Escalate + mandatory rationale (CP05/CP06), immutable | Server authority response, SoD enforcement |
| Exceptions | Seven anomaly classes, filter, states | Real detection data |
| Audit Trail | Governance timeline (CP tags) | Real evidence lineage, pack download |
| Agent | Cited replies + INSUFFICIENT_EVIDENCE | Real model, streaming, sessions |
| Platform | Zod contracts, dev-middleware mock API (+ MSW for tests), env switch, 24 tests, CI file | BFF, Fabric, Foundry, auth |

---

## Current capabilities (detail)

**Shell & navigation**
- Fixed KPMG-branded app shell: pinned sidebar + pinned agent panel; only the main area scrolls.
- Approved KPMG logo (rgb/white/black variants) wired via `KpmgLogo` (white on the navy sidebar); browser favicon set to the RGB mark.
- Primary nav (React Router): Home, Cases, Exceptions, Approvals, Audit Trail, Reports, Insights, Settings.
- Collapsible sidebar (icon rail) and dockable agent panel, with auto-collapse at narrow widths plus manual toggles.
- Container-query responsive layout (reflows on real content width, not viewport); fluid header type; no title/subtitle overlap.
- Accessibility baseline: skip link, landmarks, `aria-current`, labelled icon buttons, `aria-live` for agent responses, reduced-motion, visible focus ring.

**Home dashboard**
- KPI stat cards, Assurance Overview donut + risk breakdown, Recent Exceptions (seven anomaly classes), Recent Cases table, Quick Actions (visual only).

**Cases (A01 core)**
- Cases list with filter (All/Open/Closed), risk score, workflow step, status.
- Case detail: anomaly + rule, risk factors (CP03), recommendation + correction options with evidence citations, impact assessment (CP04), control results CP01–CP10, evidence manifest (CP08).
- Human decision panel: Approve/Reject/Escalate with mandatory rationale (CP05/CP06), immutable after submit, posts to a decision endpoint.

**Exceptions / Approvals / Audit**
- Exceptions: seven approved anomaly classes, severity filter, loading/empty/error states.
- Approvals: cases awaiting a controller decision, deep-link to case detail.
- Audit Trail: governance timeline tagged with controls (CP01–CP10) and owning agents.

**Agent chat**
- Docked assistant with suggested prompts, simulated "thinking", evidence citations on grounded replies, explicit `INSUFFICIENT_EVIDENCE` state.

**Engineering**
- React 19 + strict TS, Vite, Fluent UI v9, TanStack Query, React Router, CSS Modules + design tokens.
- Zod validation at every API boundary; mock API served by a **Vite dev middleware** (reliable, no service worker) with **MSW node** for tests; env-driven mock↔real switch; centralised endpoint map.
- 24 passing tests (unit/component/a11y-axe), clean type-check/lint, green build; docs set (architecture, api-contracts, security-boundaries, accessibility-standard, decision-log, open-questions, traceability-matrix).

---

## Limitations (explicit)

**Data & integration**
- All data is synthetic fixtures (served by a Vite dev middleware in the browser, MSW in tests) — no real backend, Fabric or Foundry. Nothing shown is a validated business result.
- No backend-for-frontend (BFF) exists; the whole Fabric/Foundry integration is documented but unbuilt. The frontend holds no credentials by design.
- Contracts are provisional — Zod schemas were shaped from the Stage docs, not confirmed API responses; real Silver/Gold columns are not yet mapped (OQ-003/004).
- No pagination, sorting, server-side filtering, or search — lists render the full fixture array.
- No real-time/streaming — agent "thinking" is simulated; no live case-state updates.
- Decision submission is a fire-and-forget mock — no optimistic concurrency or server authority-check response handling.

**Functional gaps**
- Quick Actions (Upload Payroll Data, Run Assurance Checks, View Key Insights, Generate Report) are non-functional.
- Reports, Insights, Settings, Payroll Data are placeholder pages.
- No file upload; no evidence-pack download (evidence is display-only, hashes are synthetic).
- No global case search; header Help / notifications / profile menu / avatar not implemented.

**Security & identity**
- No authentication or authorization — no Entra ID/SSO, no RBAC, no route guards; the controller is hard-coded ("KPMG User").
- No role-aware UI — every user sees every action; segregation of duties (CP06) is a label, not enforced.
- No data minimisation/masking, session handling, or token logic (none needed yet without a backend).

**Agent / AI boundary**
- Replies are canned regex matches, not a real model; citations point at fixture evidence IDs.
- `INSUFFICIENT_EVIDENCE` is keyword-triggered, not a real grounding check.
- No prompt/model versioning, evaluation, token streaming, or conversation persistence.

**Brand & compliance**
- Approved KPMG logo (rgb/white/black) is integrated (OQ-002 resolved); brand **colour tokens remain provisional** pending official values (ADR-002 superseded for the logo only).
- The React workspace is a departure from the Stage 7A technology decision (Copilot Studio + Power Apps/Dataverse) — ADR-008, pending Factory Design Authority direction.

**Accessibility & testing**
- WCAG 2.2 AA partially met: no full keyboard/screen-reader pass, no contrast audit of provisional tokens, limited axe coverage.
- No E2E running (Playwright scaffolded, browsers not installed/CI-wired); no visual regression.
- Container queries require a modern browser; no legacy fallback.

**Ops / build**
- Node isn't installed on the host — a portable Node 20 was used; the CI workflow exists but hasn't run.
- No deployment target, telemetry/AgentOps, or error boundary/monitoring.

---

## Phase 0 — Decisions & contracts (unblock everything)

**Goal:** remove the strategic and contract ambiguity that blocks real integration.

- [ ] **Resolve ADR-008**: React/Fluent vs Stage 7A's Copilot Studio + Power
      Apps/Dataverse. Obtain Factory Design Authority direction. *(highest priority)*
- [ ] Confirm governed API contracts and **Fabric Silver/Gold field mapping**
      (OQ-003, OQ-004) — map each Zod schema to real columns/views
      (`gold.vw_agent_payroll_case`, `gold.vw_agent_control_status`, etc.).
- [ ] Confirm the **auth & role model** and authority matrix (OQ-005): roles,
      delegation, expiry, dual approval, period sign-off.
- [ ] Obtain approved **brand colour tokens** (OQ-001). *(KPMG logo supplied and
      wired — OQ-002 resolved.)*

**Exit:** approved technology decision, versioned API contract, auth model, brand pack.

---

## Phase 1 — Backend-for-frontend (BFF)

**Goal:** a governed API tier that owns Fabric + Foundry; frontend flips off mocks.
Depends on Phase 0 (contracts, tech decision).

- [ ] Stand up the BFF (per ADR-008 outcome) exposing the current endpoints:
      `/api/dashboard`, `/api/cases`, `/api/cases/:id`, `/api/cases/:id/decision`,
      `/api/exceptions`, `/api/audit`, `/api/agent/messages`.
- [ ] Wire **Microsoft Fabric** reads via `FabricRepository` (extend with read
      methods over the Gold agent views); managed identity, least-privilege.
- [ ] Proxy the **Foundry Payroll Assurance Agent** for `/api/agent/messages`
      (auth, thread/session, evidence citations, redaction).
- [ ] Frontend: set `VITE_API_BASE_URL`, `VITE_USE_MOCKS=false`; align Zod
      schemas to real payloads; keep MSW for dev/test.

**Exit:** app runs on live (dev) data end-to-end through the BFF.

---

## Phase 2 — Identity, RBAC & governed decisions

**Goal:** enforce the security boundary, not just display it.
Depends on Phase 0 (auth model), Phase 1 (BFF).

- [ ] **Entra ID sign-in**, token handling, session/expiry, sign-out.
- [ ] **Route guards + role-aware UI**; hide/disable actions by permission.
- [ ] Enforce **CP05/CP06** server-side; surface authority/SoD/dual-approval
      outcomes from A09 in the decision panel (not just a canned message).
- [ ] Data minimisation / masking of sensitive worker fields; no PII in logs.

**Exit:** only authorised controllers can approve; decisions are governed and audited.

---

## Phase 3 — Complete the workspace features

**Goal:** turn placeholders and stubs into working capability.
Depends on Phase 1 (data), Phase 2 (permissions).

- [ ] **Quick Actions**: Upload Payroll Data (file upload → A03), Run Assurance
      Checks (trigger A07/A04), View Key Insights, Generate Report.
- [ ] **Evidence pack**: view/download real evidence (A08/CP08) with real hashes.
- [ ] **Reports / Insights / Settings** pages (Power BI embed or API-driven).
- [ ] **Header**: help, notifications + count, profile menu, real user context.
- [ ] Lists: **pagination, server-side sort/filter, global case search**.

**Exit:** all navigation targets are functional; no dead buttons.

---

## Phase 4 — Real-time agent & case state

**Goal:** live, grounded, streaming experience.
Depends on Phase 1 (Foundry proxy).

- [ ] **Streaming** agent responses (SSE/websocket) with token-level rendering.
- [ ] Real grounding: enforce `evidence_id`/`calculation_id` citations and true
      `INSUFFICIENT_EVIDENCE` from the backend; prompt/model versioning + eval.
- [ ] Conversation **persistence** and thread/session management.
- [ ] Live **case-state** updates (orchestrator W01–W20 transitions).

**Exit:** agent and case state reflect live backend truth.

---

## Phase 5 — Hardening, quality & delivery

**Goal:** production readiness.
Runs partly in parallel from Phase 2 onward.

- [ ] **Accessibility**: full keyboard + screen-reader pass, contrast audit of
      approved tokens, expand axe coverage — target WCAG 2.2 AA sign-off.
- [ ] **Testing**: install Playwright browsers, wire E2E in CI, add visual
      regression; raise component coverage; contract tests against the BFF.
- [ ] **Resilience**: error boundaries, retry/backoff, offline/timeout handling.
- [ ] **Observability**: AgentOps/App Insights telemetry, error monitoring.
- [ ] **Delivery**: environments, secrets management, deployment pipeline,
      rollback; run the existing CI workflow.

**Exit:** deployable, monitored, accessible, tested release.

---

## Dependency summary

```
Phase 0 (decisions/contracts)
   └─► Phase 1 (BFF: Fabric + Foundry)
          ├─► Phase 2 (auth / RBAC / governed decisions)
          │       └─► Phase 3 (features: quick actions, reports, evidence)
          └─► Phase 4 (streaming agent / live state)
Phase 5 (hardening) runs alongside Phases 2–4.
```

## Key risks / watch items

- **ADR-008 unresolved** — building further React features increases sunk cost if
  the platform decision goes to Copilot Studio/Power Apps.
- **W20/CP10 ownership** (A02 vs A08) is an open Stage 6B condition; confirm before
  wiring closure.
- **Non-Silver source attributes** (tax codes, benefits, GL) and identity-key
  mapping are incomplete — needed for accurate case/exception detail.
- **Adapted ABBA assets** (validation/recalculation) require technical-fit
  validation before reuse.

---

## Hosting & demo options

The app is a **static single-page app** (Vite build → HTML/CSS/JS on a CDN).
Goal: a cheap, low-maintenance way to share the prototype with SMEs and the team.

### Key constraint — where does demo data come from?

The mock API currently runs as a **Vite dev-only middleware** (`npm run dev`
only). A plain production build has no `/api/*`, so a hosted static site needs
one of:

- **A. Client-side mock in the build** — bundle the fixtures so the static site
  is self-contained. Zero backend, zero cost, nothing to run. Best for SME demos.
  Recommended to gate behind a `VITE_DEMO=true` flag so it never ships in a real build.
- **B. Tiny hosted mock API** — same endpoints as serverless functions. More
  realistic (real network + Zod path); a little more setup.
- **C. Wait for the BFF** (Phase 1) — host only once Fabric/Foundry is wired.

For "show people now", **Option A** is the sweet spot.

### Host comparison (cost-focused)

| Host | Cost | Auth for private demo | PR/preview envs | Effort | Fit |
|------|------|----------------------|-----------------|--------|-----|
| **Azure Static Web Apps (Free)** | Free | Built-in Entra ID (lock to KPMG tenant) | Yes (per-PR) | Low | Best for KPMG — in-tenant; free Functions become the BFF on-ramp |
| Vercel / Netlify | Free tier | Password / basic (SSO paid) | Yes | Very low | Fastest shareable link |
| Cloudflare Pages | Free | Cloudflare Access (free tier) | Yes | Low | Cheap, fast CDN |
| GitHub Pages | Free | Public only | No | Low | OK if a public link is acceptable; needs SPA 404 fallback |
| Azure Blob static website + CDN | ~pennies/mo | Add Front Door/Entra (more setup) | No | Low | Cheapest raw option, fewest features |

### Recommendation

**Azure Static Web Apps, Free tier** — free for this, built-in **Entra ID**
sign-in (only KPMG people see the "KPMG Confidential" demo), **per-PR preview
URLs** (ideal for iterating with SMEs), and built-in **Azure Functions** that
become the on-ramp to the BFF (Phase 1), so the hosting isn't thrown away later.
For the quickest link with least ceremony, **Vercel/Netlify** + a demo password.

Risk is low — all data is **synthetic** (no PII, no secrets) — but access should
still be gated given the KPMG branding.

### To make it deploy-ready (when chosen)

- [ ] Add **demo mode** (`VITE_DEMO=true`) so the production build serves fixtures
      client-side (Option A) — self-contained, no backend.
- [ ] Add host config + CI deploy (SWA `staticwebapp.config.json` with SPA
      fallback + optional Entra auth, or Vercel/Netlify config).

