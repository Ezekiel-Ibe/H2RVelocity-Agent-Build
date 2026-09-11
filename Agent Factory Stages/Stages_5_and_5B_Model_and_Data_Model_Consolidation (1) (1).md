

**Stages 5 and 5B**

**Model and Data Model Consolidation**

*Define all data required by every agent, control and workflow handover,**
**then consolidate into a unified, end-to-end data model.*

Payroll Assurance — Hire to Retire Value Stream
9 Agents (A01–A09) · 20 Workflow Steps (W01–W20)

*Document classification: KPMG Confidential**
**Agent Factory Delivery Methodology*

# Contents

1. Document Control

2. Stage 5 — Model

    2.1 Objective

    2.2 Model at Two Levels

    2.3 Data Classification

    2.4 Inputs

    2.5 Actions (Steps 1–10)

    2.6 Outputs

    2.7 Practitioner Guidance

    2.8 Controls and Evidence

    2.9 Exit Criteria

    2.10 Deliverable

    2.11 Key Tools

3. Stage 5B — Data Model Consolidation

    3.1 Purpose

    3.2 Inputs

    3.3 Actions (Steps 1–13)

    3.4 Checks Performed

    3.5 Outputs

    3.6 Controls and Evidence

    3.7 Approval Gate

    3.8 Deliverable

    3.9 Key Tools

    3.10 Next Stage

4. Common Principles

5. Key Success Factors

6. Common Pitfalls

Appendix A — Agent Directory (9 Agents)

Appendix B — ABBA Agents Referenced by Workflow

Appendix C — Workflow Step Data Model (W01–W20)

Appendix D — Silver Entities Consumed by Agents

Appendix E — Data Classification Summary

Appendix F — Data Gap Log Summary

Appendix G — Between-Step Handover Map

# 1. Document Control

| Field | Value |
| --- | --- |
| Document title | Stages 5 and 5B — Model and Data Model Consolidation |
| Scope | Payroll Assurance — Hire to Retire value stream |
| Agents in scope | 9 capability agents (A01–A09) |
| ABBA agents referenced | 7 (VA-1149, VA-1249, VA-1251, VA-1253, VA-1266, VA-1267, VA-1304) |
| Additional supporting agents | VA-11343, VA-1145, VA-1148, VA-1172, VA-1246, VA-1248, VA-1279 |
| Workflow steps | W01–W20 (20 steps) |
| Version | 2.0 |
| Classification | KPMG Confidential |
| Owner | Neill Riordan |
| Status | Submitted for Factory Design Authority review |
| Decision log ref | EDM-010 |

# 2. Stage 5 — Model

*Model data for each workflow step.*

## 2.1 Objective

Identify and model all data required within each workflow step and between workflow steps.

This means defining, for every one of the 9 agents (A01–A09) and the human participants in the Payroll Assurance workflow (W01–W20):
• What data each agent consumes (inputs)
• What data each agent creates or updates (outputs)
• What data is exchanged between agents within a step
• What data is handed over from one step to the next
• How every data item is classified (enterprise model, other source, agent created, human provided)

## 2.2 Model at Two Levels

### Within Each Workflow Step

Data exchanged between agents, controls and human participants in the step.

The 9 agents operate with distinct roles:
• A03 Data Management (Task) — collects and prepares payroll data, recalculates after corrections
• A04 Exception Processing (Task) — detects anomalies, generates correction options
• A05 Analysis (Function — 4 sub-capabilities) — scores risk, classifies anomalies, determines root cause, locates system of record
• A06 Decision Intelligence (Function) — assesses impact, creates recommendations
• A07 Quality Control (Control) — validates input data and correction outcomes
• A08 Governance & Audit (Control) — creates audit evidence, logs governance actions
• A09 Human Approval Control (Control) — enforces approval authority, segregation of duties, commit authorisation
• A01 Workspace (Experience) — presents cases to the Payroll Controller, captures decisions
• A02 Orchestrator (Value Stream) — manages case lifecycle, routing, escalation, SLA, closure

ABBA agents (e.g., VA-1149, VA-1246, VA-1267) are invoked by these 9 agents within specific workflow steps but are not counted as separate agents in the architecture.

### Between Workflow Steps

Data handed from one workflow step to the next.

