**Payroll Assurance Agent**

Stage 4 - Classify Deliverable | Capability-Based Agent Model

# Executive Summary

This Stage 4 deliverable classifies the Payroll Assurance Agent using a capability-based agent model rather than creating a separate agent for every workflow step.

The model consolidates the Stage 3 workflow steps into 9 meaningful capability agents across Experience, Orchestration, Task, Insight and Control categories.

The Experience Agent is the starting point for the user journey, supporting Payroll Controller review, approval, exception handling and access to audit evidence.

The Payroll Assurance Orchestrator coordinates the end-to-end workflow and routes work to Task, Insight and Control agents.

Control responsibility is consolidated into Quality Control, Governance & Audit and Human Approval Control agents to keep governance clear and proportionate.

Stage 4 Activities Covered

- 

| **No.** | **Stage 4 Activity** | **Payroll Assurance Output** |
| --- | --- | --- |
| 1 | Analyse the workflow step | Stage 3 workflow steps analysed and grouped into capability agents. |
| 2 | Identify agents and controls | 9 capability agents identified, including control mechanisms and human approval control. |
| 3 | Classify each agent | Each capability agent classified as Experience, Orchestration, Task, Insight or Control. |
| 4 | Define internal orchestration | Payroll Assurance Orchestrator coordinates agent interactions and handovers. |
| 5 | Define handovers | Inputs and outputs between capability agents are defined. |
| 6 | Define control point | Control points mapped across data, rules, evidence, approval, validation, audit and closure. |
| 7 | Create Framework for each agent | Framework provided for every capability agent. |
| 8 | Assess reuse using ABBA | Excluded by request. |

# 1. Capability-Based Agent Landscape

**Figure 1. Capability-based Stage 4 agent landscape with Experience Agent as the starting point.**

![image1](media/Payroll_Assurance_Agent_Stage_4_Classify_Capability_Based%20(2)/image1.png)

# 2. Agent Inventory and Classification

| **ID** | **Agent Name** | **Agent Type** | **Purpose** | **Workflow Coverage** |
| --- | --- | --- | --- | --- |
| A01 | Payroll Assurance Workspace Agent | Experience | User-facing workspace for Payroll Controller to view exceptions, review recommendations, approve/reject/escalate and access audit evidence.  | W13, W14 |
| A02 | Payroll Assurance Orchestrator | Orchestration | Coordinates the end-to-end payroll assurance case lifecycle, routes work to specialist agents, manages handovers, escalations and closure. | W08, W12, W15, W20 |
| A03 | Payroll Data Management Agent | Task | Collects payroll/workforce data and supports recalculation after approved corrections. | W01, W16 |
| A04 | Payroll Exception Processing Agent | Task | Runs payroll exception detection and generates resolution options for identified issues. | W03, W09 |
| A05 | Payroll Analysis Agent | Insight | Calculates risk, classifies exceptions, explains payroll calculations and diagnoses root cause. | W04, W05, W06, W07 |
| A06 | Payroll Decision Intelligence Agent | Insight | Assesses impact and creates decision-ready recommendations with rationale and evidence. | W10, W11 |
| A07 | Payroll Quality Control Agent | Control | Validates input completeness and validates correction outcome after recalculation. | W02, W17 |
| A08 | Payroll Governance & Audit Agent (AgentOps) | Control | Creates audit evidence packs and records governance actions, decisions and evidence lineage. | W18, W19 |
| A09 | Human Approval Control Agent | Control | Enforces mandatory human approval for pay-impacting changes and captures approval decisions & signs off the period | W13, W14, W15 |

# 3. Agent-to-Workflow Mapping

