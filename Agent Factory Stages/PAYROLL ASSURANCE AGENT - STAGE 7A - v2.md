# **PAYROLL ASSURANCE AGENT**
**STAGE 7A – BUILD, UNIT TEST & TECHNICAL REVIEW**
Agent Factory implementation working package for A01–A09

| **Document ID** | HR-RTP-001-S7A |
| --- | --- |
| **Version** | Working Draft v1.0 |
| **Status** | Build-ready working document; execution and approval evidence to be attached |
| **Scope** | Nine components A01–A09; workflow W01–W20; controls CP01–CP10 |
| **Prepared for** | Developers, Solution Architects, Technical Reviewers and Factory Design Authority |
| **Owner persona** | Payroll Controller |
| **Classification** | KPMG Confidential |

**EXIT GATE:** Do not progress to Stage 7B until every assigned component has an approved build record, mandatory unit tests have passed, technical-review findings are closed or formally accepted, and the technical reviewer records completion.

# 1. Executive Summary

Stage 7A converts the approved Payroll Assurance design into versioned, controlled and individually reviewed implementation assets. The solution comprises nine capability components: one Experience component, one Orchestration component, two Task components, two Insight components and three Control components. The end-to-end workflow detects, explains, diagnoses and recommends; consequential payroll corrections and payroll-period sign-off remain subject to authorised human approval.

**Design boundary.** Deterministic services own payroll calculations, anomaly rules, validation, reconciliation, materiality and risk inputs. Generative AI may produce grounded explanations and advisory recommendation narratives, but it cannot invent payroll values, approve changes, commit corrections or close a case.

| **Required deliverable** | **Definition of done** | **Working status** |
| --- | --- | --- |
| Built Component Specification | A01–A09 artefacts checked in and aligned to approved boundaries | Specification complete; runtime evidence pending |
| Implemented Controls Documentation | CP01–CP10 implemented with positive and negative-path evidence | Design complete; runtime evidence pending |
| Internal Orchestration Design | State, routing, retry, timeout, idempotency and re-entry implemented | Design complete; runtime evidence pending |
| Handover & Integration Specification | Versioned contracts, correlation, acknowledgement and errors tested | Contracts defined; test evidence pending |
| Unit Test Evidence and Results | Approved tests executed; failures retained and re-tested | Catalogue defined; execution not asserted |
| Technical Review Report | Independent checklist complete and findings resolved | Template ready; approval pending |
| Updated Implementation Documentation | As-built design, configuration, runbook and change log current | Working baseline created |
| Technology Decision Register | Architecture decisions recorded and approved | Recommended stack adopted subject to environment validation |

# 2. Source Basis, Inputs and Traceability

| **Input** | **Stage 7A use** | **Entry evidence** |
| --- | --- | --- |
| Stage 6B Build-Ready Design | Primary component, control, handover, readiness and technology baseline | Approved version and disposition of open conditions |
| Approved Data Model | Canonical Silver/Gold objects, shared keys, lineage and source-gap treatment | Approved model version and mapping reference |
| Unit Test Scenarios | Positive, negative, boundary, failure, security and recovery acceptance criteria | Scenario catalogue, test data and expected results |
| Control Specifications | CP01–CP10 implementation, ownership, fail-safe behaviour and evidence | Control acceptance criteria and evidence mapping |
| Technology Recommendations | Starting architecture and platform constraints | Approved or conditionally accepted recommendation |
| Component Allocation Matrix | Builder, reviewer, interfaces, dependencies and delivery boundary | Named ownership and interface accountability |

**Entry rule.** Inputs must be approved, versioned and traceable. Ambiguities are logged with an owner. Thresholds, physical mappings, role titles, retention periods and business rules are not silently invented.

# 3. Architecture and Technology Decision

| **Layer** | **Selected implementation** | **Rationale** |
| --- | --- | --- |
| Experience | Copilot Studio plus governed Power Apps/Dataverse workspace | Role-aware case review, evidence access and secure human decisions |
| State and orchestration | Dataverse plus Power Automate; Azure integration services for durable external calls | Authoritative state, routing, retries, escalation and commit gates |
| Data | Microsoft Fabric Bronze/Silver/Gold and OneLake | Trusted snapshots, canonical keys, lineage and deterministic controls |
| Deterministic services | Fabric SQL/notebooks and governed Azure Functions/APIs | Versioned, repeatable payroll rules, calculations and validation |
| AI and evaluation | Azure AI Foundry | Grounded explanations and recommendation narratives only |
| Identity and security | Microsoft Entra ID, managed identities, RBAC and DLP | Least privilege, service authentication, SoD and environment protection |
| Reporting | Power BI over certified semantic models | Role-aware assurance status, trends and evidence completeness |
| Evidence and monitoring | Immutable evidence store plus AgentOps operational telemetry | Separate business evidence from technical monitoring |
| Engineering lifecycle | Managed solutions, source control and CI/CD | Versioned promotion, automated tests, approvals and rollback |

## 3.1 Common Component Contract

| **Envelope area** | **Required fields and behaviour** |
| --- | --- |
| Identity | case\_id, execution\_id, payroll\_run\_id, worker\_id and correction\_id where applicable |
| Versioning | schema\_version, component\_version, rule\_version, prompt/model version and configuration effective date |
| Security | actor/service identity, role, purpose, authorisation context and data classification |
| Evidence | evidence\_id, source reference, hash, event time, producer and lineage |
| Reliability | correlation\_id, idempotency\_key, attempt number, retry eligibility, acknowledgement and safe re-entry state |
| Outcome | status, result payload, control results, error category, owner and explicit next\_state |

# 4. Technical Details for the Nine Capability Agents

## 4.1 System Architecture Overview

The Payroll Assurance solution uses a layered, capability-based architecture. A01 provides the controlled user experience; A02 is the authoritative workflow orchestrator and case-state coordinator; A03 and A04 perform operational data and exception-processing tasks; A05 and A06 provide analysis and decision intelligence; and A07, A08 and A09 enforce quality, audit and human-approval controls. Microsoft Fabric supplies governed Bronze, Silver and Gold data; Dataverse stores case and approval state; Power Automate and Azure integration services coordinate durable handovers; Azure AI Foundry supports grounded narrative generation; and Entra ID, managed identities, role-based access control and data-loss prevention secure access. Deterministic services remain authoritative for payroll calculations, rules, validation, approvals and write-back.

| **Architecture layer** | **Primary agents** | **Technical role** | **Core platform dependencies** |
| --- | --- | --- | --- |
| Experience | A01 | Role-aware case review, evidence access and decision capture | Copilot Studio, Power Apps, Dataverse, Entra ID |
| Orchestration | A02 | Case state, workflow sequencing, routing, retries, escalation and closure transition | Dataverse, Power Automate, Azure integration services |
| Task processing | A03, A04 | Data acquisition, recalculation, anomaly detection and correction-option generation | Fabric pipelines, SQL/notebooks, payroll and source-system APIs |
| Insight | A05, A06 | Risk, classification, explanation, root cause, impact and recommendation | Fabric deterministic services, Azure Functions/APIs, Azure AI Foundry |
| Control | A07, A08, A09 | Data quality, post-correction validation, immutable evidence, authority and SoD | Fabric controls, immutable evidence store, AgentOps, Dataverse, Entra ID |

