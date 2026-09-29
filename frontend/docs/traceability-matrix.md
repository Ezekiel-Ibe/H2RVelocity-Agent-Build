# Traceability & Reconciliation Matrix

Reconciles the frontend against the approved Agent Factory artefacts (Stages 3,
4, 5/5B, 6B, 7A). The initial UI was built from the visual reference; this matrix
tracks alignment to the approved capability and data model.

## Source artefacts

| Stage | Document | Key contribution |
|-------|----------|------------------|
| 3 | Decompose | Capability, L3 Augmented+ autonomy, W01–W20, Payroll Controller owner |
| 4 | Classify (Capability-Based) | 9 agents (A01–A09), A01 workspace framework, CP01–CP10, seven anomaly classes |
| 5 / 5B | Model & Data Model Consolidation | Silver entities, Gold agent views, shared keys, handovers |
| 6B | Consolidation & Build Readiness | Consolidated design, control coverage, open conditions B-01…B-06 |
| 7A | Build, Unit Test & Technical Review | A01 build spec, common component contract, technology decision |

## Reconciliation status

| # | Area | Approved model | Action | Status |
|---|------|----------------|--------|--------|
| 1 | Primary object | Assurance **cases** (`case_id`, W01–W20) for the Payroll Controller | Replace "Engagements" with **Cases** | Done |
| 2 | Anomalies | Seven approved classes (Stage 4 §8 A04 / 7A §4.4) | Replace fixtures with the seven classes | Done |
| 3 | Human approval | A01 review + Approve/Reject/Escalate, mandatory rationale (CP05/CP06) | Add decision panel to case detail | Planned |
| 4 | Technology | Experience = Copilot Studio + Power Apps/Dataverse (7A §3) | Record React departure (ADR-008) | Done |
| 5 | Contracts | Silver entities + Gold agent views + shared keys | Update Zod contracts + api-contracts.md | Partial |
| 6 | Case detail objects | Risk score/bands, root cause, options, impact, recommendation, control results CP01–CP10, evidence pack | Model + build case-detail view | Planned |
| 7 | Agent boundary | Foundry narrative-only; cite `evidence_id`/`calculation_id`; `INSUFFICIENT_EVIDENCE` | Reflect evidence citations in agent replies | Planned |
| 8 | Navigation | Controller-facing: Cases, Exceptions, Approvals, Audit Trail, Reports, Insights | Align nav labels/paths | Partial |

## The seven approved anomaly classes (Stage 4 §8 / Stage 7A §4.4)

1. Leaver still paid
2. Joiner not paid
3. Unexplained variance (e.g. >45%)
4. Missing tax code
5. Negative net pay
6. Duplicate pay record
7. Unapproved change

## Controls (CP01–CP10)

| Control | Owner agent | Steps |
|---------|-------------|-------|
| CP01 Input completeness | A07 | W02 |
| CP02 Approved anomaly rule | A04 | W03 |
| CP03 Risk and severity | A05 | W04–W05 |
| CP04 Evidence sufficiency | A06 | W10–W11 |
| CP05 Mandatory human approval | A09 | W13–W15 |
| CP06 Segregation of duties | A09 | W14–W15 |
| CP07 Post-correction validation | A07 | W17 |
| CP08 Audit evidence completeness | A08 | W18 |
| CP09 Governance logging | A08 | W19 |
| CP10 Case closure | A02 (7A) / A08 (workflow) — open condition | W20 |

## Data model mapping (Stage 5/5B)

Shared keys used across the workflow: `case_id`, `payroll_run_id`, `worker_id`,
`correction_id`, `audit_pack_url`. Frontend consumes Gold agent views through the
BFF — see [api-contracts.md](api-contracts.md):

- `gold.vw_agent_payroll_case` → Cases
- `gold.vw_agent_control_status` → control results (CP01–CP10)
- `gold.vw_agent_correction_decision` → recommendations / approvals
- `gold.vw_agent_evidence_pack` → audit evidence
- `silver.worker`, `silver.payroll_run`, `silver.payroll_line`, `silver.compensation`

## Note on the React workspace

Stage 7A §3 selects the Experience layer as **Copilot Studio + Power Apps /
Dataverse**. This React/Fluent workspace is therefore a **departure** from the
approved Technology Decision Register and is recorded as ADR-008 in
[decision-log.md](decision-log.md). It should be treated as a prototype /
alternative pending Factory Design Authority direction.