| **Workflow Step** | **Stage 3 Activity** | **Capability Agent Owner** |
| --- | --- | --- |
| W01 | Collect Payroll Data | A03 Payroll Data Management Agent |
| W02 | Validate Input Data | A07 Payroll Quality Control Agent |
| W03 | Detect Anomalies | A04 Payroll Exception Processing Agent |
| W04 | Calculate Risk Score | A05 Payroll Analysis Agent |
| W05 | Classify Anomaly | A05 Payroll Analysis Agent |
| W06 | Explain Payroll Calculation | A05 Payroll Analysis Agent |
| W07 | Determine Root Cause | A05 Payroll Analysis Agent |
| W08 | Locate System of Record | A05 Payroll Analysis Agent |
| W09 | Generate Correction Options | A04 Payroll Exception Processing Agent |
| W10 | Assess Impact | A06 Payroll Decision Intelligence Agent |
| W11 | Create Recommendation | A06 Payroll Decision Intelligence Agent |
| W12 | Escalate for Approval | A02 Payroll Assurance Orchestrator |
| W13 | Review Recommendation | A01 Workspace + A09 Approval Control |
| W14 | Approve, Reject or Escalate | A01 Workspace + A09 Approval Control |
| W15 | Commit Correction | A02 Orchestrator + A09 Approval Control |
| W16 | Recalculate Payroll | A03 Payroll Data Management Agent |
| W17 | Validate Outcome | A07 Payroll Quality Control Agent |
| W18 | Create Audit Evidence | A08 Governance & Audit Agent (AgentOps) |
| W19 | Log Governance Actions | A08 Governance & Audit Agent (AgentOps) |
| W20 | Close Case | A08 Governance & Audit Agent (AgentOps) |

# 4. Internal Orchestration

The Payroll Assurance Workspace Agent initiates and presents the user journey, acting as the entry point for Payroll Controller interaction.

The Payroll Assurance Orchestrator receives the case request, manages the case state and coordinates all downstream capability agents.

Task agents perform operational work such as data collection, anomaly detection, options generation and payroll recalculation.

Insight agents interpret results and produce risk scoring, classification, explanations, root-cause analysis, impact assessment and recommendations.

Control agents enforce mandatory controls across data quality, human approval, audit evidence, governance logging, validation and closure.

All outputs are passed back through the orchestrator so handovers, decisions and evidence lineage remain traceable.

- 

**Orchestration diagram - capability-based internal orchestration**

![image2](media/Payroll_Assurance_Agent_Stage_4_Classify_Capability_Based%20(2)/image2.png)
Revised Internal Orchestration Diagram Based on Agent Data Mapping (Input/Output)

![image6](media/Payroll_Assurance_Agent_Stage_4_Classify_Capability_Based%20(2)/image6.png)

# 5. Handover Matrix

| **From** | **To** | **Information Handed Over** | **Output / Evidence** |
| --- | --- | --- | --- |
| Payroll Assurance Workspace Agent | Payroll Assurance Orchestrator | User request, selected payroll run, exception view or approval action | Case initiated or decision captured |
| Payroll Assurance Orchestrator | Payroll Data Management Agent | Data collection request and payroll scope | Consolidated payroll assurance data set |
| Payroll Data Management Agent | Payroll Quality Control Agent | Collected payroll and workforce data | Data quality result and gap list |
| Payroll Quality Control Agent | Payroll Exception Processing Agent | Validated data set | Detected anomalies and initial exception list |
| Payroll Exception Processing Agent | Payroll Analysis Agent | Anomaly register and proposed correction options.  | Risk score, classification, explanation and root-cause assessment |
| Payroll Exception Processing Agent | Onboarding & Lifecycle Agent | Leaver still paid or Joiner not paid detected |  |
| Payroll Analysis Agent | Payroll Decision Intelligence Agent | Classified exception, explanation and root-cause evidence | Impact assessment and recommendation |
| Payroll Decision Intelligence Agent | Payroll Assurance Orchestrator | Recommended action, rationale, impact and evidence | Approval decision required |
| Payroll Assurance Orchestrator | Human Approval Control Agent | Approval case and decision options | Payroll Controller review outcome |
| Human Approval Control Agent | Payroll Data Management Agent | Approved, rejected or escalated decision | Commit, rework or close path |
| Payroll Data Management Agent | Payroll Quality Control Agent |  Approved correction and source system route | Recalculated payroll result |
| Payroll Quality Control Agent | Payroll Governance & Audit Agent (AgentOps) | Validation result and correction evidence | Audit pack and governance log |
| Payroll Governance & Audit Agent (AgentOps) | Payroll Assurance Orchestrator | Audit pack, decision log and action log | Closed case or open exception |