Between-step handovers use Silver entity keys and Case Management state:
• payroll\_run\_id — links payroll data across collection, validation, detection, recalculation
• worker\_id — links worker context across all steps
• case\_id — links assurance case lifecycle from W03 detection through W20 closure
• correction\_id — links correction from W09 options through W15 commit to W16 recalculation
• audit\_pack\_url — links evidence from W18 assembly through W20 closure

## 2.3 Data Classification

Every data item is classified using one of the following categories:

| Classification | Symbol | Definition |
| --- | --- | --- |
| Enterprise model | ✓ Already in the enterprise data model | Maps to an existing Silver canonical entity (worker, employment, compensation, payroll\_run, payroll\_line, position, organisation\_unit, absence) |
| Other source | → Exists elsewhere, not yet in model | Exists in a named source system but not (yet) in Silver. Remains in Bronze/source layer. |
| Agent created | + Created during workflow | Generated by an agent at runtime (risk scores, classifications, recommendations, calculations) |
| Human provided | 👤 Provided by a human participant | Entered by a human (approval decisions, controller comments, override values, period sign-off) |
| Does not currently exist | ⊘ Does not currently exist | Referenced but does not exist in any known system. Logged in the data gap log. |

## 2.4 Inputs

| Input | Description |
| --- | --- |
| Workflow steps | 20 workflow steps (W01–W20) from Payroll Assurance workflow |
| Agent inventory | 9 agents (A01–A09) as defined in the Stage 6 detailed designs |
| Component frameworks | Agent types: Task (A03, A04), Insight (A05, A06), Control (A07, A08, A09), Experience (A01), Orchestrator (A02) |
| Internal orchestration | Case lifecycle managed by A02 Orchestrator across W01–W20 |
| Workflow handovers | Between-step data flows documented in docs/stage-5-data-flow-map.md |
| Control points | 3 Control Agents: A07 (QC), A08 (Governance), A09 (Human Approval) |
| Overall AI Framework | Payroll Assurance agent architecture within Hire to Retire value stream |
| Enterprise data model | config/enterprise\_model.yml + sql/10\_silver/070\_workforce.sql |
| ABBA reference | 7 ABBA agents referenced by workflow steps (see Appendix B) |

## 2.5 Actions (Steps 1–10)

### 1. Identify input data for each agent and control

For each of the 9 agents (A01–A09), all input data has been identified and traced to its source.

Silver entities consumed:
• silver.worker — worker\_id, worker\_status, hire\_date, termination\_date
• silver.employment — employment\_status, employment\_type, start\_date
• silver.compensation — annual\_amount, currency\_code, component\_name, effective\_from
• silver.payroll\_run — payroll\_run\_id, pay\_period, run\_status, total\_gross, total\_net
• silver.payroll\_line — amount, hours, rate, pay\_element\_type
• silver.position — via gold.vw\_agent\_workforce (position\_title, job\_family, job\_level)
• silver.organisation\_unit — via gold.vw\_agent\_workforce (unit\_name, cost\_centre\_id)

Gold objects consumed:
• gold.dim\_worker, gold.dim\_position, gold.dim\_date
• gold.fact\_payroll\_line, gold.fact\_absence, gold.fact\_headcount
• gold.vw\_agent\_workforce, gold.vw\_agent\_compensation
• gold.vw\_agent\_payroll\_case, gold.vw\_agent\_payroll\_calculation
• gold.vw\_agent\_correction\_decision, gold.vw\_agent\_evidence\_pack, gold.vw\_agent\_control\_status

### 2. Identify data created or updated

Each agent produces specific outputs:
• A03 — collected data bundles, completeness reports, recalculation summaries
• A04 — anomaly lists (anomaly\_id, type, severity), correction options
• A05 — risk scores (0–100), anomaly classifications, root cause assessments, system of record identification, calculation explanations
• A06 — impact assessments (gross, tax, pension, net, cost centre, GL), ranked recommendations with confidence levels
• A07 — validation results (PASS/PARTIAL/FAIL), findings with severity
• A08 — audit evidence packs, governance action logs, data lineage records, agent execution records
• A09 — approval control results (AUTHORISED/REJECTED/ESCALATED), authorisation codes, period sign-off
• A01 — approval decisions (APPROVE/REJECT/ESCALATE), controller comments, override values
• A02 — case creation, step routing, escalation notifications, SLA breach alerts, case closure