## 4.2 Key Components and Dependencies

| **Agent** | **Technical responsibility** | **Upstream dependencies** | **Downstream dependencies** |
| --- | --- | --- | --- |
| A01 Workspace | Presents case, evidence and permitted decisions; captures rationale and overrides | A02 case state; A05/A06 analysis; A07 controls; A08 evidence; Entra identity | A09 approval control; A02 routing; A08 audit events |
| A02 Orchestrator | Owns workflow state, transition guards, SLA, retry, escalation and final close event | Payroll trigger; outcomes from A01 and A03–A09 | All component routing; Dataverse case state; operational alerts |
| A03 Data Management | Collects source data, creates versioned snapshots and invokes approved recalculation | HRIS, payroll, time, benefits, tax, GL, Fabric and A09 authorisation | A07 validation; A02 state; A08 evidence |
| A04 Exception Processing | Runs approved anomaly rules and produces controlled correction options | A07 validated snapshot; rule catalogue; policy and source references | A05 analysis; lifecycle handover; A08 evidence |
| A05 Analysis | Calculates risk/classification and produces grounded explanation, root cause and source location | A04 anomalies; calculation trace; policies; lineage; source registry | A06 decision intelligence; A01 presentation; A08 evidence |
| A06 Decision Intelligence | Calculates option impacts and produces an evidence-backed advisory recommendation | A05 analysis; A04 options; tax, pension, benefits, GL and policy context | A02 approval route; A01 review; A09 control; A08 evidence |
| A07 Quality Control | Validates input completeness and post-correction outcome | A03 snapshots/recalculation; rule configuration; A04 detection logic | A04 detection; A02 rework route; A08 evidence |
| A08 Governance & Audit | Collects events, builds immutable evidence, logs governance and attests closure readiness | Events and evidence from A01–A09; lineage and retention configuration | A01 evidence view; A02 closure decision; audit and compliance stores |
| A09 Human Approval Control | Enforces authority, delegation, SoD, dual approval, commit authorisation and sign-off | A01 decision; A02 state; Entra identity; authority matrix; correction hash | A02 commit route; A03 recalculation; A08 approval evidence |

## 4.3 Data Flow Description

1. **Trigger and case creation:** A payroll-calendar event or authorised manual request causes A03 to create a case in Dataverse/Fabric with case\_id, payroll\_run\_id, correlation\_id, SLA and initial state.

2. **Collection:** A03 retrieves Silver layer worker, employment, compensation, payroll-run and payroll-line records and stages source-specific data from HRIS, payroll, time, benefits, tax and GL through governed Bronze layer in Fabric. It produces a versioned snapshot, source counts, hashes and lineage.

3. **Input validation:** A03 passes the snapshot reference to A07. A07 executes completeness, referential, temporal, validity, reconciliation and cross-source checks. A failed blocking rule returns the case to controlled hold; a valid result advances to anomaly detection.

4. **Detection and analysis:** A07 passes the validated dataset to A04. A04 executes the approved seven-anomaly catalogue and sends anomalies, rule versions and matched evidence to A05. A05 calculates risk and classification, builds calculation explanations, identifies root cause and locates the system of record.

5. **Options and recommendation:** A04 generates correction options using A05 root-cause and source information. A05 and A04 outputs are passed to A06, which calculates deterministic payroll, tax, pension, benefits and GL impacts and prepares a grounded advisory recommendation.

6. **Human review and approval:** A06 sends the recommendation package to A02. A02 exposes it through A01 and invokes A09. A01 captures the human decision and rationale; A09 validates identity, authority, delegation, SoD, dual approval and correction integrity.

7. **Commit and recalculation:** When A09 produces valid authorisation, A02 issues an idempotent commit instruction to A03. A03 invokes the payroll write-back/recalculation interface, records the receipt and retrieves the recalculated output.

8. **Outcome validation and evidence:** A03 passes before/after values and recalculated results to A07. A07 compares expected and actual outcomes and reruns applicable anomaly checks. A08 continuously receives evidence events, then creates the manifest, governance log and closure attestation.

9. **Closure:** A02 closes the case only after A08 attests evidence completeness and all control results and open actions satisfy CP10. Failed validation, rejected approval, incomplete evidence or unresolved integration status follows an explicit rework or held-state route.

## 4.4 Known Integration Constraints

| **Constraint** | **Technical impact** | **Required treatment** |
| --- | --- | --- |
| W20/CP10 ownership remains subject to formal approval | Competing closure responsibilities can create duplicate or unauthorised state transitions | Use A08 for evidence attestation and A02 for the single authoritative close transition; obtain Factory Design Authority approval |
| Onboarding & Lifecycle capability is not yet available | Joiner-not-paid and leaver-still-paid cases cannot complete an automated external investigation | Use a versioned adapter, ACK/NACK/timeout contract, manual fallback and controlled re-entry state |
| Physical source-to-canonical mappings and identity keys are incomplete | Worker, lifecycle, time, benefits and payroll records may not join consistently | Approve mapping specifications and identity-matching rules; quarantine ambiguous records |
| Non-Silver source attributes are required | Tax codes, benefits, timesheets, GL mappings and authority data are not all represented in Silver | Use governed Bronze/API schemas with canonical keys, classification, lineage and ownership |
| Write-back, rollback and status-reconciliation contract is not final | A timeout after submission could cause duplicate payroll changes or an unknown outcome | Require idempotency keys, signed authorisation, status query/read-back, no blind retry and controlled rollback |
| Blocking/warning rules, risk bands and materiality thresholds require approval | Components cannot safely apply invented defaults or produce final expected results | Maintain versioned configuration and fail closed or return INSUFFICIENT\_EVIDENCE where mandatory values are absent |
| Delegation, expiry, dual approval and period sign-off semantics remain conditional | A09 cannot finalise every authority path without an approved authority model | Version the authority matrix and test direct, delegated, expired, dual-approval and SoD scenarios |
| Evidence-store retention, legal hold and access pattern are open | A08 cannot assert final retention or disposal behaviour | Keep retention configurable and obtain Governance/Privacy approval before production |
| Adapted validation and recalculation assets are not yet technically proven | Schema, Fabric compatibility, security and control behaviour may differ from the target design | Complete contract, security, evidence and regression tests before reuse |
| AI service is non-authoritative and may be unavailable | Narrative generation may fail or return insufficiently grounded text | Preserve deterministic outputs, enforce evidence citations, evaluate prompts and provide structured fallback without narrative |

# 5. Component Allocation and Build Specifications

Components should be built in parallel against the common contract, fixed schema versions and explicitly owned interfaces. Each package must include source/configuration, automated tests, security configuration, evidence events, deployment metadata and a technical-review record.