# 6. Control Point Model

**Figure 2. Consolidated control model across Payroll Assurance capability agents.**

![image3](media/Payroll_Assurance_Agent_Stage_4_Classify_Capability_Based%20(2)/image3.png)

| **Control ID** | **Control Point** | **Owning Agent** | **Workflow Coverage** | **Control Outcome** |
| --- | --- | --- | --- | --- |
| CP01 | Input completeness control | A07 Payroll Quality Control Agent | W02 | Blocks analysis if required records/fields are missing. |
| CP02 | Approved anomaly rule control | A04 Payroll Exception Processing Agent | W03 | Only approved deterministic anomaly rules are used. |
| CP03 | Risk and severity control | A05 Payroll Analysis Agent | W04-W05 | Applies agreed risk, severity and classification logic. |
| CP04 | Evidence sufficiency control | A06 Payroll Decision Intelligence Agent | W10-W11 | Recommendation must include impact, rationale and supporting evidence. |
| CP05 | Mandatory human approval control | A09 Human Approval Control Agent | W13-W15 | No pay-impacting correction can proceed without Payroll Controller approval. |
| CP06 | Segregation of duties control | A09 Human Approval Control Agent | W14-W15 | Agent recommends and prepares actions but does not approve pay-impacting changes. |
| CP07 | Post-correction validation control | A07 Payroll Quality Control Agent | W17 | Confirms correction resolved the anomaly and introduced no new issue. |
| CP08 | Audit evidence completeness control | A08 Payroll Governance & Audit Agent (AgentOps) | W18 | Audit pack must capture anomaly, diagnosis, recommendation, approval, correction and validation evidence. |
| CP09 | Governance logging control | A08 Payroll Governance & Audit Agent (AgentOps) | W19 | Decision, approval and action logs must be recorded. |
| CP10 | Case closure control | A02 Payroll Assurance Orchestrator | W20 | Case cannot close while actions remain open or evidence is incomplete. |

# 7. Human Approval Flow

**Figure 3. Human approval flow for recommendation review, approve/reject decisions and controlled correction commit.**

![image4](media/Payroll_Assurance_Agent_Stage_4_Classify_Capability_Based%20(2)/image4.png)

**Mermaid diagram - human approval and exception path**

![image5](media/Payroll_Assurance_Agent_Stage_4_Classify_Capability_Based%20(2)/image5.png)

# 8. Agent Frameworks

## Payroll Assurance Workspace Agent

| **Framework Component** | **Definition** |
| --- | --- |
| Agent type | Experience |
| Purpose | Provide the user-facing entry point for Payroll Controller review and approval. |
| Inputs | Approval case, anomaly summary, recommendation, audit evidence |
| Outputs | Review outcome, approval/rejection/escalation decision, comments |
| Key behaviours | Dashboard, exception view, recommendation review, evidence access, approval action capture |
| Human interaction | Payroll Controller review and decision capture |
| Exception handling | If recommendation is disputed, route to manual investigation or SME review. |

## Payroll Assurance Orchestrator

| **Framework Component** | **Definition** |
| --- | --- |
| Agent type | Orchestration |
| Purpose | Coordinate the end-to-end payroll assurance workflow and maintain case state. |
| Inputs | Workflow trigger, agent outputs, approval decision |
| Outputs | Next-step routing, case state update, commit/close instruction |
| Key behaviours | Sequence management, handover routing, escalation handling, correction orchestration and closure |
| Human interaction | Routes approval cases to Workspace and receives decision from Human Approval Control |
| Exception handling | If handover fails, hold case and trigger exception path. |

