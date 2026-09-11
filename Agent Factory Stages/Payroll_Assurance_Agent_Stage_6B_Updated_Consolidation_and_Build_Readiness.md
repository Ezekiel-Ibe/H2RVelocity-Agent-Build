**KPMG**

**Payroll Assurance Agent**

**STAGE 6B - UPDATED CONSOLIDATION AND BUILD READINESS**

*End-to-end assurance of the Stage 6A design against updated Stage 4 v2*

| **Document control** | **Details** |
| --- | --- |
| Version | Draft v2.0 |
| Status | Conditional readiness assessment for Factory Design Authority review |
| Updated reference | Payroll\_Assurance\_Agent\_Stage\_4\_Classify\_Capability\_Based (2).docx |
| Owner persona | Payroll Controller |
| Business capability | Continuous Payroll Assurance |
| Classification | KPMG Confidential |

Primary update source: uploaded Stage 4 v2 capability-based model, including updated workflow ownership, handovers, control points and ABBA reuse assessment.

# Executive Summary

This Stage 6B package consolidates the updated Stage 6A component designs using the uploaded Stage 4 v2 as the authoritative classification and reuse reference. The solution remains a nine-agent capability model. The revised assessment is conditional because the Stage 4 v2 introduces an unresolved W20 ownership inconsistency, an external lifecycle-agent handover requiring a return contract, and ABBA adaptation decisions that require technical fit validation before build.

| **Gate recommendation: **CONDITIONALLY READY FOR FACTORY DESIGN AUTHORITY REVIEW. Do not mark build-ready until critical issues B-01 to B-06 are closed or formally accepted with accountable owners. |
| --- |

# 1. Consolidated Updated Solution

| **ID** | **Component** | **Class** | **Consolidated responsibility** |
| --- | --- | --- | --- |
| A01 | Payroll Assurance Workspace Agent | Experience | Review, evidence access and decision capture |
| A02 | Payroll Assurance Orchestrator | Orchestration | Routing, escalation, commit coordination and state |
| A03 | Payroll Data Management Agent | Task | Data collection and recalculation |
| A04 | Payroll Exception Processing Agent | Task | Anomaly detection and correction options |
| A05 | Payroll Analysis Agent | Insight | Risk, classification, explanation, diagnosis and source location |
| A06 | Payroll Decision Intelligence Agent | Insight | Impact and recommendation |
| A07 | Payroll Quality Control Agent | Control | Input and post-correction validation |
| A08 | Payroll Governance & Audit Agent (AgentOps) | Control | Audit evidence, governance logs and case closure |
| A09 | Human Approval Control Agent | Control | Human approval, SoD and period sign-off |

# 2. End-to-End Orchestration Assurance

| **Phase** | **Steps** | **Flow** | **Adjusted Flow (To be reviewed)** | **Output** | **Control** |
| --- | --- | --- | --- | --- | --- |
| Ingest/validate | W01-W02 | A03 -> A07 | A03 -> A07 | Trusted dataset and DQ(Data Quality) result | CP01 |
| Detect | W03 | A04, with lifecycle handover where applicable | A07 -> A04 -> Lifecycle and Onboarding Agent (Handover where applicable) | Anomaly register | CP02 |
| Analyse | W04-W08 | A05 | A04 -> A05 | Risk, classification, explanation, root cause and source | CP03 |
| Options/recommend | W09-W11 | A04 -> A06 | A05 -> A06 | Decision-ready recommendation | CP04 |
| Human decision | W12-W14 | A02 -> A01/A09 | A06 -> A02 - > A09 | Approve, reject or escalate | CP05/CP06 |
| Commit/recalculate | W15-W16 | A02/A09 -> A03 | A09 - > A03 | Receipt and recalculated payroll | CP05/CP06 |
| Validate | W17 | A07 | A03 - > A07 | ValidationResult or rework | CP07 |
| Evidence/log | W18-W19 | A08 | A07 -> A08 | Audit pack and governance log | CP08/CP09 |
| Close | W20 | A08 workflow role; A02 CP10 role unresolved | A08 -> Close case /<br>A08 -> A02 (Open exception) | Closed case or open exception | CP10 |