### 3. Identify data consumed by controls

3 Control Agents:
• A07 Quality Control — payroll run data, data quality rules, tolerance thresholds; produces validation results and findings
• A08 Governance & Audit — case lifecycle events from all agents, data lineage metadata; produces evidence packs and governance logs
• A09 Human Approval — approval decisions, authority matrix, correction details, approver identity; produces control results and authorisation codes

### 4. Identify data passed to other agents

Within-step exchanges follow the agent-type pattern:
A03/A04 (Task) → A05/A06 (Function) → A07/A08/A09 (Control) → A01 (Experience) → A02 (Value Stream)

Key exchanges:
• A04 produces anomaly list → A05 scores and classifies
• A05 produces root cause → A06 assesses impact and recommends
• A06 produces recommendation → A01 presents to controller
• A01 produces decision → A09 validates authority → A02 routes to next step

### 5. Identify data handed to the next step

12 handover points identified using shared Silver entity keys and Case Management state.

Key handovers:
• W01→W02: Collected payroll data (payroll\_run\_id)
• W03→W04: Detected anomalies (case\_id)
• W14→W15: Approval decision (case\_id, approval\_id)
• W15→W16: Committed correction (payroll\_run\_id, correction\_id)
• W18→W20: Audit evidence (payroll\_run\_id, audit\_pack\_url)

### 6. Define entity, attributes and relationships

8 Hire to Retire Silver entities defined:
• worker (15 columns), position (14), organisation\_unit (12), employment (16)
• absence (14), compensation (16), payroll\_run (18), payroll\_line (18)

Key relationships:
• worker → party (party\_id); worker → organisation (organisation\_id)
• employment → worker (worker\_id) + position (position\_id)
• compensation → worker (worker\_id); payroll\_line → worker (worker\_id)
• position → organisation\_unit (organisation\_unit\_id)

All defined in config/enterprise\_model.yml with SQL DDL in sql/10\_silver/070\_workforce.sql.

### 7. Classify data availability

All data points classified into four categories (see Section 2.3).
Classification evidence: docs/stage-5-data-classification.csv.

### 8. Log missing data

Data gaps logged in docs/stage-5-data-gap-log.csv (358 gaps) with resolution categories:
• Source-system-specific (e.g., ni\_category, tax\_code) — remain in Bronze
• Application layer (e.g., approval\_id) — managed at application layer
• Agent created/transient (e.g., risk\_score) — no model change
• Review required (e.g., ytd\_gross) — candidate for future Silver admission

Per-agent detail in docs/complete-agent-data-gap-log.csv (889 rows).

### 9. Add missing data to the model

No new Silver entities required. The existing Hire to Retire vertical slice (8 entities) covers the canonical business data needs for all 9 agents.

Decision recorded in docs/decision-log.md (EDM-010).

### 10. Record the source and ownership

Source traceability in every Silver entity via record envelope columns:
• record\_source\_system, record\_source\_id — source origin
• fabric\_ingestion\_timestamp — ingestion time
• fabric\_effective\_from/to, fabric\_current\_indicator — SCD2 versioning
• record\_hash — change detection
• data\_classification, data\_quality\_status — governance metadata

Ownership defined in config/enterprise\_model.yml per vertical slice.

## 2.6 Outputs

| Output | Description |
| --- | --- |
| Data model per workflow step | 20 workflow step data models (W01–W20) in docs/stage-5-workflow-step-data-model.md |
| Entity and attribute definitions | 8 Silver entities in sql/10\_silver/070\_workforce.sql |
| Relationships | Foreign keys in sql/90\_post\_deploy/001\_foreign\_keys.sql |
| Data classifications | docs/stage-5-data-classification.csv |
| Data gap log | docs/stage-5-data-gap-log.csv + docs/complete-agent-data-gap-log.csv |
| Source and ownership | config/enterprise\_model.yml and Silver record envelope columns |

## 2.7 Practitioner Guidance

• Trace data through the step and to the next step — follow the flow from Bronze → Silver → Gold → Agent, and from one workflow step to the next via shared keys.