## Payroll Data Management Agent

| **Framework Component** | **Definition** |
| --- | --- |
| Agent type | Task |
| Purpose | Collect source data and support recalculation after approved correction. |
| Inputs | Payroll, HCM, Time, Absence, Benefits, Policy and Statutory data; approved correction |
| Outputs | Consolidated data set, recalculated payroll result |
| Key behaviours | Data retrieval, data preparation, payroll recalculation, source payload preparation |
| Human interaction | No direct approval, but receives approved correction instruction only |
| Exception handling | If source data unavailable or recalculation fails, escalate to Orchestrator. |

## Payroll Exception Processing Agent

| **Framework Component** | **Definition** |
| --- | --- |
| Agent type | Task |
| Purpose | Detect payroll anomalies and generate possible correction options. |
| Inputs | Validated payroll data, worker lifecycle data, policy/tolerance rules |
| Outputs | Anomaly register and correction options |
| Key behaviours | Run approved anomaly checks, create exception list, apply policy options |
| Human interaction | Outputs reviewed through downstream Insight and Approval agents |
| Exception handling | If exception class is unknown, route to manual investigation. |

## Payroll Analysis Agent

| **Framework Component** | **Definition** |
| --- | --- |
| Agent type | Insight |
| Purpose | Analyse payroll anomalies, calculate risk, classify, explain and diagnose root cause. |
| Inputs | Anomaly register, payroll records, prior payroll records, policy data |
| Outputs | Risk score, classified exception, explanation, root-cause assessment |
| Key behaviours | Risk scoring, classification, gross-to-net explanation, variance analysis, root-cause diagnosis |
| Human interaction | Supports Payroll Controller by generating explainable evidence |
| Exception handling | If evidence is insufficient, request additional data or manual review. |

## Payroll Decision Intelligence Agent

| **Framework Component** | **Definition** |
| --- | --- |
| Agent type | Insight |
| Purpose | Assess impact and create recommendation for human decision. |
| Inputs | Root cause, correction options, pay/tax/pension/GL context |
| Outputs | Impact assessment and recommended correction |
| Key behaviours | Impact analysis, option comparison, recommendation rationale, evidence packaging |
| Human interaction | Prepares decision-ready recommendation for human review |
| Exception handling | If impact is material or outside tolerance, escalate for additional approval. |

## Payroll Quality Control Agent

| **Framework Component** | **Definition** |
| --- | --- |
| Agent type | Control |
| Purpose | Validate data quality and post-correction outcome. |
| Inputs | Collected data set, recalculated payroll result, original anomaly |
| Outputs | Data validation result and post-correction validation result |
| Key behaviours | Input completeness check, data quality check, validation after correction |
| Human interaction | No direct human approval, but can block progression if controls fail |
| Exception handling | If validation fails, route back to Orchestrator for rework. |

## Payroll Governance & Audit Agent (AgentOps)

| **Framework Component** | **Definition** |
| --- | --- |
| Agent type | Control |
| Purpose | Create audit evidence and record governance actions. |
| Inputs | Workflow history, approval decision, correction evidence, validation result |
| Outputs | Audit evidence pack and governance log |
| Key behaviours | Evidence compilation, action logging, decision logging, audit readiness checks |
| Human interaction | Provides evidence to Payroll Controller, audit, risk and compliance stakeholders |
| Exception handling | If evidence pack incomplete, keep case open until completed. |

## Human Approval Control Agent

| **Framework Component** | **Definition** |
| --- | --- |
| Agent type | Control |
| Purpose | Enforce mandatory human approval before pay-impacting correction is committed. |
| Inputs | Recommendation, evidence, approval rules, Payroll Controller decision |
| Outputs | Approval decision, rejection, escalation or commit authorisation |
| Key behaviours | Human approval gate, SoD enforcement, approval record capture |
| Human interaction | Captures Payroll Controller approval/rejection/escalation decision |
| Exception handling | If approval missing or outside authority, block correction commit. |