## 4.1 A01 – Payroll Assurance Workspace Agent

| **Overview** | Experience component supporting W13–W14; gives the Payroll Controller a secure case, evidence and decision workspace. |
| --- | --- |
| **Dependencies and integrations** | A02, A08, A09, Entra ID, Dataverse, secure evidence links. |
| **Inputs** | Case status, worker context, anomaly, risk, root cause, recommendation, calculation trace, control results and evidence manifest. |
| **Outputs** | ApprovalDecision, rationale, comments, override request, escalation request and review telemetry. |
| **Technology** | Copilot Studio plus Power Apps/Dataverse. No Stage 6B platform departure. |
| **Build approach** | Configure role-aware case views, evidence drill-down, allowed actions, mandatory rationale, optimistic locking, immutable post-submit state and secure links. Use environment variables and connection references. |
| **Security and data controls** | Authenticate with Entra ID; enforce role-based case access; minimise displayed worker data; prevent sensitive content in notifications and technical logs. |
| **Error handling** | Retry read-only retrieval; preserve draft decisions; reject invalid choices or overrides; route missing evidence and SLA breaches through A02. |
| **Controls** | Participates in CP05 and CP06; evidence includes actor, timestamp, rationale, allowed action set and immutable decision record. |
| **Unit tests** | Approve/reject/escalate, missing or short rationale, override without justification, concurrent decision, unauthorised case access, incomplete evidence and SLA breach. |
| **Technical-review focus** | Role model, data minimisation, decision immutability, accessibility, evidence trace and no hidden approval bypass. |

## 4.2 A02 – Payroll Assurance Orchestrator

| **Overview** | Orchestration component managing case state, W01–W20 sequencing, routing, escalation, commit coordination and closure. |
| --- | --- |
| **Dependencies** | All A01–A09 contracts, Dataverse, Power Automate, external integration adapters and AgentOps. |
| **Inputs/outputs** | Consumes triggers, step outcomes, approvals and control results; emits state transitions, routing instructions, SLA events, commit and closure instructions. |
| **Technology** | Dataverse and Power Automate with Azure durable integration for long-running or transactional external calls. |
| **Build approach** | Implement explicit state machine, transition guards, correlation, idempotency, deterministic retries, timeout, dead-letter route, compensation, re-entry and closure checklist. |
| **State management** | Dataverse is authoritative. Each transition records from\_state, to\_state, trigger, actor, timestamp, contract version and evidence reference. |
| **Error handling** | No blind retry after consequential submission. Query status using idempotency key; hold orphaned cases; expose owner, SLA and safe next state. |
| **Controls** | CP10 executor. A08 attests evidence completeness; A02 performs the final authoritative close transition after no open actions or failed controls remain. |
| **Unit tests** | Happy-path state flow, rejection, escalation, timeout, duplicate commit, invalid transition, stuck case, re-entry, lifecycle return and closure blocked/passed. |
| **Technical-review focus** | Single state authority, loop prevention, idempotency, safe failure, re-entry correctness and CP10 ownership. |

## 4.3 A03 – Payroll Data Management Agent

| **Overview** | Task component supporting W01 data collection and W16 recalculation/read-back. |
| --- | --- |
| **Dependencies** | Fabric, HRIS, payroll, time, benefits, tax, GL, source APIs, A02, A07 and A09. |
| **Inputs** | Payroll scope; worker, employment, compensation, payroll run/line data; controlled Bronze/API contracts for source-specific fields; approved correction. |
| **Outputs** | Versioned source snapshot, completeness report, lineage, recalculation request/result, write-back receipt and before/after values. |
| **Technology** | Fabric pipelines, notebooks and SQL with governed APIs/Functions for payroll integration. |
| **Build approach** | Create idempotent extraction pipelines, snapshot/hash metadata, canonical key mapping, schema validation, controlled Bronze staging, approved write-back adapter and status read-back. |
| **Data handling** | Encrypt in transit/at rest; retain purpose and classification; use worker\_id, payroll\_run\_id and source identifiers; prohibit unmasked payroll values in logs. |
| **Error handling** | Classify source failure, partial data and stale data. Hold mandatory-source failure. For unknown write-back status, query before any retry. |
| **Controls** | Supports CP01 and evidence for extraction, version, source counts, hashes, approvals, idempotency and recalculation deltas. |
| **Unit tests** | Complete snapshot, missing mandatory source, partial optional source, stale data, identity mismatch, duplicate request, approved recalculation and timeout-after-submit. |
| **Technical-review focus** | Physical mappings, non-Silver contracts, lineage, idempotency, write-back authority and rollback/read-back. |

## 4.4 A04 – Payroll Exception Processing Agent

| **Overview** | Task component supporting W03 anomaly detection and W09 correction-option generation. |
| --- | --- |
| **Dependencies** | A07 validated snapshot, Fabric data, versioned rule catalogue, A05 analysis, policy and source ownership references. |
| **Inputs/outputs** | Consumes validated payroll/workforce evidence and rules; produces anomaly register, matched records, rule version, evidence and controlled correction options. |
| **Technology** | Fabric SQL/notebooks and governed Functions/APIs; deterministic rules are authoritative. |
| **Build approach** | Implement the seven approved classes: leaver still paid, joiner not paid, unexplained variance, missing tax code, negative net pay, duplicate pay record and unapproved change. External lifecycle cases use a versioned adapter. |
| **Configuration** | Thresholds, tolerances, effective dates, duplicate keys and approved reason codes are version-controlled configuration, not hard-coded defaults. |
| **Error handling** | Reject stale/unapproved rules; return INSUFFICIENT\_DATA rather than guessing; hold lifecycle cases on timeout or NACK and route manual investigation. |
| **Controls** | CP02. Evidence includes rule ID/version, input snapshot hash, matched record IDs, result, effective date and execution identity. |
| **Unit tests** | Each anomaly class, no-anomaly path, threshold boundary, zero denominator, duplicate window, missing evidence, unapproved rule, lifecycle ACK/NACK/timeout/re-entry. |
| **Technical-review focus** | Rule approval, reproducibility, false-positive controls, option boundaries and no A04-to-A06 analysis bypass. |

## 4.5 A05 – Payroll Analysis Agent