# 3. Data Continuity and Stage 5B Validation (Silver Entity)

| **Transition** | **Required objects** | **Assessment** | **Condition** |
| --- | --- | --- | --- |
| A03 -> A07 | Worker, PayrollRun, PayItem, TimeRecord, LifecycleEvent, snapshot | Aligned | Physical mappings and identity keys remain open. |
| A07 -> A04 | Validated dataset, DQ results and control state | Aligned | Approve blocking/warning rules. |
| A04 -> A05 | PayrollAnomaly, rule and evidence | Aligned | Approve seven-anomaly rule catalogue. |
| A04 -> Lifecycle | Lifecycle anomaly, worker/event evidence | New in v2 | Define response object and return route. |
| A05 -> A06 | PayrollRisk, RootCauseAssessment, explanation and lineage | Aligned | Approve weights, bands and confidence. |
| A06 -> A01/A09 | Recommendation, impact, evidence snapshot | Aligned | Approve authority and materiality. |
| A09 -> A02/A03 | ApprovalDecision, SoD and sign-off | Aligned | Define expiry, delegation and dual approval. |
| A03 -> A07 after commit | Receipt, before/after and recalculated output | Aligned | Approve write-back contract. |
| A07 -> A08 | Validation and control evidence | Aligned | Approve retention and immutable store. |
| A08/A02 -> closure | Manifest, log, open-action and closure state | Conditional | Resolve W20 accountability. |

Reference to the detailed data model check this: \[provide a link\]

# 4. Updated Control Coverage

| **ID** | **Control** | **Owner** | **Coverage** | **Stage 6B result** |
| --- | --- | --- | --- | --- |
| CP01 | Input completeness | A07 | W02 | Green |
| CP02 | Approved anomaly rule | A04 | W03 | Green |
| CP03 | Risk and severity | A05 | W04-W05 | Green |
| CP04 | Evidence sufficiency | A06 | W10-W11 | Green |
| CP05 | Mandatory human approval | A09 | W13-W15 | Green |
| CP06 | Segregation of duties | A09 | W14-W15 | Green |
| CP07 | Post-correction validation | A07 | W17 | Green |
| CP08 | Audit evidence completeness | A08 | W18 | Green |
| CP09 | Governance logging | A08 | W19 | Green |
| CP10 | Case closure | A02 in control table; A08 in workflow mapping | W20 | Red - ownership conflict |

# 5. Updated ABBA Consolidation

| **Area** | **Disposition** | **Consolidation result** |
| --- | --- | --- |
| Validation capabilities | Adapt VA-1246, VA-1172, VA-1279 | Conditional pending combined Quality Control fit. |
| Anomaly detection candidates | VA-1149/VA-1266 not suitable | Exclude from build baseline. |
| Explanation candidates | VA-1267/VA-1253 not suitable | Exclude unless new evidence proves scope fit. |
| Recalculation candidates | Adapt VA-1145, VA-1248, VA-11343 | Conditional pending Fabric/source and format fit. |
| Governance monitor | VA-1304 not suitable | Do not treat monitoring as logging. |
| Closure candidates | VA-1249/VA-1251 not suitable | Build assurance-specific closure pattern. |
| Remaining capabilities | New design | Proceed under Stage 6A specifications. |