• Be specific on entities and attributes — name the exact Silver entity and column.

• Do not assume data exists — classify it. If not in the enterprise model, log it in the data gap log.

• Add missing data directly and continue — if a data item should be in Silver, add it and record the decision.

• Use ABBA to identify existing entities and common attributes — the ABBA agents referenced in the workflow provide existing patterns for payroll validation, calculation, and governance.

• Maintain clear lineage, ownership and definitions.

## 2.8 Controls and Evidence

| Control | Result | Evidence |
| --- | --- | --- |
| Evidence of data trace | ✅ | All agent inputs/outputs traced to source/destination |
| Data classification recorded | ✅ | docs/stage-5-data-classification.csv |
| Missing data logged and added | ✅ | docs/stage-5-data-gap-log.csv (358 gaps) |
| Data lineage documented | ✅ | docs/stage-5-data-flow-map.md |
| Source and ownership recorded | ✅ | config/enterprise\_model.yml + Silver record envelope |

## 2.9 Exit Criteria

Every agent, control and handover has its data requirements modelled with availability classified and any gaps added.

Verification:
• ✅ All 9 agents (A01–A09) have input/output data models
• ✅ All ABBA agents referenced by the workflow are documented (Appendix B)
• ✅ All 20 workflow steps (W01–W20) have data models
• ✅ All 12 between-step handover points are documented with shared keys
• ✅ All data points are classified
• ✅ All data gaps are logged with resolution categories
• ✅ 8 Silver entities confirmed sufficient for the Payroll Assurance scope

## 2.10 Deliverable

A complete data model for each workflow step, ready for consolidation.

Artefacts:
• docs/stage-5-workflow-step-data-model.md
• docs/stage-5-data-classification.csv
• docs/stage-5-data-gap-log.csv
• docs/stage-5-data-flow-map.md
• docs/complete-agent-data-gap-log.csv

## 2.11 Key Tools

| Tool | Purpose |
| --- | --- |
| Enterprise data model | config/enterprise\_model.yml |
| ABBA assets | Referenced agents for payroll validation, calculation, governance |
| Data modelling templates | Stage 5 workflow data model spreadsheet |
| Entity and attribute catalogues | sql/10\_silver/070\_workforce.sql; sql/20\_gold/005\_workforce\_star.sql |

# 3. Stage 5B — Data Model Consolidation

*Consolidate and approve the end-to-end data model.*

## 3.1 Purpose

Bring the data models from all workflow steps together to confirm the complete, end-to-end data model supports the full workflow.

For the Payroll Assurance scope:
• All 20 workflow steps (W01–W20) are supported by the enterprise data model
• All 9 agents (A01–A09) have their data requirements met
• All between-step handovers use consistent shared keys
• All data gaps are resolved, accepted, or logged
• The consolidated model is ready for Factory Design Authority review

## 3.2 Inputs

| Input | Source | Status |
| --- | --- | --- |
| Data models from all workflow steps | docs/stage-5-workflow-step-data-model.md (W01–W20) | ✅ Complete |
| Data classifications | docs/stage-5-data-classification.csv | ✅ Complete |
| Data gap log (with added items) | docs/stage-5-data-gap-log.csv + docs/complete-agent-data-gap-log.csv | ✅ Complete |
| Workflow handovers | docs/stage-5-data-flow-map.md | ✅ Complete |
| Agent inventory | 9 agents (A01–A09) from Stage 6 detailed designs | ✅ Complete |
| Overall AI Framework | Payroll Assurance agent architecture | ✅ Active |
| Enterprise data model | config/enterprise\_model.yml + sql/10\_silver/070\_workforce.sql | ✅ Active |
| Control requirements | 3 Control Agents (A07, A08, A09) defined with data requirements | ✅ Complete |

## 3.3 Actions (Steps 1–13)

### 1. Assemble all step data models

All 20 workflow step data models (W01–W20) assembled in docs/stage-5-workflow-step-data-model.md, mapping each step to its owning agent (A01–A09), any ABBA agents invoked, Silver entities consumed, Gold objects consumed, and non-Silver source systems.

### 2. Walk the end-to-end workflow