| **Overview** | Insight component supporting W04–W08 risk, classification, calculation explanation, root cause and system-of-record location. |
| --- | --- |
| **Dependencies** | A04 anomaly register, Fabric calculation trace and lineage, approved policies, source registry and AI Foundry. |
| **Inputs/outputs** | Consumes anomaly, payroll calculation, policy and evidence; produces factor-level risk, classification, explanation, root-cause assessment and source reference. |
| **Technology** | Deterministic Fabric/Function services plus Azure AI Foundry for grounded narrative and evaluation. |
| **Build approach** | Calculate factor values and bands deterministically; use versioned prompts P-01/P-02 only to explain supplied facts. Every material number must reference evidence\_id or calculation\_id. |
| **AI boundary** | Missing, stale or contradictory evidence returns INSUFFICIENT\_EVIDENCE. No unsupported assertion, invented value, approval or correction. |
| **Error handling** | Return structured analysis without narrative if AI is unavailable; route unclassified or low-confidence source cases for manual review. |
| **Controls** | CP03. Evidence includes factors, weights, band, rule/config version, prompt/model version, grounding references and evaluation result. |
| **Unit tests** | Risk boundaries, incomplete factors, classification categories, complete/missing calculation evidence, source lookup, prompt grounding, hallucination checks and AI outage. |
| **Technical-review focus** | Approved weights/bands, deterministic arithmetic, grounded prompts, evaluation thresholds and evidence completeness. |

## 4.6 A06 – Payroll Decision Intelligence Agent

| **Overview** | Insight component supporting W10–W11 impact assessment and evidence-backed advisory recommendation. |
| --- | --- |
| **Dependencies** | A05 analysis, correction options, tax/pension/benefits/GL context, policy constraints and AI Foundry. |
| **Inputs/outputs** | Consumes root cause, options and deterministic context; produces option impacts, evidence sufficiency result, ranked advisory recommendation and rationale. |
| **Technology** | Governed deterministic impact service plus Azure AI Foundry for grounded comparison narrative. |
| **Build approach** | Calculate gross, tax, NI, pension, benefit, net, cost-centre and GL impacts deterministically. Compare approved options using versioned criteria; AI narrates but does not select outside supplied scores. |
| **Error handling** | Do not substitute stale reference data silently. Mark estimate status and evidence age; if required evidence is missing, withhold recommendation and route for data completion. |
| **Controls** | CP04. Evidence includes input options, calculations, alternatives, ranking factors, confidence, prompt/model version and cited supporting evidence. |
| **Unit tests** | Single/multiple options, threshold boundary, missing tax/GL evidence, zero-impact option, low-confidence options, grounded rationale and AI unavailable fallback. |
| **Technical-review focus** | Calculation authority, materiality configuration, evidence sufficiency, unbiased option comparison and explicit human decision request. |

## 4.7 A07 – Payroll Quality Control Agent

| **Overview** | Control component supporting W02 input validation and W17 post-correction validation. |
| --- | --- |
| **Dependencies** | A03 snapshots/results, Fabric data-quality configuration, A04 detection rules, approved validator schema patterns. |
| **Inputs/outputs** | Consumes snapshot or recalculated output and rule configuration; produces PASS/PARTIAL/FAIL result, findings, evidence and rework route. |
| **Technology** | Fabric data-quality rules, SQL/notebooks and governed validation APIs. |
| **Build approach** | Implement completeness, referential, validity, temporal, reconciliation and cross-source rules. Separate blocking errors from warnings. At W17 compare expected and actual results and rerun anomaly checks. |
| **Error handling** | Fail closed when mandatory rule configuration or required data is absent; isolate rule execution defects and do not convert them to PASS. |
| **Controls** | CP01 and CP07. Evidence includes rule ID/version, actual/expected, severity, snapshot hash, override, before/after and no-new-anomaly result. |
| **Unit tests** | All pass, warnings only, mandatory-field failure, referential/temporal/reconciliation failure, correct correction, mismatch, new anomaly, override and unavailable rules. |
| **Technical-review focus** | Blocking/warning semantics, validator adaptation fit, tolerance approval, override governance and outcome reconciliation. |

## 4.8 A08 – Payroll Governance & Audit Agent

| **Overview** | Control component supporting W18–W20 evidence, governance logging and closure attestation. |
| --- | --- |
| **Dependencies** | Events from A01–A09, immutable store, AgentOps telemetry, lineage services and A02 closure contract. |
| **Inputs/outputs** | Consumes events, decisions, versions, receipts and validations; produces manifest, immutable audit pack, governance log, lineage and CP10 attestation. |
| **Technology** | Immutable evidence storage, AgentOps/event services and Fabric lineage metadata. |
| **Build approach** | Validate standard events, hash inputs/outputs, assemble chronological evidence, separate business evidence from operational telemetry, and attest completeness without performing authoritative case closure. |
| **Data handling** | Append-only records, role-scoped access, approved retention/legal hold, data minimisation and tamper-evident hashes. |
| **Error handling** | Reject malformed events; deduplicate by event ID; buffer during store outage; mark incomplete categories and block closure attestation. |
| **Controls** | CP08, CP09 and CP10 attestation. Evidence includes manifest, hashes, actors, versions, retention tags, open actions and completeness status. |
| **Unit tests** | Persist event, complete/incomplete pack, malformed/duplicate event, immutable update rejection, store outage, retention metadata and closure attestation. |
| **Technical-review focus** | Evidence versus telemetry separation, retention approval, immutability, completeness logic and A08/A02 closure split. |

## 4.9 A09 – Human Approval Control Agent

| **Overview** | Control component supporting W13–W15 authority, approval, SoD, commit authorisation and period sign-off. |
| --- | --- |
| **Dependencies** | A01 decision, A02 state, Entra identity, approved authority matrix, payroll integration and A08 evidence. |
| **Inputs/outputs** | Consumes recommendation, decision, correction hashes, identity and authority; produces ApprovalDecision, SoD result, authorisation token, rejection/escalation and sign-off evidence. |
| **Technology** | Dataverse approvals, Power Automate and Entra-based identity/authority checks. |
| **Build approach** | Validate identity, authority, preparer/approver separation, delegation scope/expiry, dual approval and correction integrity. Issue signed commit authorisation only after all controls pass. |
| **Error handling** | Fail safe when identity or authority matrix is unavailable; reject SoD or integrity failure; escalate insufficient authority; prevent sign-off with open cases. |
| **Controls** | CP05 and CP06. Evidence includes authority snapshot, SoD identities, delegation, approvals, correction hash, authorisation token and sign-off checklist. |
| **Unit tests** | Within authority, insufficient authority, SoD conflict, valid/expired delegation, dual approval, modified correction, missing approval, identity outage and sign-off with open cases. |
| **Technical-review focus** | Fail-safe behaviour, delegated authority, token integrity, no commit bypass and period sign-off accountability. |

# 6. Implemented Controls Documentation