Reference is to be made to the ABBA Reuse Assessment detailed document: \[[Payroll\_Assurance\_Agent\_Stage\_6\_Assess\_Reuse.docx\]](https://kpmgoneuk.sharepoint.com/:w:/r/sites/GB-KPMGxMicrosoftAgenticAI-KPMGONLY/_layouts/15/Doc.aspx?sourcedoc=%7B74FD1F46-F2DE-4562-B698-681F46DAE3B9%7D&file=Payroll_Assurance_Agent_Stage_6_Assess_Reuse.docx&action=default&mobileredirect=true)

# 6. Unit-Test Coverage Assessment

| **Coverage area** | **Assessment** | **Required addition** |
| --- | --- | --- |
| A01-A09 component behaviour | Green | Maintain normal, boundary and failure tests. |
| W01-W20 orchestration | Amber | Add W20 ownership resolution test. |
| Lifecycle cross-agent handover | Amber | Add response, timeout, rejection and re-entry tests. |
| Seven anomalies | Amber | Approve expected data and results for each class. |
| ABBA adapted assets | Amber | Run contract, security, evidence and regression tests. |
| CP01-CP09 | Green | Positive and negative control cases present. |
| CP10 | Red | Cannot finalise until owner/executor model is approved. |
| Human approval and sign-off | Amber | Add delegation, expiry, dual approval and period sign-off tests. |
| Data/security/audit | Amber | Physical contracts, retention and evidence store remain open. |

# 6b. Unit Test Scenarios and Expected Results

| **ID** | **Scope** | **Scenario** | **Expected result** | **Status** |
| --- | --- | --- | --- | --- |
| UT-01 | A03/W01 | Complete authorised payroll snapshot | Dataset created with source/version/hash; state advances |  |
| UT-02 | CP01/W02 | Mandatory worker or pay item missing | Analysis blocked; missing-field evidence and steward route created |  |
| UT-03 | A04/W03 | Known duplicate pay item matches approved rule | Anomaly created with matched records and rule version |  |
| UT-04 | A05/W04 | Approved risk factors at threshold boundary | Expected band returned with each factor and config version |  |
| UT-05 | A05/P-01 | Explanation request with complete calculation trace | All values cited; no unsupported assertion |  |
| UT-06 | A05/P-01 | Explanation request with missing policy evidence | INSUFFICIENT\_EVIDENCE and missing item list |  |
| UT-07 | A06/W10-11 | Two valid correction options | Impact comparison and advisory recommendation returned |  |
| UT-08 | A09/CP05 | Pay-impacting correction without approval | Commit blocked; approval case created |  |
| UT-09 | A09/CP06 | Preparer attempts to approve own correction | Decision rejected; SoD conflict logged |  |
| UT-10 | A02/W15 | Duplicate commit message with same idempotency key | Single write-back; duplicate safely acknowledged |  |
| UT-11 | A03/W16 | Integration times out after submission | No blind retry unless status is known/idempotent; exception routed |  |
| UT-12 | A07/W17 | Actual net pay differs from expected after correction | Validation fails; case returns to rework |  |
| UT-13 | A08/CP08 | Evidence manifest missing approval snapshot | Closure blocked; evidence deficiency raised |  |
| UT-14 | A02/W20 | All controls pass and no actions remain | Case closed with final evidence reference |  |
| UT-15 | Security | Unauthorised user requests worker detail | Access denied and security event logged |  |
| UT-16 | Resilience | AI service unavailable | Deterministic result retained; narrative fallback shown |  |

# 7. Readiness Assessment

| **Criterion** | **Status** | **Basis** | **Required disposition** |
| --- | --- | --- | --- |
| Updated component designs | In progress | Nine component contracts updated. | Approve Stage 6A consolidation. |
| Workflow continuity | In progress | Primary flow complete; lifecycle return route open. | Approve return/re-entry. |
| W20 closure | Conflict already identified | A08 versus A02 ownership conflict. | Approve single RACI and execution pattern. |
| Data continuity | Completed and In review | Logical mappings aligned to Stage 5B. | Close/accept physical mapping conditions. |
| Control coverage | Completed and In review | CP01-CP09 clear; CP10 conflict. | Resolve CP10. |
| ABBA reuse | 3 Strong agents Identified for reuse and 1 agent (Recalculate Payroll) to be added  | Asset decisions known; adaptations not validated. | Complete fit-gap and regression tests. |
| Human intervention | Completed | Approval/sign-off present; authority details open. | Approve authority model. |
| Unit tests | Test scenarios identified subject to confirmation | Expanded baseline defined. | Approve expected results and test data. |
| Security/evidence | AgentOps Audit to take responsibility | Principles defined; implementation decisions open. | Approve evidence, retention and access pattern. |

# 8. Critical Issues and Actions Log

| **ID** | **Priority** | **Issue** | **Required action** | **Owner** |
| --- | --- | --- | --- | --- |
| B-01 | Critical | Resolve W20 ownership | Approve A08 evidence/attestation role and A02 state-transition role, or choose another single accountable model. | Factory Design Authority |
| B-02 | Critical | Lifecycle handover contract | Define Onboarding & Lifecycle response, SLA, exception and re-entry. | H2R capability owners |
| B-03 | Critical | ABBA adaptation fit | Validate VA-1246/1172/1279 and VA-1145/1248/11343 against data, controls and Fabric. | Component owners |
| B-04 | Critical | Seven-anomaly rules | Approve precise deterministic rules, thresholds, evidence and expected results. | Payroll SME/Controller |
| B-05 | Critical | Write-back and sign-off | Approve authority, SoD, period sign-off, idempotency and rollback. | Payroll/IAM/Integration |
| B-06 | Critical | Stage 5B entry conditions | Resolve or formally accept DA-01 to DA-08 treatment. | Design Authority |
| B-07 | High | Evidence/retention | Approve immutable store, legal hold, access and retention. | Governance/Privacy |
| B-08 | High | Physical mappings | Approve source-to-canonical mappings and identity matching. | Data Architecture |
| B-09 | Medium | UX terminology | Align “approve/reject/escalate”, period sign-off and case closure language. | Experience owner |

# 9. Recommended Implementation Technology

The following remains an advisory Stage 6B recommendation. Final selection belongs to Build and must reflect approved Stage 5B architecture and the adapted-asset fit assessment.

| **Layer** | **Recommended pattern** | **Condition** |
| --- | --- | --- |
| Experience | Copilot Studio plus governed case workspace | Role/action model and evidence UX approved. |
| Orchestration/state | Power Automate/Dataverse or Azure integration services | W20 state ownership and lifecycle return route approved. |
| AI/evaluation | Azure AI Foundry | Grounded prompts and evaluation; no payroll arithmetic authority. |
| Data | Microsoft Fabric | DA-03, source mappings, security and environment decisions approved. |
| Deterministic logic | Fabric SQL/notebooks or governed APIs/Functions | Versioned rules and test evidence. |
| Identity | Entra ID, managed identity, RBAC/DLP | SoD, delegation and sign-off authority approved. |
| Reporting | Power BI over certified models | Data minimisation and access approved. |
| Audit/monitoring | Immutable evidence store plus operational telemetry | Business evidence separated from technical monitoring. |
| Lifecycle | Source control, managed solutions and CI/CD | ABBA adaptations versioned and regression-tested. |

# 10. Factory Design Authority Decision Record

| **Decision item** | **Selection / comment** |
| --- | --- |
| Decision | ☐ Build-ready  ☐ Conditionally approved  ☐ Return to Stage 6A |
| W20 accountability |  |
| Lifecycle handover approval |  |
| ABBA adaptation approval |  |
| Approved unit-test baseline |  |
| Stage 5B conditions |  |
| Residual risks accepted |  |
| Authority owner / date |  |

# Appendix A. Change Traceability

| **Updated Stage 4 v2 item** | **Stage 6A update** | **Stage 6B check** |
| --- | --- | --- |
| Nine capability agents | Agent contracts retained and refreshed. | Component completeness. |
| A08 AgentOps W18-W20 | A08 behaviour expanded through closure preparation. | W20 ownership conflict flagged. |
| Onboarding & Lifecycle handover | Cross-capability contract added. | Return/re-entry remains conditional. |
| ABBA detailed assessment | Reuse table replaced with evidence-based dispositions. | Adapted assets require fit validation. |
| A09 period sign-off | Human-control behaviour and tests expanded. | Authority/sign-off condition. |
| Seven anomaly classes | Deterministic catalogue and tests expanded. | Expected results require SME approval. |