W01 Collect → W02 Validate → W03 Detect → W04 Score → W05 Classify → W06 Explain → W07 Root Cause → W08 Locate SoR → W09 Correction Options → W10 Impact → W11 Recommend → W12 Escalate → W13 Review → W14 Approve → W15 Commit → W16 Recalculate → W17 Validate Outcome → W18 Audit Evidence → W19 Log Governance → W20 Close Case

Each step is owned by one of the 9 agents. ABBA agents are invoked within steps but do not own them.

### 3. Trace every input to a source

Every agent input traces to one of:
(a) Enterprise model Silver entity
(b) Named source system
(c) Another agent's output
(d) A human participant

### 4. Trace every output to a consumer or storage

Agent outputs flow to:
• Agent/system destinations — Payroll Engine, HRIS, ERP, Case Management
• Audit/governance destinations — Audit Log, GRC System, Compliance Archive, Document Vault
• Human-facing destinations — Payroll Dashboard, Employee Self-Service Portal

### 5. Validate within-step data exchanges

Within each workflow step, data exchanges follow the consistent pattern:
Task Agents (A03, A04) → Function Agents (A05, A06) → Control Agents (A07, A08, A09) → Experience Agent (A01) → Value Stream Agent (A02)

This pattern is verified across all 20 workflow steps.

### 6. Validate between-step handovers

12 handover points validated using shared Silver entity keys (see Appendix G).
All handover entities are defined in Silver with surrogate keys, canonical identifiers, and source traceability.

### 7. Confirm consistent entities and attributes

Enforced by automated validation:
• scripts/validate\_model.py — verifies all entities in config/enterprise\_model.yml have corresponding SQL DDL
• tests/test\_repository.py — 9 automated tests verify naming standards, record envelope columns, idempotent DDL

The 9 agents consume the Hire to Retire Silver entities: worker, employment, compensation, payroll\_run, payroll\_line, plus position and organisation\_unit via Gold views.

### 8. Confirm agent created data destinations

Agent-created outputs confirmed:
• Risk scores, classifications, root cause → consumed by downstream agents
• Recommendations → presented to humans via A01
• Recalculated pay elements → written to silver.payroll\_line via A03
• Audit evidence → persisted to Document Vault via A08

No new Silver entities required for agent-created data.

### 9. Confirm human data capture points

Human-provided data captured at:
• Approval decisions (approve/reject/escalate) → A01 Workspace Agent
• Period sign-off → A09 Human Approval Control Agent
• Controller comments, override values → A01 Workspace interface

### 10. Identify missing data, attributes or relationships

358 data gaps logged. Per-agent detail in complete-agent-data-gap-log.csv (889 rows).

Conclusion: No new Silver entities required. The existing Hire to Retire vertical slice (8 entities) covers the canonical business data needs for all 9 agents.

### 11. Add and update as required

Model maintained via pull requests with CI validation:
• validate\_model.py must pass
• All 9 tests must pass
• CODEOWNERS review
• PR checklist completion

### 12. Repeat end-to-end check

Cross-check completed:
• ✅ All 20 workflow steps map to Silver entities
• ✅ All 9 agents have Gold analytical objects
• ✅ Magenta context package CP-005 (Hire to Retire) provides semantic context
• ✅ Handover entities use consistent keys
• ✅ Ontology relationships connect payroll entities across the workflow

### 13. Prepare for Design Authority review

This document constitutes the Stage 5B submission for Factory Design Authority review.
Decision log reference: EDM-010.

## 3.4 Checks Performed

| Check | Result | Evidence |
| --- | --- | --- |
| Every input has a defined source | ✅ | All inputs traced — Silver, source systems, agent output, or human |
| Every output has a defined consumer or storage | ✅ | All outputs — agent/system, audit/governance, or human-facing |
| Internal data exchanges are consistent | ✅ | Consistent agent-type pattern across all 20 steps |
| Step handovers are consistent and complete | ✅ | Shared payroll\_run\_id, worker\_id, case\_id at all handover points |
| Shared entities and attributes are consistent | ✅ | Enforced by validate\_model.py and test\_repository.py |
| Agent created data has a destination | ✅ | All outputs flow to downstream agents, systems, or audit stores |
| Human provided data has a capture point | ✅ | Captured via A01 and A09 |
| Control evidence is supported | ✅ | 3 Control Agents (A07, A08, A09) defined |
| Enterprise model alignment is achieved | ✅ | 8 Silver entities, Gold objects, CP-005 Magenta package |

