**	**

**HR-RTP-001: Payroll Assurance Agent**

Stage 3 - Decompose Deliverable

Prepared for Stage 3 Review and Sign-off

Document version: Draft

Date: 14 August 2026

# Document Control

| **Control Item** | **Details** |
| --- | --- |
| Document title | Payroll Assurance Agent - Stage 3 Decompose Deliverable |
| Version | Draft v1.0 |
| Status | Draft for review and sign-off |
| Prepared by | H2R  |
| Prepared for | Stage 3 review and sign-off stakeholders |
| Date | 14 August 2026 |
| Approval required from | Payroll Assurance Agent SME / Stage 3 approver |
| Review purpose | Confirm that the Stage 3 decomposition accurately reflects the Payroll Assurance capability, workflow, decision points, handovers, exceptions and human intervention model. |

# Table of Contents

**1. Executive Summary**

2. Stage 3 Activities and Outputs

3. Step 1 - Review and Understand the Capability

4. Step 2 - Create the Overall AI Framework

5. Step 3 - Map the End-to-End Workflow

6. Step 4 - Decompose into Workflow Steps

7. Step 5 - Define Handovers and Interactions

8. Decisions, Exceptions and Human Intervention Points

9. Step 6 and Step 7 - SME Validation and Confirmation

# Executive Summary

Stage 3 translates the Payroll Assurance agent capability into an overall AI Framework and an end-to-end workflow that can be analysed, classified and designed in the subsequent factory stages.

The Payroll Assurance Agent supports continuous payroll assurance by detecting anomalies, explaining payroll calculations, diagnosing root causes, assessing impact, recommending corrective actions and producing audit evidence.

The agent operates within an L3 Augmented+ autonomy model: it can detect, explain and recommend, but payroll corrections and payroll sign-off remain human-approved by the Payroll Controller.

The core workflow follows: Detect -> Explain -> Diagnose -> Options -> Impact Analysis -> Recommend -> Human Approval -> Commit -> Validate -> Close.

# Stage 3 Activities and Outputs

| **Stage 3 Step** | **Activity** | **Payroll Assurance Output** |
| --- | --- | --- |
| 1 | Review and understand the capability | Confirmed capability scope, intent, boundaries, success measures, constraints and open questions. |
| 2 | Create overall AI Framework | Business-agent framework covering purpose, users, inputs, outputs, systems, dependencies, controls and human guardrails. |
| 3 | Map the end-to-end workflow | High-level process map from payroll review trigger through detection, recommendation, approval, validation and closure. |
| 4 | Decompose into workflow steps | Design-ready workflow catalogue with discrete steps, objectives, performers, inputs, outputs and controls. |
| 5 | Define handovers and interactions | Data and process handover model between systems, agent components, Payroll Controller and governance. |
| 6 | Validate with SME | SME walkthrough checklist covering workflow accuracy, decisions, handovers and exceptions. |
| 7 | Obtain SME confirmation | Confirmation that workflow reflects the business process and decomposition is complete. |

## Inputs from Stage 2

Defined business capability

Confirmed outcome

Scope, users and success measures

Constraints

## Outputs of Stage 3

Overall AI Framework for the business agent

End-to-end high-level process map

Decomposed list of workflow steps

Decisions and exceptions catalogue

Human intervention points

SME confirmation that the workflow reflects the business process

# Step 1 - Review and Understand the Capability

## Capability Summary

| **Area** | **Definition** |
| --- | --- |
| Business capability | Continuous Payroll Assurance |
| Business outcome | Right-first-time, compliant payroll with reduced leakage, reduced audit effort and full correction evidence. |
| Capability owner | Payroll Controller  |
| Agent name | Payroll Assurance Agent |
| Owner persona | Payroll Controller |
| Autonomy level | L3 Augmented+; auto-detects and explains within policy, while corrections remain human-approved. |
| Primary purpose | Provide continuous assurance that employee lifecycle changes are correctly reflected in pay before employee-facing errors or compliance breaches occur. |
| Trigger | A payroll run reaches pre-sign-off, or an assurance control is manually initiated for the current payroll period |