| **ID** | **Owner** | **Type** | **Operation and fail-safe response** | **Required evidence** |
| --- | --- | --- | --- | --- |
| CP01 Input completeness | A07 | Preventive/Detective | Block analysis when mandatory fields or sources are absent. | Snapshot, DQ result, missing items and rule version |
| CP02 Approved anomaly rules | A04 | Preventive/Detective | Execute only effective, approved deterministic rules. | Rule/version, matches, execution trace |
| CP03 Risk and severity | A05 | Detective | Apply approved factors, weights and bands; expose factor results. | Factors, weights, band and config version |
| CP04 Evidence sufficiency | A06 | Preventive | Withhold recommendation if required evidence is absent or stale. | Evidence checklist, citations and alternatives |
| CP05 Human approval | A09 | Preventive | Block consequential change without valid approval. | Decision, authority, rationale, identity and timestamp |
| CP06 Segregation of duties | A09 | Preventive | Reject conflicting preparer, approver or deployer identities. | Identity snapshot, conflict rule and result |
| CP07 Post-correction validation | A07 | Detective/Corrective | Compare expected/actual, rerun rules and return failed cases to rework. | Before/after, receipt, validation and rework event |
| CP08 Audit completeness | A08 | Preventive/Detective | Block closure attestation if evidence categories are incomplete. | Manifest, hashes, missing category list |
| CP09 Governance logging | A08 | Detective | Record material actions, decisions, versions and overrides immutably. | Append-only event record |
| CP10 Case closure | A08 attests; A02 executes | Preventive | No close transition with failed controls, missing evidence or open actions. | Attestation, checklist, final state event |

# 7. Internal Orchestration Design

| **Phase** | **Steps and route** | **State/output** | **Control** |
| --- | --- | --- | --- |
| Ingest and validate | W01 A02→A03; W02 A03→A07 | Trusted snapshot or controlled hold | CP01 |
| Detect | W03 A07→A04; lifecycle branch where applicable | Anomaly register or no-anomaly evidence | CP02 |
| Analyse | W04–W08 A04→A05 | Risk, classification, explanation, root cause and source | CP03 |
| Options and recommend | W09 A05→A04; W10–W11 A05/A04→A06 | Options, impact and decision-ready recommendation | CP04 |
| Human decision | W12 A06→A02; W13–W14 A02→A01/A09 | Approve, reject or escalate | CP05/CP06 |
| Commit and recalculate | W15 A09→A02→A03; W16 A03 | Receipt and recalculated result | CP05/CP06 |
| Validate | W17 A03→A07 | PASS or controlled rework | CP07 |
| Evidence and log | W18–W19 A07→A08 | Manifest and governance log | CP08/CP09 |
| Close | W20 A08 attestation→A02 transition | Closed case or open exception | CP10 |

**Trigger and response mechanisms.** Payroll calendar or authorised manual trigger creates a case. Each handover requires ACK, NACK or TIMEOUT. Retries are bounded and deterministic; duplicate prevention uses idempotency keys. Rejected approvals return to review, failed validation returns to correction options, missing evidence returns to the producing step, and unresolved external lifecycle cases remain held with a manual route.

# 8. Handover & Integration Specification

| **Handover** | **Payload** | **Integration pattern** | **Failure/re-entry** |
| --- | --- | --- | --- |
| A03→A07 | Snapshot reference, payroll\_run\_id, worker keys, source/hash and completeness | Governed Fabric reference/API | Hold on blocking data failure; re-enter W01/W02 |
| A07→A04 | Validated dataset, DQ results and control state | Versioned contract | NACK on failed schema/control; return W02 |
| A04→A05 | Anomaly, rule version, matched evidence | API/event with correlation ID | Dead-letter on invalid payload; reprocess after fix |
| A04→Lifecycle | Case, worker, lifecycle event, anomaly, evidence and requested response | External adapter with ACK/NACK/timeout | Hold, manual route and controlled re-entry |
| A05→A06 | Risk, classification, explanation, root cause, source and lineage | Governed API | Return INSUFFICIENT\_EVIDENCE; no bypass |
| A06→A02→A01/A09 | Recommendation, impacts, evidence snapshot and requested decision | Dataverse/Power Automate | Hold pending valid human decision |
| A09→A02→A03 | ApprovalDecision, SoD result, correction hash and authorisation token | Controlled commit workflow | Reject mismatch; re-enter W14 |
| A03→A07 after commit | Receipt, before/after and recalculated output | Payroll API plus read-back | Query status before retry; hold unknown outcome |
| A07→A08 | Validation, control evidence and rework status | Immutable event contract | Reject malformed event; preserve operational failure |
| A08→A02 closure | Manifest, open actions and closure attestation | Versioned closure contract | No close if attestation fails or is absent |

# 9. Unit Testing, Evidence and Defect Management

Automate deterministic, contract, control and security tests wherever possible. Every result must identify the exact build version, scenario, test data, expected and actual result, evidence reference, defect and re-test. Failed evidence must not be deleted or overwritten.

| **ID** | **Scope** | **Scenario** | **Expected outcome** | **Status/evidence** |
| --- | --- | --- | --- | --- |
| UT-01 | A03/W01 | Complete authorised snapshot | Dataset created with source/version/hash; state advances | Not executed / attach run |
| UT-02 | CP01/W02 | Mandatory worker or pay item missing | Analysis blocked; gap evidence and steward route created | Not executed / attach run |
| UT-03 | A04/W03 | Each of seven anomaly classes | Correct anomaly, records, evidence and rule version | Not executed / attach run |
| UT-04 | A04/Lifecycle | ACK, NACK, timeout and re-entry | Controlled status and safe route; no silent success | Not executed / attach run |
| UT-05 | A05/W04 | Risk factor boundary | Expected band with factor/config version | Not executed / attach run |
| UT-06 | A05/P-01 | Complete calculation trace | All material values cited; no unsupported assertion | Not executed / attach run |
| UT-07 | A05/P-01 | Missing policy evidence | INSUFFICIENT\_EVIDENCE and missing-item list | Not executed / attach run |
| UT-08 | A06/W10–W11 | Two valid options | Impact comparison and advisory recommendation | Not executed / attach run |
| UT-09 | A09/CP05 | Pay-impacting correction without approval | Commit blocked; approval case retained | Not executed / attach run |
| UT-10 | A09/CP06 | Preparer approves own correction | Decision rejected; SoD conflict logged | Not executed / attach run |
| UT-11 | A02/W15 | Duplicate commit/idempotency key | Single write-back; duplicate acknowledged | Not executed / attach run |
| UT-12 | A03/W16 | Timeout after submission | No blind retry; status queried; exception routed | Not executed / attach run |
| UT-13 | A07/W17 | Actual differs from expected | Validation fails; case returns to rework | Not executed / attach run |
| UT-14 | A08/CP08 | Manifest missing approval snapshot | Attestation blocked; deficiency raised | Not executed / attach run |
| UT-15 | A02/A08/W20 | All controls pass and no actions remain | A08 attests; A02 emits one close event | Not executed / attach run |
| UT-16 | Security | Unauthorised worker detail request | Access denied and security event logged | Not executed / attach run |
| UT-17 | Resilience | AI service unavailable | Deterministic result retained; narrative fallback | Not executed / attach run |
| UT-18 | A09 | Delegation, expiry, dual approval and sign-off | Only valid authority combinations progress | Not executed / attach run |

## 8.1 Test Data Requirements

- Synthetic or approved masked payroll runs spanning normal, boundary, exception and failure conditions.

- Seven anomaly-class fixtures with approved expected outcomes and rule versions.

- Authority, delegation, expiry, dual-approval and SoD identities.