## 3.5 Outputs

| Output | Location | Status |
| --- | --- | --- |
| Unified end-to-end data model | config/enterprise\_model.yml + sql/ | ✅ Active |
| Data dictionary | docs/silver-layer-entities.csv, gold-layer-entities.csv, magenta-layer-entities.csv | ✅ Complete |
| Relationship model | sql/90\_post\_deploy/001\_foreign\_keys.sql | ✅ Complete |
| Resolved data gap log | docs/stage-5-data-gap-log.csv + docs/complete-agent-data-gap-log.csv | ✅ Complete |
| End-to-end data trace map | docs/stage-5-data-flow-map.md | ✅ Complete |
| End-to-end data flow map | docs/hire-to-retire-layer-diagram.md + docs/layer-architecture-diagram.md | ✅ Complete |
| Data model version | v1.0.0 (config/enterprise\_model.yml) | ✅ Active |
| Change log | CHANGELOG.md | ✅ Updated |
| Evidence of cross-check | This document | ✅ Complete |
| DA approval decision | docs/decision-log.md EDM-010 | ⏳ Pending |

## 3.6 Controls and Evidence

| Evidence | Location |
| --- | --- |
| End-to-end data trace map | docs/stage-5-data-flow-map.md |
| Data model version | v1.0.0 (config/enterprise\_model.yml) |
| Change log | CHANGELOG.md |
| Evidence of cross-check | This document |
| DA approval decision | docs/decision-log.md EDM-010 — pending |

## 3.7 Approval Gate

Factory Design Authority (including SME) review required.

Approval confirms the data model supports the complete workflow.
If not approved, return affected items to Stage 5, Model.

Approval checklist:
☐ Data model supports the complete Payroll Assurance workflow (W01–W20, 9 agents)
☐ All agent, control, and handover data requirements are modelled
☐ Data availability is classified for all data items
☐ Gaps are logged, resolved, or accepted
☐ End-to-end data flow is documented and validated

Status: Submitted for review. Approval date: pending.

## 3.8 Deliverable

Approved, end-to-end data model ready to support detailed design.

## 3.9 Key Tools

| Tool | Purpose |
| --- | --- |
| Enterprise data model | config/enterprise\_model.yml |
| Data modelling templates | Stage 5 workflow data model spreadsheet |
| ABBA assets | Referenced agents for payroll patterns |
| Data lineage tools | docs/stage-5-data-flow-map.md |

## 3.10 Next Stage

Proceed to Stage 6 — Design with an approved end-to-end data model.

Stage 6 detailed designs for each agent (A01–A09) are in docs/stage-6-detailed-designs/.

# 4. Common Principles

• Model at both levels — within the step and between steps.
• Classify every data item.
• Log and add missing data — no separate approval required for additions.
• Maintain clear lineage, ownership and definitions.

# 5. Key Success Factors

• Complete and accurate data trace.
• Consistent entity and attribute definitions (enforced by automated validation).
• Early identification of missing data.
• Clear handovers and evidence for controls.

# 6. Common Pitfalls

• Missing handover data between steps.
• Inconsistent entity or attribute definitions.
• Assuming data exists without classifying it.
• Not validating the combined model end-to-end.

# Appendix A — Agent Directory (9 Agents)

| Agent | Agent ID(s) | Name | Type | Role in Workflow |
| --- | --- | --- | --- | --- |
| A01 | VA-14259 | Payroll Assurance Workspace Agent | Experience | Presents cases to controller; captures decisions |
| A02 | VA-14260 | Payroll Assurance Orchestrator | Value Stream | Case lifecycle, routing, escalation, SLA, closure |
| A03 | VA-14254 | Payroll Data Management Agent | Task | Collects payroll data; recalculates after corrections |
| A04 | VA-14261 | Payroll Exception Processing Agent | Task | Detects anomalies; generates correction options |
| A05 | VA-14255/56/57/58 | Payroll Analysis Agent (4 sub-capabilities) | Function | Risk scoring, classification, root cause, system of record, calculation explanation |
| A06 | VA-14262 | Payroll Decision Intelligence Agent | Function | Impact assessment; ranked recommendations |
| A07 | VA-14263 | Payroll Quality Control Agent | Control | Input validation (W02); outcome validation (W17) |
| A08 | VA-14264 | Payroll Governance & Audit Agent | Control | Audit evidence; governance action logging |
| A09 | VA-14265 | Human Approval Control Agent | Control | Authority checks; segregation of duties; commit authorisation; period sign-off |