## Capability Boundary

In scope: anomaly detection, payroll risk scoring, explanation, diagnosis, impact assessment, recommendation, approval support, validation and audit evidence.

Out of scope for agent autonomy: independent approval of corrections, independent payroll sign-off and unauthorised policy changes.

Mandatory guardrail: every pay correction and payroll sign-off requires Payroll Controller approval.

## Success Measures

Anomaly detection precision and recall against a labelled payroll error set.

False positive rate below the agreed target threshold.

Percentage of corrections approved without amendment.

Audit evidence completeness of 100%.

Zero pay auto-corrected outside tolerance during back testing.

# Step 2 - Create the Overall AI Framework

| **Framework Element** | **Payroll Assurance Definition** |
| --- | --- |
| Purpose | Prevent payroll errors before sign-off by continuously detecting, explaining and assessing payroll anomalies. |
| Business owner | Payroll Controller. |
| Users | Payroll Controller, Payroll Manager, Payroll Administrator, HR Operations, Finance, Audit and Compliance stakeholders. |
| Trigger | Payroll run pre-sign-off, with potential extension to daily or continuous monitoring based on release scope. |
| Inputs | Current and prior pay records, worker master and employment status, time and absence, lifecycle events, pay policy and statutory tables. |
| Outputs | Anomaly register, risk score, explanation, diagnosis, correction options, impact assessment, recommendation, approval action, validation result and audit evidence pack. |
| Value delivered | Earlier error detection, consistent controls, clearer explanations, reduced leakage and complete audit evidence.  |
| Systems and dependencies | HCM, Payroll, Time, Benefits, Identity and General Ledger. |
| Human involvement | Payroll Controller approves all corrections and signs off the period; data owners resolve source-system issues.  |
| Governance controls | Segregation of duties, human approval, audit logging, evidence retention and AI Governance action logs. |
| Compliance considerations | HMRC PAYE / RTI, Pensions Act 2008, National Minimum Wage Act, UK GDPR / DPA 2018, ISO 30414 and SOX-style payroll controls. |
| Human guardrails | Agent can detect, explain and recommend; Payroll Controller approves corrections and signs off payroll. |
| Known constraints  | Client-specific thresholds and tolerances; data quality; systems-of-record integration; no model-generated calculations; no autonomous approval.  |

# Step 3 - Map the End-to-End Workflow

## Purpose

Identify the trigger that starts the workflow.

Map the high-level sequence of payroll assurance business activities.

Identify decisions, exceptions and handovers.

Identify human intervention points before any correction is committed.

- 

## High-Level Process Map

**Figure 1. End-to-end Payroll Assurance workflow process map.**

![image1](media/Payroll_Assurance_Agent_Stage_3_Decompose%20(2)/image1.png)

# Step 4 - Decompose into Workflow Steps

## Purpose

Break the workflow into discrete, design-ready steps.

Keep the steps at the correct level of granularity for downstream classification and solution design.

Ensure the decomposed steps collectively deliver the intended payroll assurance outcome.

Identify inputs, outputs, decisions, exceptions, controls and handovers for each step.

- 

- 

- 

- 

## Detailed Workflow Diagram

![image2](media/Payroll_Assurance_Agent_Stage_3_Decompose%20(2)/image2.png)

## Workflow Decomposition Catalogue