- External lifecycle ACK, NACK, timeout and malformed-response fixtures.

- Write-back success, failure, unknown-status and duplicate-receipt fixtures.

- Missing, stale, contradictory and complete evidence packages for AI evaluation.

- Unauthorised access, excessive-field and sensitive-log redaction scenarios.

## 8.2 Defect Tracking and Remediation

| **Field** | **Required record** |
| --- | --- |
| Defect ID and severity | Stable identifier; Critical, High, Medium or Low |
| Source | Component, test, control or review finding |
| Impact | Data, security, payroll outcome, evidence, integration or operability |
| Root cause | Code, configuration, data contract, design ambiguity or environment |
| Remediation | Fix, approved design change, compensating control or formal acceptance |
| Evidence | Original failure, commit/PR, reviewer approval and successful re-test |
| Closure | Closed by owner and independently verified; no Critical/High open at gate |

# 10. Technical Review Report

| **Review area** | **Pass criteria** | **Finding/resolution** | **Status** |
| --- | --- | --- | --- |
| Design alignment | Implementation traces to approved Stage 6B or approved ADR | To be completed | Pending |
| Component boundary | No duplicated or missing ownership | To be completed | Pending |
| Technology decision | Selection, rationale, alternatives and deviations recorded | To be completed | Pending |
| Data handling | Mappings, classification, minimisation, lineage and retention evidenced | To be completed | Pending |
| Security | Identity, least privilege, SoD, secrets, DLP and logging controls pass | To be completed | Pending |
| Controls | Applicable CP01–CP10 positive and negative paths tested | To be completed | Pending |
| Orchestration | State, retry, timeout, duplicate, exception and re-entry behaviour tested | To be completed | Pending |
| Handovers | Schema, version, ACK/NACK, correlation and error contract tested | To be completed | Pending |
| Unit tests | All mandatory tests pass; failures and re-tests retained | To be completed | Pending |
| Operations | Monitoring, runbook, rollback and support ownership current | To be completed | Pending |
| Documentation | As-built specification and change log match the reviewed artefact | To be completed | Pending |

| **Reviewer** | Pending |
| --- | --- |
| **Review date** | Pending |
| **Outcome** | Pending: Approve / Approve with conditions / Rework |
| **Mandatory findings closed** | Pending |
| **Reviewer recommendations** | Pending |
| **Approval evidence reference** | Pending |

# 11. Updated Implementation Documentation

| **Record** | **Required content** | **Status/reference** |
| --- | --- | --- |
| As-built design | Actual components, interfaces, state, controls, data and deployment | Pending update after implementation |
| Configuration register | Environment variables, connections, rules, thresholds and effective dates | Pending |
| Deployment and rollback | Package, dependencies, promotion steps, validation and rollback | Pending |
| Operational runbook | Monitoring, alerts, support ownership, replay, recovery and escalation | Pending |
| Design changes | Before/after, rationale, impact, approver and linked ADR | See decision register |
| Assumptions | Statement, owner, validation method, due date and consequence | See risk/assumption register |
| Lessons learned | Build, test, control, integration and review learnings | To be updated continuously |
| Release notes | Version, changes, known conditions, test/review references | Pending |

# 12. Technology Decision Register

| **ID** | **Decision** | **Rationale/deviation** | **Status** |
| --- | --- | --- | --- |
| TD-01 | Adopt Microsoft stack defined in Section 3 | Aligned to Stage 6B; no platform departure | Proposed |
| TD-02 | Dataverse is authoritative for case state | Prevents competing state authorities | Proposed |
| TD-03 | Azure durable integration for transactional/long-running external calls | Implementation refinement; supports reliable status and replay | Proposed |
| TD-04 | AI explains and recommends only | Arithmetic, controls, approval and commit remain deterministic/human | Required |
| TD-05 | A08 attests; A02 closes | Reconciles W20 workflow and CP10 state ownership | FDA approval required |
| TD-06 | Non-Silver source fields use governed Bronze/API contracts | Preserves source-specific attributes while mapping canonical keys | Data Architecture approval required |
| TD-07 | Reuse only validated schema/rule patterns | Unsuitable ABBA agents are not invoked; adapted assets require regression evidence | Fit validation required |

# 13. Controls & Evidence Required

| **Evidence area** | **Minimum evidence** | **Reference/status** |
| --- | --- | --- |
| Unit Test Execution | Run ID, build version, test data, expected/actual, logs, result and defect/re-test links | Pending |
| Code / Artifact Check-in | Repository, branch, commit hash, PR, reviewer, pipeline and package/version | Pending |
| Technical Review Completion | Checklist, findings, resolutions, independent reviewer and approval record | Pending |
| Change Log and Rationale | Change ID, source defect/constraint, decision, impact, approval and linked artefact | Pending |
| Data Handling Compliance | Classification, minimisation, lineage, access review, masking, retention and deletion/legal hold | Pending |
| Security and Control Implementation | RBAC, service identity, SoD, DLP, secrets, negative tests, audit events and control results | Pending |

# 14. Risks, Assumptions, Lessons and Change Log

| **ID** | **Item** | **Treatment** | **Owner/evidence** |
| --- | --- | --- | --- |
| R-01 | W20/CP10 accountability not formally approved | Use A08 attestation and A02 transition; hold gate until approved | Factory Design Authority |
| R-02 | External lifecycle endpoint unavailable | Versioned adapter, timeout/NACK, manual route and re-entry | H2R capability owner |
| R-03 | Physical and non-Silver mappings incomplete | Governed Bronze/API contracts; approve mappings before production | Data Architecture |
| R-04 | Write-back authority and rollback open | Disable production commit until contract, idempotency and status reconciliation approved | Payroll/IAM/Integration |
| R-05 | Thresholds and test expectations awaiting approval | Configuration placeholders only; no invented defaults | Payroll SME/Controller |
| R-06 | Evidence retention/legal hold not approved | Keep configurable; no final retention claim | Governance/Privacy |
| R-07 | Adapted validation/recalculation assets lack fit evidence | Contract, security and regression testing before adoption | Component owners |
| L-01 | Contract-first parallel build reduces component coupling | Freeze envelopes and keys before implementation | Solution Architect |
| L-02 | Evidence and operational telemetry serve different purposes | Maintain separate stores, schemas and access controls | Governance/Platform |
| CL-01 | Created comprehensive Stage 7A working baseline | Added components, controls, orchestration, tests, review and evidence registers | Working Draft v1.0 |

# 15. Implementation Guidance

Implementation should follow a contract-first, control-led delivery model. The nine capability agents may be built in parallel once shared schemas, keys, state transitions, security roles and evidence contracts are baselined. Every workstream remains responsible for its own build artefacts, automated unit tests, security configuration, evidence events and technical-review closure.

## 15.1 Roles and Responsibilities