# Appendix B — ABBA Agents Referenced by Workflow

These agents are invoked by the 9 capability agents (A01–A09) within specific workflow steps. They are not separate agents in the architecture.

| ABBA Agent ID | Referenced In | Invoked By | Context |
| --- | --- | --- | --- |
| VA-1149 | W03 Detect Anomalies | A04 | Policy enforcement & anomaly detection |
| VA-1266 | W03 Detect Anomalies | A04 | Supplementary detection logic |
| VA-1267 | W06 Explain Payroll Calculation | A05 | Payroll experience agent |
| VA-1253 | W06 Explain Payroll Calculation | A05 | Payroll experience agent |
| VA-1304 | W16 Recalculate Payroll | A03 | Data governance monitor |
| VA-1249 | W16 Recalculate Payroll | A03 | Payroll administration workflow manager |
| VA-1251 | W17 Validate Outcome | A07 | Payroll value stream manager |

Additional supporting agents referenced in the agent catalogue but not ABBA-designated:

| Agent ID | Name | Type | Referenced In |
| --- | --- | --- | --- |
| VA-11343 | Payroll Recalculate | Task | W15 Commit Correction |
| VA-1145 | Automated payroll calculations agent | Task | W14 Approve |
| VA-1246 | Payroll data validator | Task | W02 Validate, W15 Commit |
| VA-1248 | Automated payroll calculations agent | Task | W14 Approve |
| VA-1172 | Data validation agent | Task | W02 Validate |
| VA-1279 | Time record validator | Task | W02 Validate |

# Appendix C — Workflow Step Data Model (W01–W20)

| Step | Name | Owner Agent | ABBA Invoked | Silver Entities | Key Non-Silver Sources |
| --- | --- | --- | --- | --- | --- |
| W01 | Collect Payroll Data | A03 | — | worker, employment, compensation, payroll\_run, payroll\_line | HRIS, Benefits Admin, Time & Attendance, Tax Engine, ERP GL |
| W02 | Validate Input Data | A07 | VA-1246, VA-1172, VA-1279 | worker, employment, compensation, payroll\_run, payroll\_line | HRIS, Payroll System, Time Tracking, Identity API |
| W03 | Detect Anomalies | A04 | VA-1149, VA-1266 | compensation, payroll\_line | HRIS, Time & Attendance, Payroll Engine |
| W04 | Calculate Risk Score | A05 | — | worker, compensation, payroll\_run, payroll\_line | Payroll System, Compliance Rules Engine |
| W05 | Classify Anomaly | A05 | — | payroll\_line, compensation | HRIS, Benefits Admin, Garnishment System |
| W06 | Explain Payroll Calculation | A05 | VA-1267, VA-1253 | payroll\_line, compensation | Payroll System |
| W07 | Determine Root Cause | A05 | — | worker, compensation, payroll\_line | HRIS, GL/ERP, Compliance API |
| W08 | Locate System of Record | A05 | — | payroll\_run | Payroll Engine, MDM Directory |
| W09 | Generate Correction Options | A04 | — | worker, payroll\_line, compensation | HRIS, Payroll Engine, Finance GL |
| W10 | Assess Impact | A06 | — | payroll\_line, compensation | Payroll Engine, Tax Engine, Benefits Admin |
| W11 | Create Recommendation | A06 | — | (as W10) | (as W10) |
| W12 | Escalate for Approval | A02 | — | payroll\_run | Case Management, Identity/SSO |
| W13 | Review Recommendation | A01 + A09 | — | worker, payroll\_run, payroll\_line | Payroll System, HRIS, Case Mgmt |
| W14 | Approve, Reject or Escalate | A01 + A09 | VA-1145, VA-1248 | payroll\_line, compensation | HRIS, Payroll System, Tax API |
| W15 | Commit Correction | A02 + A09 | VA-11343, VA-1246 | payroll\_run, payroll\_line | HRIS, Payroll System, HMRC API |
| W16 | Recalculate Payroll | A03 | VA-1304, VA-1249 | payroll\_run, payroll\_line | Payroll System, Tax Engine |
| W17 | Validate Outcome | A07 | VA-1251 | payroll\_run, payroll\_line | HRIS, Benefits Admin, Controls Config |
| W18 | Create Audit Evidence | A08 | — | payroll\_run | Payroll System, Case Mgmt, Data Lake |
| W19 | Log Governance Actions | A08 | — | (as W18) | (as W18) |
| W20 | Close Case | A02 | — | payroll\_run | Case Management |