| **Step** | **Workflow Activity** | **Description** | **Performer** | **Output / Evidence** |
| --- | --- | --- | --- | --- |
| W01 | Collect Payroll Data  | Pull current/prior payroll, worker, time, absence, policy and statutory reference data. | Agent / Integration | Consolidated data set |
| W02 | Validate Input Data  | Check whether required files, fields, periods and worker populations are available. | Agent Control | Data completeness result and gap list |
| W03 | Detect Anomalies  | Run deterministic anomaly checks over payroll records and worker lifecycle data. | Agent Control | Anomaly register |
| W04 | Calculate Risk Score  | Calculate period payroll risk based on anomaly volume, severity and escalation status. | Agent Insight | Payroll risk score |
| W05 | Classify Anomaly  | Categorise anomaly type and severity. | Agent Task | Classified exception |
| W06 | Explain Payroll Calculation  | Generate gross-to-net explanation and variance analysis. | Agent Insight | Calculation explanation |
| W07 | Determine Root Cause  | Identify why the anomaly occurred. | Agent Insight | Root-cause assessment |
| W08 | Locate System of Record  | Locate whether root cause sits in HCM, Payroll, Time, Benefits, Identity or GL. | Agent Orchestration | Source system reference |
| W09 | Generate Correction Options  | Create possible correction options based on policy, tolerance and source system. | Agent Task | Correction options |
| W10 | Assess Impact  | Assess payroll, tax, NI, pension, GL, employee and compliance impact. | Agent Insight | Impact assessment |
| W11 | Create Recommendation  | Recommend preferred resolution with rationale and evidence. | Agent Task | Recommended action |
| W12 | Escalate for Approval  | Package recommendation for human review. | Agent Orchestration | Approval case |
| W13 | Review Recommendation  | Payroll Controller reviews evidence, impact and recommended action. | Human | Review outcome |
| W14 | Approve or Reject  | Human decision confirms whether correction can proceed. | Human Control | Approval decision |
| W15 | Commit Correction  | Apply approved correction through the agreed write-back path. | Payroll Team / System | Committed correction |
| W16 | Recalculate Payroll  | Recalculate affected employee/payroll result after correction. | Agent / Payroll System | Updated payroll result |
| W17 | Validate Outcome  | Confirm anomaly is resolved and nothing new has been introduced. | Agent Control | Validation result |
| W18 | Create Audit Evidence  | Create deterministic evidence pack for decision and correction. | Agent Control | Audit pack |
| W19 | Log Governance Actions  | Emit action, decision and evidence metadata to governance. | Agent Control | Governance log |
| W20 | Close Case  | Close the payroll assurance case and archive evidence. | Agent Orchestration | Closed case |

# Step 5 - Define Handovers and Interactions

| **From** | **To** | **Handover / Interaction** | **Output / Evidence** |
| --- | --- | --- | --- |
| HCM | Payroll Assurance Agent | Worker master, status, hire date, termination date, pay group and lifecycle events. | Worker data extract / API payload |
| Payroll System | Payroll Assurance Agent | Current and prior pay records including gross, tax, NI, pension, net, approvals and changed fields. | PayItem data extract / API payload |
| Time & Absence | Payroll Assurance Agent | Contracted hours, worked hours and absence days. | TimeRecord data extract / API payload |
| Benefits / Policy / Statutory Tables | Payroll Assurance Agent | Benefit deductions, pay policy, tolerance rules and statutory calculation tables.<br>(Benefits platform schema not yet modelled) | Reference data set |
| Payroll Assurance Agent | Payroll Controller | Anomaly details, root cause, options, impact, recommendation and evidence. | Approval case pack |
| Payroll Controller | Payroll Assurance Agent | Approve, reject, request more information or escalate decision. | Human decision record |
| Payroll Assurance Agent / Payroll Team | Payroll System | Approved correction only. | Correction transaction |
| Payroll System | Payroll Assurance Agent | Corrected payroll result for recalculation and validation. | Updated pay result |
| Payroll Assurance Agent | AI Governance / Audit Repository | Decision log, action log, validation result and audit evidence. | Governance log and audit pack |

# Decisions, Exceptions and Human Intervention Points

## Key Decision Points