| **Role** | **Core responsibilities** | **Primary outputs and approvals** |
| --- | --- | --- |
| Delivery Lead / Product Owner | Own scope, priorities, delivery plan, dependencies, risks and Stage 7A completion reporting. | Approved backlog, milestone status, issue escalation and gate recommendation. |
| Payroll Controller / Payroll SME | Approve payroll rules, thresholds, anomaly expectations, materiality, human decisions and period-sign-off semantics. | Business-rule approval, test expected results and business acceptance. |
| Solution Architect | Maintain end-to-end architecture, component boundaries, state authority, technology decisions and integration patterns. | Architecture decision records, approved contracts and technical coherence assessment. |
| Component Owners / Developers | Build A01–A09 components, configuration, prompts, rules, APIs, evidence events and automated tests. | Checked-in artefacts, unit-test results, implementation notes and defect fixes. |
| Data Architect / Fabric Engineer | Approve canonical and non-Silver mappings, identity keys, lineage, data-quality contracts and Fabric implementation. | Approved mappings, model version, pipeline assets and data-validation evidence. |
| Integration Engineer | Implement versioned handovers, adapters, ACK/NACK, timeout, idempotency, status read-back and rollback behaviour. | Integration contracts, interface tests, operational recovery and deployment evidence. |
| Security and IAM Lead | Define identities, managed connections, least privilege, RBAC, DLP, SoD, delegation and secret handling. | Security design approval, access review and negative-path security evidence. |
| Control, Risk and Governance Lead | Validate CP01–CP10 implementation, evidence completeness, retention, legal hold and audit requirements. | Control test approval, evidence-store decision and residual-risk disposition. |
| Test Lead / Quality Engineer | Maintain test data, automated suites, traceability, defect triage, regression and re-test evidence. | Test completion report, defect status and quality recommendation. |
| Technical Reviewer | Independently review each component for design, security, data, controls, operability and documentation. | Review checklist, findings, resolution verification and component approval. |
| DevOps / Platform Engineer | Manage repositories, branching, CI/CD, managed solutions, environment promotion, monitoring and rollback. | Pipeline evidence, release package, deployment record and operational telemetry. |
| Factory Design Authority | Approve material design decisions, W20/CP10 accountability, deviations, residual risks and progression to Stage 7B. | Formal gate decision and signed decision record. |

## 15.2 Phased Timeline and Key Milestones

The timeline below is a relative delivery sequence. Calendar dates should be assigned after resource availability, environment readiness and external-interface commitments are confirmed.

| **Phase** | **Indicative timing** | **Key activities** | **Milestone / exit condition** |
| --- | --- | --- | --- |
| 1. Mobilise and baseline | Week 1 | Confirm scope, ownership, environments, repositories, backlog, risks and Stage 6B conditions. | M1: Delivery plan and accountable owners approved. |
| 2. Contract and control freeze | Weeks 1–2 | Baseline shared envelope, schemas, canonical keys, A02 state model, CP01–CP10 evidence and security roles. | M2: Version 1 contracts and control acceptance criteria frozen. |
| 3. Parallel component build | Weeks 2–5 | Build A01–A09 in parallel; implement deterministic services, prompts, configuration, audit events and local mocks. | M3: All components checked in, deployable and locally demonstrable. |
| 4. Automated unit and contract testing | Weeks 3–6 | Execute component, boundary, failure, security, control and regression tests; remediate defects continuously. | M4: Mandatory unit and contract tests pass with no unresolved Critical defect. |
| 5. Technical review | Weeks 5–7 | Perform independent review of design alignment, security, data handling, controls, operability and documentation. | M5: Each component approved or all mandatory findings formally closed. |
| 6. Stage 7A consolidation | Week 7 | Update as-built documentation, evidence register, technology decisions, change log, runbook and release notes. | M6: Complete, traceable implementation package assembled. |
| 7. Authority gate | Week 8 | Present component approvals, test evidence, unresolved conditions and residual-risk decisions. | M7: Factory Design Authority approves progression to Stage 7B or returns defined actions. |

## 15.3 Success Metrics and Definition of Completion

| **Success area** | **Completion metric** | **Required evidence** |
| --- | --- | --- |
| Component build | 9 of 9 capability-agent packages are versioned, checked in, deployable and traceable to approved requirements. | Repository, commit, pull request, package version and deployment result. |
| Design traceability | Every implemented component, interface, rule and control maps to Stage 6B or an approved design decision. | Traceability matrix, decision record and change log. |
| Automated testing | 100% of mandatory unit, contract, control and security scenarios are executed; all pass or have an approved exception. | Test runs, expected/actual results, failed-run retention and exception approval. |
| Defect quality | No open Critical or High defect; Medium defects have owners, target dates and accepted impact. | Defect register, remediation commits and successful re-tests. |
| Control effectiveness | CP01–CP10 positive and negative paths operate as designed; no control can be bypassed through an alternate route. | Control test evidence, audit events and reviewer sign-off. |
| Orchestration reliability | W01–W20 supports happy path, rejection, rework, escalation, timeout, duplicate prevention and safe re-entry without orphaned cases. | State-transition logs, resilience tests and reconciliation report. |
| Integration readiness | All required handovers validate schema/version, correlation, ACK/NACK, error response and idempotency behaviour. | Contract-test results, adapter logs and failure/recovery evidence. |
| Data compliance | All data has approved source mapping, classification, lineage, access control and non-Silver treatment; sensitive values are absent from unauthorised logs. | Mapping approval, lineage record, access review and log inspection. |
| Security | Least privilege, managed identity, RBAC, DLP, SoD, delegation and secret-management tests pass. | Security configuration, access tests and security-review approval. |
| Evidence and audit | Every material execution produces complete, tamper-evident evidence with actor, version, time, hash and case reference. | Evidence manifest, immutable-store test and completeness result. |
| Technical review | 9 of 9 components have an independent completed review with all mandatory findings resolved. | Signed review checklists and resolution records. |
| Operational readiness | Monitoring, alerts, support ownership, replay, recovery, rollback and release notes are current and tested. | Runbook, monitoring evidence, rollback rehearsal and release package. |
| Stage 7A completion | All deliverables and approvals are attached, residual risks are accepted, and the authority records permission to progress. | Final evidence index and Factory Design Authority decision. |

**Completion rule:** Stage 7A is complete only when the evidence demonstrates that the nine components are built, controlled, tested, independently reviewed and operationally documented. A planned activity, draft artefact or unexecuted test does not count as completion.

# 16. Practitioner Guidance and Stage 7B Exit Gate

- Build A01–A09 in parallel where versioned contracts and shared keys are stable.

- Follow Stage 6B exactly unless a defect or constraint is evidenced; record every departure in the decision register.

- Use automated unit tests and pipeline gates for deterministic logic, contracts, security and controls.

- Preserve original failed test runs and link every fix to a defect, commit and re-test.

- Do not expose sensitive payroll data in notifications, prompts, operational logs or unauthorised reporting.

- Keep AI outputs grounded, advisory and clearly separated from deterministic calculations and human decisions.

- Complete an individual technical review for every component before integration.