# 9. Assess reuse using ABBA

| **Workflow Step** | **Capability Agent Owner** | **Match in ABBA** | **ABBA Agent ID** | **ABBA Agent Name** | **Agent Type** | **Purpose / Usage** | **Reuse Assessment** | **Variance From Requirement** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W01 Collect Payroll Data | A03 Payroll Data Management Agent | No | N/A | N/A | Task | Collect payroll, HR, benefits and time-record data from source systems | New design |  |
| W02 Validate Input Data | A07 Payroll Quality Control Agent | Yes | VA-1246 | Payroll data validator | Task | Validate payroll data completeness, accuracy and consistency | Adapted | Focus only on payroll data validation can be used as part of payroll quality control agent |
| W02 Validate Input Data | A07 Payroll Quality Control Agent | Yes | VA-1172 | Data validation agent | Task | Validates employee data for accuracy, completeness, and consistency. | Adapted | Focus only on employee data validation can be used as part of payroll quality control agent |
| W02 Validate Input Data | A07 Payroll Quality Control Agent | Yes | VA-1279 | Time record validator | Task | Validates time records for accuracy, completeness, and policy compliance. | Adapted | Focus only on time record data validation, can be used as part of payroll quality control agent |
| W03 Detect Anomalies | A04 Payroll Exception Processing Agent | Yes | VA-1149 | Policy enforcement & anomaly detection agent | Control | Detect compensation and payroll anomalies | Not suitable asset | The compensations anomalies is not one of the seven anomalies (leaver-still-paid, joiner-not-paid, unexplained 45% variance, missing tax code, negative net, duplicate, unapproved change) from the scope |
| W03 Detect Anomalies | A04 Payroll Exception Processing Agent | Yes | VA-1266 | Policy enforcement & anomaly detection agent | Control | Identifies anomalies in compensation data and enforces policy compliance. | Not suitable asset | The compensations anomalies is not one of the seven anomalies (leaver-still-paid, joiner-not-paid, unexplained 45% variance, missing tax code, negative net, duplicate, unapproved change) from the scope |
| W04 Calculate Risk Score | A05 Payroll Analysis Agent | No | N/A | N/A | Insight | Calculate risk score for detected payroll anomalies | New Design |  |
| W05 Classify Anomaly | A05 Payroll Analysis Agent | No | N/A | N/A | Insight | Categorize payroll exceptions into defined classifications | New Design |  |
| W06 Explain Payroll Calculation | A05 Payroll Analysis Agent | Yes | VA-1267 | Payroll experience agent | Experience | Explain payroll calculations and exception details to users | Not suitable asset | Unsure the capability of the experience agent can explain the anomalies category in the scope. |
| W06 Explain Payroll Calculation | A05 Payroll Analysis Agent | Yes | VA-1253 | Payroll experience agent | Experience | Creates positive payroll experiences through clear communication and prompt issue resolution. | Not suitable asset | Unsure the capability of the experience agent can explain the anomalies category in the scope. |
| W07 Determine Root Cause | A05 Payroll Analysis Agent | No | N/A | N/A | Insight | Identify root cause of payroll anomalies | New Design |  |
| W08 Locate System of Record | A05 Payroll Analysis Agent | No | N/A | N/A | Insight | Determine originating system causing payroll issue | New Design |  |
| W09 Generate Correction Options | A04 Payroll Exception Processing Agent | No | N/A | N/A | Task | Generate correction and remediation options | New Design |  |
| W10 Assess Impact | A06 Payroll Decision Intelligence Agent | No | N/A | N/A | Insight | Assess business and payroll impact of correction options | New Design |  |
| <br>W11 Create Recommendation | A06 Payroll Decision Intelligence Agent | No | N/A | N/A | Insight | Recommend optimal corrective action | New Design |  |
| W12 Escalate for Approval | A02 Payroll Assurance Orchestrator | No | N/A | N/A | Orchestration | Escalate high-risk cases to Payroll Controller | New Design |  |
| W13 Review Recommendation | A01 Payroll Assurance Workspace Agent<br>A09 Human Approval Control Agent | No | N/A | N/A | Experience + Control | Assist human review for pay-impacting changes and captures approval decisions & signs off the period | New Design |  |
| W14 Approve, Reject or Escalate | A01 Payroll Assurance Workspace Agent<br>A09 Human Approval Control Agent | No | N/A | N/A | Experience + Control | Enforces mandatory human approval for pay-impacting changes and captures approval decisions & signs off the period | New Design |  |
| W15 Commit Correction | A02 Payroll Assurance Orchestrator<br>A09 Human Approval Control Agent | No | N/A | N/A | Orchestration + Control | Apply approved payroll corrections | New Design |  |
| W16 Recalculate Payroll | A03 Payroll Data Management Agent | Yes | VA-1145 | Automated payroll calculations agent | Task | Recalculate payroll after correction<br>Automates complex payroll calculations including bonuses, commissions, and adjustments. | Adapted | The agent serves the calculation purpose however the data source of calculation to be reviewed during design as the existing agent data source tends to get it from source system and 3rd party platform instead of Fabric. |
| W16 Recalculate Payroll | A03 Payroll Data Management Agent | Yes | VA-1248 | Automated payroll calculations agent | Task | Recalculate payroll after correction<br>Automates complex payroll calculations including bonuses, commissions, and adjustments. | Adapted | The agent serves the calculation purpose, however the data source of calculation to be reviewed during design as the existing agent data source tends to get it from source system and 3rd party platform instead of Fabric. |
| W16 Recalculate Payroll | A03 Payroll Data Management Agent | Yes | VA-11343 | Payroll recalculate | Task | Process payroll data where original values were incorrect, calculate the correct values and return the corrections in an HMRC approved format. | Adapted |  |
| W17 Validate Outcome | A07 Payroll Quality Control Agent | Yes | VA-1246 | Payroll data validator | Task | Revalidate corrected payroll results<br>Validates payroll data for accuracy, completeness, and consistency. | Adapted | The agent can be used directly for payroll result validation after correction as part of the quality control. |
| W18 Create Audit Evidence | A08 Governance & Audit Agent | No | N/A | N/A | Control | Assemble audit evidence and case documentation | New Design |  |
| W19 Log Governance Actions | A08 Governance & Audit Agent | Yes | VA-1304 | Data governance monitor | Control | Ensures reporting practices comply with data governance policies and standards. | Not suitable asset | The Data Governance Monitor Agent is responsible for continuously overseeing and validating that all reporting activities within the organization adhere strictly to established data governance policies and standards. However, this is not directly designed for logging purposes but rather monitoring have the governance been properly made. |
| W20 Close Case | A02 Payroll Assurance Orchestrator | Yes | VA-1249 | Payroll administration workflow manager | Process Agent | Coordinate payroll workflow closure | Not suitable asset | This agent helps to manage regular payroll administration workflow including case closing but not particularly with the flow in this scope. |
| W20 Close Case | A02 Payroll Assurance Orchestrator | Yes | VA-1251 | Payroll value stream manager | Value Stream Agent | Manage end-to-end payroll process completion | Not suitable asset | This agent helps to maintain regular payroll administration workflow, including case closing but not particularly with the flow in this scope. |

# 10. Stage 4 Output Summary

| **Required Stage 4 Output** | **Status** |
| --- | --- |
| Agent inventory per workflow step | Included as capability-agent grouped inventory and workflow mapping. |
| Agent classifications | Included for every capability agent. |
| Internal orchestration diagrams | Included with visual diagram and Mermaid diagram. |
| Handovers to previous and next steps | Included through capability handover matrix. |
| Control point defined for every step | Included through consolidated control point model and control matrix. |
| Framework for every agent | Included for all 9 capability agents. |
| ABBA reuse assessment and variance log | Included |