# Appendix D — Silver Entities Consumed by Agents

| Silver Entity | Agents Consuming | Key Fields Used |
| --- | --- | --- |
| silver.worker | A01, A03, A04, A05, A07 | worker\_id, worker\_status, hire\_date, termination\_date |
| silver.employment | A03 | employment\_status, employment\_type, start\_date |
| silver.compensation | A03, A04, A05, A06 | annual\_amount, currency\_code, component\_name, effective\_from |
| silver.payroll\_run | A02, A03, A05, A07, A08, A09 | payroll\_run\_id, pay\_period, run\_status, total\_gross, total\_net |
| silver.payroll\_line | A01, A03, A04, A05, A06, A07 | amount, hours, rate, pay\_element\_type |
| silver.position | via gold.vw\_agent\_workforce | position\_title, job\_family, job\_level |
| silver.organisation\_unit | via gold.vw\_agent\_workforce | unit\_name, cost\_centre\_id |

# Appendix E — Data Classification Summary

| Classification | Examples | Model Action |
| --- | --- | --- |
| Enterprise model (in Silver) | worker\_id, annual\_amount, payroll\_run\_id | No action — already in model |
| Other source (outside Silver) | ni\_category, tax\_code, pension\_scheme\_id | Remains in Bronze/source layer |
| Agent created | risk\_score, anomaly\_class, recommendation\_id | Transient — no model change |
| Human provided | approval\_decision, controller\_comment, override\_value | Captured at application layer |

# Appendix F — Data Gap Log Summary

| Resolution Category | Example Data Points | Action |
| --- | --- | --- |
| Covered — mapped to Silver | employee\_id → silver.worker.worker\_id | Confirmed mapping |
| Gap — Source-system-specific | ni\_category, tax\_code, pension\_scheme\_id | Remains in Bronze |
| Gap — Application layer | approval\_id, approver\_id, attachment\_count | Managed by application layer |
| Gap — Agent created/transient | risk\_score, anomaly\_id, alert\_severity | No model change |
| Gap — Review required | ytd\_gross, ledger\_account\_map | Candidate for future Silver admission |

# Appendix G — Between-Step Handover Map

| # | Source Step | Target Step | Shared Key | Handover Data |
| --- | --- | --- | --- | --- |
| H01 | W01 Collect | W02 Validate | payroll\_run\_id | Collected data bundle |
| H02 | W02 Validate | W03 Detect | payroll\_run\_id, worker\_id | Validated payroll records |
| H03 | W03 Detect | W04 Score | case\_id | Anomaly list + exception case IDs |
| H04 | W04 Score | W05 Classify | case\_id, risk\_score | Risk-scored anomalies |
| H05 | W05 Classify | W06 Explain | case\_id | Classified anomalies |
| H06 | W07 Root Cause | W08 Locate SoR | case\_id | Root cause + contributing systems |
| H07 | W08 Locate SoR | W09 Corrections | case\_id, source\_system\_id | System of record identification |
| H08 | W10 Impact | W11 Recommend | case\_id | Impact assessment |
| H09 | W13 Review | W14 Approve | case\_id, approval\_id | Review recommendation |
| H10 | W15 Commit | W16 Recalculate | payroll\_run\_id, correction\_id | Committed correction |
| H11 | W16 Recalculate | W17 Validate | payroll\_run\_id | Recalculated payroll lines |
| H12 | W18 Audit | W20 Close | payroll\_run\_id, audit\_pack\_url | Audit evidence pack |

*— End of Document —*