| **Decision ID** | **Decision** | **Primary Performer** | **Evidence Required** |
| --- | --- | --- | --- |
| D01 | Is an anomaly detected? | Agent | Anomaly detection result |
| D02 | Is anomaly severity above tolerance? | Agent | Severity and tolerance rules |
| D03 | Does a valid approved change already exist? | Agent | Approval history and changed fields |
| D04 | Which system of record owns the issue? | Agent | Source system trace |
| D05 | Which correction option should be recommended? | Agent | Options and impact assessment |
| D06 | Does Payroll Controller approve the recommendation? | Payroll Controller | Approval decision and rationale |
| D07 | Was the correction successful? | Agent | Post-correction validation result |

## Exception Catalogue

| **Exception Class** | **Description** | **Expected Handling** |
| --- | --- | --- |
| Leaver still paid | Employee has termination date before period end, but gross pay remains above zero. | Escalate for review and correction approval. |
| Joiner not paid | New employee expected to be paid but no payroll result exists. | Escalate as high employee-impact issue. |
| Unexplained variance | Gross pay variance exceeds threshold and no approved change exists. | Diagnose root cause and recommend correction or explanation. |
| Missing tax code | Tax code is missing from payroll record. | Human-approved correction due to HMRC/RTI exposure. |
| Negative net pay | Net pay is below zero. | Escalate for urgent review. |
| Duplicate pay record | More than one pay record exists for the same worker and period. | Escalate and validate duplicate handling. |
| Unapproved change | Changed payroll field lacks required approval evidence. | Block or escalate based on control rules. |

## Human Intervention Points

| **Point** | **Where it occurs** | **Human Role** | **Why Required** |
| --- | --- | --- | --- |
| HIP-01 | Recommendation review | Payroll Controller | To confirm the agent recommendation is appropriate and evidence is sufficient. |
| HIP-02 | Correction approval | Payroll Controller | No pay correction should be committed without human approval. |
| HIP-03 | Material variance / policy exception | Payroll Controller / Payroll Manager as defined by governance | Higher-risk cases may require additional business judgement. |
| HIP-04 | Payroll sign-off | Payroll Controller | Payroll period sign-off remains a human accountability. |
| HIP-05 | Rejected or escalated recommendation | Payroll Controller / Payroll SME | Manual investigation is needed when the recommendation is not accepted. |

# Step 6 and Step 7 - SME Validation and Confirmation

## SME Walkthrough Checklist

| **Validation Area** | **Confirmation Question** | **Evidence to Capture** |
| --- | --- | --- |
| Capability | Does the workflow accurately represent the Payroll Assurance business capability? | SME confirmation notes |
| Workflow completeness | Are all major payroll assurance activities included? | Updated workflow or gap list |
| Granularity | Are the workflow steps at the right level of detail for design? | Accepted Workflow Decomposition catalogue |
| Decisions | Are all decision points and approval outcomes captured? | Key Decision Points sign-off |
| Exceptions | Are all known payroll exception classes represented? | Exception Catalogue sign-off |
| Human intervention | Are all approval and escalation points correct? | Human intervention Points sign-off |
| Handovers | Are all system, data and human handovers accurate? | Handover and Interactions sign-off |
| Outcome | Do the steps collectively deliver continuous payroll assurance? | SME confirmation of completeness |

# Completion Guidance

## Practitioner Guidance

Focus on the business process, not on how the solution will be built.

Use outcomes and decisions to identify the right steps.

Ensure no material activity is missed.

Keep steps at the correct level of detail for design.

## Key Success Factors

Clear understanding of the business intent.

Accurate workflow mapping and decomposition.

Early SME engagement and collaboration.

Complete handover definitions between steps.

## Common Pitfalls

Designing solution details too early.

Using steps that are too granular or too high level.

Missing exceptions and human interventions.

Unclear handovers and data exchanges.

# Appendix A - Glossary and Acronyms

| **Term / Acronym** | **Definition** |
| --- | --- |
| AI | Artificial Intelligence |
| SME | Subject Matter Expert |