| **Stage 7A exit criterion** | **Required disposition** |
| --- | --- |
| All A01–A09 artefacts checked in | Commit, PR, package and version references attached |
| CP01–CP10 evidenced | Positive and negative-path results attached; CP10 model approved |
| Orchestration and handovers proven | State, contract, timeout, duplicate, exception and re-entry tests pass |
| Unit testing complete | No unresolved Critical or High defect; failures and re-tests retained |
| Technical review complete | Independent reviewer records approval or formal conditions |
| Implementation documentation current | As-built, configuration, runbook, rollback and release notes match artefacts |
| Technology and departures approved | Decision register signed and residual risks accepted |
| **Gate outcome** | **Pending – do not proceed to Stage 7B until all evidence is attached and approved.** |

# Appendix A – Glossary, Related Documents and Change Log

## A.1 Glossary of Key Terms

| **Term** | **Definition** |
| --- | --- |
| Agent Factory | Structured delivery methodology used to decompose, classify, model, design, build, test and assure AI-enabled capability agents. |
| Capability Agent | A component aligned to a stable business or technical capability rather than a single workflow step. |
| A01–A09 | The nine Payroll Assurance capability agents covering Experience, Orchestration, Task, Insight and Control responsibilities. |
| W01–W20 | The twenty workflow steps spanning payroll-data collection through validation, analysis, approval, correction, evidence and closure. |
| CP01–CP10 | The ten control points covering data completeness, approved rules, risk, evidence sufficiency, approval, SoD, validation, audit, governance and closure. |
| Experience Agent | User-facing component that presents cases, evidence and permitted actions and captures human decisions. |
| Orchestration Agent | Component that coordinates workflow sequencing, state, routing, retries, escalation and handovers. |
| Task Agent | Component that performs defined operational work such as data collection, recalculation or anomaly processing. |
| Insight Agent | Component that analyses verified information and produces risk, explanation, diagnosis, impact or recommendations. |
| Control Agent | Component that enforces preventive, detective or corrective controls and records supporting evidence. |
| AgentOps | Operational and governance capability for agent execution monitoring, evidence capture, telemetry and audit support. |
| ABBA | Agent catalogue and reuse-assessment source used to identify existing assets or patterns that may be adapted. |
| Bronze / Silver / Gold | Fabric data layers for source-aligned ingestion, canonical trusted data and curated analytical or agent-consumption objects. |
| Dataverse | Authoritative store for governed case, workflow, approval and configuration data in this design. |
| Canonical Key | Consistent identifier, such as worker\_id, payroll\_run\_id or case\_id, used across data objects and handovers. |
| Handover Contract | Versioned schema defining payload, producer, consumer, correlation, acknowledgements, errors and safe re-entry behaviour. |
| Correlation ID | Identifier used to trace a request and its related events across agents, systems and workflow steps. |
| Idempotency Key | Identifier that prevents a repeated request from producing more than one consequential update. |
| ACK / NACK | Positive or negative acknowledgement confirming whether a handover was accepted or rejected. |
| SoD | Segregation of Duties; a control preventing conflicting roles, such as a preparer approving their own change. |
| Evidence Manifest | Structured index of the evidence required to prove case execution, controls, decisions, changes and outcomes. |
| Immutable Evidence Store | Append-only repository in which audit records cannot be overwritten or deleted through normal processing. |
| Grounded AI Output | AI-generated narrative restricted to supplied, cited evidence and deterministic calculations. |
| Technical Review | Independent assessment of implementation alignment, security, data handling, controls, testing, integration and operability. |
| Factory Design Authority | Governance body that approves material design decisions, residual risks and progression to the next delivery stage. |

## A.2 Related Documents

| **Document** | **Relationship to this Stage 7A package** | **Link / location** |
| --- | --- | --- |
| Payroll Assurance Agent – Stage 3 Decompose Deliverable | Defines the end-to-end business workflow, human intervention points, exceptions and W01–W20 baseline. | Uploaded project file; repository or SharePoint link to be confirmed. |
| Payroll Assurance Agent – Stage 4 Classify Capability Based | Defines the nine-agent inventory, classifications, ownership, orchestration, controls and handovers. | Uploaded project file; repository or SharePoint link to be confirmed. |
| Stages 5 and 5B – Model and Data Model Consolidation | Defines canonical data entities, keys, classifications, handover data, gaps and the consolidated data model. | Uploaded project file; repository or SharePoint link to be confirmed. |
| Payroll Assurance Agent – Stage 6A Updated Detailed Component Design | Provides component behaviour, inputs/outputs, controls, handovers, deterministic logic and test scenarios. | Uploaded project file; repository or SharePoint link to be confirmed. |
| Payroll Assurance Agent – Stage 6B Updated Consolidation and Build Readiness | Primary build baseline for component responsibilities, control coverage, readiness conditions and technology recommendations. | Uploaded project file; repository or SharePoint link to be confirmed. |
| Payroll Assurance Agent – Stage 6 Assess Reuse | Contains the detailed ABBA reuse and adaptation assessment referenced by the Stage 6B baseline. | Open the Stage 6 Assess Reuse document |
| A01–A09 Detailed Design Specifications | Provide detailed build specifications for the Workspace, Orchestrator, Data Management, Exception Processing, Analysis, Decision Intelligence, Quality Control, Governance & Audit and Human Approval components. | Uploaded Markdown project files; repository or SharePoint links to be confirmed. |
| Enterprise Model and SQL Artefacts | Provide authoritative entity definitions, Silver/Gold structures, foreign keys and model validation assets. | config/enterprise\_model.yml; sql/10\_silver/070\_workforce.sql; sql/90\_post\_deploy/001\_foreign\_keys.sql. |
| Stage 5 Data Trace and Gap Artefacts | Provide workflow-level data traceability, classification, source ownership and gap resolution. | docs/stage-5-data-flow-map.md; docs/stage-5-data-classification.csv; docs/stage-5-data-gap-log.csv; docs/complete-agent-data-gap-log.csv. |
| Decision and Change Records | Record data-model approval, technology decisions, implementation changes and rationale. | docs/decision-log.md; CHANGELOG.md; Stage 7A Technology Decision Register. |

## A.3 Change Log

| **Version number** | **Date** | **Author** | **Change description** |
| --- | --- | --- | --- |
| 0.1 | 2 September 2026 | Ibegbunam, Ezekiel | Created the initial Stage 7A working-document baseline. |
| 0.2 | 2 September 2026 | Ibegbunam, Ezekiel | Added the nine-agent technical details, system architecture, dependencies, data flows and integration constraints. |
| 0.3 | 2 September 2026 | Ibegbunam, Ezekiel | Added implementation guidance covering roles, phased milestones and measurable completion criteria. |
| 0.4 | 2 September 2026 | Ibegbunam, Ezekiel | Added Appendix A with glossary, related-document register and formal change log. |
| 1.0 | Pending | Pending | First approved Stage 7A baseline following completed technical review and Factory Design Authority acceptance. |

