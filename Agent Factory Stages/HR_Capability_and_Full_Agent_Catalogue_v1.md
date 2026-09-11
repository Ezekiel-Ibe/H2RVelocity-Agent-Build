**HR REIMAGINED**

**HR Capability & Full Agent Catalogue: Engineering Specification**

Part 1 for HR - agents & outcomes to follow and approve · Part 2 the full engineering catalogue

One document, two parts, mirroring the O2C catalogue. Part 1 lets HR follow and approve each value stream, its objective, agents, outcomes and client value. Part 2 is the full engineering specification: ontology, the deterministic-core / LLM boundary, a tool catalogue, cross-cutting orchestration and governance, per-value-stream build specifications (with use cases, inputs/outputs, deterministic calculations, human-in-the-loop, controls, risks, evaluation and maturity), per-agent engineering detail (ID card, data schema, generic script, skills), a collaboration matrix and build sequencing.

# Part 1 - For HR: agents, outcomes & client value

| **Value stream** | **Objective** | **Lead agent** | **Client outcome** |
|----|----|----|----|
| Recruit to Offboard | Continuous Workforce Activation | Onboarding & Lifecycle Agent | Day-one-productive joiners paid right first time; no leaver paid in error. |
| Talent Design to Evaluate | Continuous Workforce Development | Learning & Skills Agent | Capability gaps closed faster and cheaper; higher mobility and AI literacy; ratings kept human. |
| Measure to Reward | Optimised Business Partnering | Workforce-Intelligence Copilot | Defensible, evidence-based reward and pay-equity compliance; faster cited advisory. |
| Manage Workforce Relations to Experience | Continuous Workforce Safeguarding | Employee Service + ER/IR Intake Agents | Lower cost-to-serve; consistent policy; safe, human-led ER handling. |
| Plan to Optimize Total Workforce | Continuous Workforce Shaping & Planning | Workforce Shaping Agent | Optimal total-workforce mix and cost, planned in days, with a defensible human-vs-agent decision. |
| Workforce Schedule to Pay | Continuous Payroll Assurance | Payroll Assurance Agent | Right-first-time, compliant pay; leakage down, audit halved, every correction evidenced. |
| Govern to Evolve | Continuous Agent Workforce Management | AgentOps Control Tower | The digital workforce governed as a workforce - registry, zero SoD breaches, AI-Act/ISO 42001 conformance. |

*Each stream owns an objective; a team of agents resolves each decision and a human approves anything consequential, with segregation of duties, write-back to the system of record, evidence and a learning loop.*

# Part 2 - Engineering specification

# 0. Purpose, scope & how to use

This catalogue specifies the HR agent estate to the level an engineering team needs to build. Section 1 defines the ontology; Section 2 the deterministic-core / LLM boundary; Section 3 the tool catalogue; Section 4 cross-cutting orchestration and governance; Section 5 the per-value-stream build specifications; Section 6 the per-agent engineering detail; Section 7 the collaboration matrix; Section 8 build sequencing. Cores marked built are tested reference implementations; the rest are build-next and their design intent is specified here.

# 1. HR Ontology & Knowledge Graph - core entity model

One canonical, HCM-neutral Workforce model (maps to Workday / SAP SuccessFactors / Oracle HCM / ADP). Worker, position and cost entities are shared with the Finance domain (one enterprise graph).

| **Entity** | **Status** | **Key attributes** |
|----|----|----|
| Worker | built | worker_id, type (employee/contingent/agent), status, hire_date, term_date, pay_group, fte, skills |
| Position | built | position_id, job_id, org_id, budgeted_fte, status (filled/vacant) |
| PayItem | built | worker_id, gross, base, allowances, overtime, tax, ni, tax_code, ni_category, pension, rti_status, net, approved_by, changed_fields |
| TimeRecord | built | worker_id, contracted_hours, worked_hours, absence_days |
| CapabilityDemand | built | capability, demand_fte, supply_fte, agentifiable_pct, avg_cost_human, avg_cost_agent |
| Case | built | case_id, worker_id, stream (service/er), category, priority, sla_hours, channel, auto_resolvable |
| ERCase | built | case_id, worker_id, risk_type, severity, status, flags (union/psychosocial/legal) |
| Event | built | event_id, type (joiner/mover/leaver/payrun), worker_id, date |
| AgentReg | built | agent_id, name, domain (HR/Finance/O2C), agent_class, status, cost, tokens, drift, sod_ok, escalation |
| RewardGroup | build-next | group, comparators, avg_pay, controls (role/level/tenure) |
| Skill / Learning | build-next | skill_id, worker_id, proficiency, demand, learning_path, agentifiable |

## 1.1 Core relationships

- Worker -\> fills -\> Position

- Position -\> in -\> OrgUnit

- Worker -\> paid via -\> PayItem

- Worker -\> records -\> TimeRecord

- Worker -\> raises -\> Case / ERCase

- Worker -\> subject of -\> Event

- CapabilityDemand -\> resourced by -\> Worker (human/contingent/agent)

- AgentReg -\> governs -\> Agent workforce (cross-domain)

## 1.2 Event chain

joiner -\> onboarding tasks -\> access provisioning -\> first-pay enrolment -\> payrun -\> (mover/leaver) -\> offboarding -\> final pay -\> access revoke. Each event ties to entity state and is the trigger for the relevant decision workspace.

## 1.3 Known data gaps to close before build

- Persistent agent memory is not built in any domain (platform-wide roadmap gap).

- Total-rewards / compensation schema (RewardGroup) and skills/learning schema are build-next.

- Contingent-labour and procurement (SOW) data not yet integrated.

- Benefits platform schema not yet modelled.

- Identity/access (joiner/leaver provisioning) integration to be defined per client.

# 2. Design principle - deterministic core / LLM boundary

Every figure, threshold, anomaly, gap, scenario and score is computed by a tested deterministic core - no model call for numbers. The LLM is used only for grounded narration (explaining pay, drafting a bounded service response, summarising a case), always cited and never for a consequential decision. This is the assurance principle carried from the Finance recon/adjustments agents: the agent narrates and routes; it does not calculate or decide the consequential.

# 3. Tool catalogue

Deterministic functions per agent (the tested cores and their build-next equivalents).

| **Agent** | **Tool (deterministic function)** | **Computes** |
|----|----|----|
| Onboarding & Lifecycle Agent | lifecycle_integrity | cross-system joiner/leaver integrity exceptions |
| Onboarding & Lifecycle Agent | lifecycle_check | per-worker integrity issue + severity |
| Learning & Skills Agent | skills_gap | capability gap (FTE) |
| Learning & Skills Agent | dev_route | development route |
| Workforce-Intelligence Copilot | pay_equity | pay-equity gap % + flag |
| Workforce-Intelligence Copilot | evidence_pack | decision-ready evidence pack |
| Employee Service | triage_case | case routing decision |
| Employee Service | er_triage | ER risk class, severity, flags |
| Workforce Shaping Agent | workforce_mix | human/contingent/agent mix |
| Workforce Shaping Agent | capability_gaps | capability gap register (FTE) |
| Workforce Shaping Agent | agentify_scenario | agentify cost delta (net/month) |
| Workforce Shaping Agent | resource_decision | human/blended/agent recommendation |
| Payroll Assurance Agent | detect_anomalies | 7-class anomaly register |
| Payroll Assurance Agent | risk_score | period payroll risk score |
| Payroll Assurance Agent | classify_pay_anomaly | variance + anomaly class + severity |
| Payroll Assurance Agent | explain_pay | gross-to-net breakdown |
| Payroll Assurance Agent | audit_pack | deterministic computation |
| AgentOps Control Tower | fleet_summary | fleet cost/drift/SoD summary |
| AgentOps Control Tower | sod_check | segregation-of-duties violations |
| AgentOps Control Tower | compliance_coverage | AI-Act/ISO 42001 coverage % |
| AgentOps Control Tower | fleet_meter | digital-labour cost + SoD |

# 4. Cross-cutting - orchestration, registry & governance

## 4.1 Cross-agent communication

| **From** | **To** | **Message / trigger** |
|----|----|----|
| Payroll Assurance | Onboarding & Lifecycle | leaver-still-paid / joiner-not-paid detected -\> lifecycle remediation |
| Workforce Shaping | AgentOps | agentify scenario accepted -\> onboard a new agent (digital establishment) |
| Onboarding & Lifecycle | Identity/IT | access provision/revoke request (approved) |
| Any agent | AgentOps | action + cost + decision log (continuous) |
| Workforce Shaping | Finance EPM | establishment / cost post (approved) |
| Employee Service | ER/IR Intake | sensitive case -\> ER escalation |

## 4.2 Agent registry

| **Agent** | **Owner (persona)** | **Knowledge sources** | **Status** |
|----|----|----|----|
| Onboarding & Lifecycle Agent | HR Operations Lead | Workforce Knowledge Graph + policy | core built & tested |
| Learning & Skills Agent | HRBP + CLO / L&D | skills/policy (build-next) | build-next |
| Workforce-Intelligence Copilot | Reward + HRBP | skills/policy (build-next) | build-next |
| Employee Service + ER/IR Intake Agents | HR Operations / ER Specialist | Workforce Knowledge Graph + policy | core built & tested |
| Workforce Shaping Agent | CHRO / Workforce Strategy | Workforce Knowledge Graph + policy | core built & tested |
| Payroll Assurance Agent | Payroll Controller | Workforce Knowledge Graph + policy | core built & tested |
| AgentOps Control Tower | AI Governance / AgentOps Lead | Workforce Knowledge Graph + policy | core built & tested |

## 4.3 Segregation-of-duties matrix

| **Outcome** | **Agent initiates** | **Human approves (cannot be the initiator)** |
|----|----|----|
| Continuous Workforce Activation | Onboarding & Lifecycle Agent (detect/propose) | HR Operations Lead |
| Continuous Workforce Development | Learning & Skills Agent (detect/propose) | HRBP + CLO / L&D |
| Optimised Business Partnering | Workforce-Intelligence Copilot (detect/propose) | Reward + HRBP |
| Continuous Workforce Safeguarding | Employee Service + ER/IR Intake Agents (detect/propose) | HR Operations / ER Specialist |
| Continuous Workforce Shaping & Planning | Workforce Shaping Agent (detect/propose) | CHRO / Workforce Strategy |
| Continuous Payroll Assurance | Payroll Assurance Agent (detect/propose) | Payroll Controller |
| Continuous Agent Workforce Management | AgentOps Control Tower (detect/propose) | AI Governance / AgentOps Lead |

## 4.4 Audit trail schema

Per case: case_id; source_data_snapshot; agent_reasoning/trace; recommendation; human_decision {approver_identity, timestamp, decision}; system_writeback_ref; downstream_confirmations\[\]; outcome; learning_captured. Immutable, reversible, retained per policy. Aligned to SOX-style payroll controls, EU AI Act logging/oversight and ISO/IEC 42001.

## 4.5 Compliance framework cross-reference

| **Framework** | **Primarily applies to** | **What the build must satisfy** |
|----|----|----|
| EU AI Act | payroll, ER, workforce evaluation | high-risk employment uses kept assistive/human-approved; logging, transparency, human oversight (obligations deferred to 2 Dec 2027) |
| ISO/IEC 42001 | the agent fleet (Govern to Evolve) | AI management system - registry, monitoring, conformance evidence |
| ISO 30414 | workforce & cost reporting (Plan, Reward) | human-capital metric definitions and reporting |
| UK GDPR / DPA 2018 | all worker data; ER Art. 9 | lawful basis, purpose limitation, DPIA, special-category controls |
| HMRC PAYE / RTI | payroll | statutory pay accuracy and reporting |
| EU Pay Transparency Directive | reward / pay-equity | pay-gap disclosure and evidence (enforceable Jun 2026) |
| ACAS / NYC LL144 / SOX-style | ER; hiring; payroll controls | fair process; bias audit; control evidence |

## 4.6 Evaluation framework by component type

| **Component type** | **What the build must evaluate** |
|----|----|
| Deterministic core | unit tests + coverage; correctness vs worked reference; zero false consequential actions in backtesting |
| Classification / triage | precision/recall vs labelled set; false-positive/negative rate |
| LLM narration | grounding / faithfulness; citation completeness; no unsupported claims |
| End-to-end workspace | % decisions approved without amendment; cycle time; audit-evidence completeness; autonomy-limit adherence |

# 5. Per-value-stream build specifications

## 1. Recruit to Offboard - Continuous Workforce Activation

**Owner persona:** HR Operations Lead

**Agents:** Onboarding & Lifecycle Agent

**Behaviours:** Detect -\> Diagnose -\> Cross-check -\> Recommend -\> Remediate

### Purpose

Enforce joiner-to-pay and leaver-to-pay integrity across HCM and payroll — the cross-system control single-suite ERPs do not enforce end to end.

### Use case

During the June pay run, W-014 (terminated 31 May) is still active on payroll for GBP 1,890 and W-020 (joined 2 June) is missing from pay entirely. The team detects both from a lifecycle-vs-payroll-vs-access cross-check, diagnoses a broken leaver feed and an onboarding step completing after the payroll cut-off, identifies HCM and the HCM-\>payroll interface as the systems of record, recommends stop-pay + access revoke + recovery for W-014 and an off-cycle payment for W-020, HR Ops and IT approve, the corrections are written back, and both cases close with a control-improvement recommendation (event-driven leaver sync; day-one readiness gate).

### Inputs (entities read)

- Worker master & status

- Lifecycle events (joiner/mover/leaver)

- Current payroll

- Onboarding/offboarding checklists

### Outputs (entities written)

- IntegrityExceptions: worker, kind, severity

### Deterministic calculation requirements

- Deterministic set operations: leaver_still_paid = status==leaver AND worker in payroll_current; joiner_not_paid = status==active AND hire_date\<=period_end AND worker NOT in payroll_current; onboarding_incomplete = joiner event present AND (checks\|access\|first-pay flags open). No model call.

- Severity is rule-based (high for pay/access breaks). Remediation options are a governed lookup by exception type.

### Human-in-the-loop boundary

HR Operations approves remediation; IT approves access changes. Escalates: Pay stop/start and access changes — human-approved; Right-to-work / eligibility exceptions.

### Governance & compliance controls

- No autonomous pay or access change

- Segregation of duties

- Evidence trail for audit

- Deterministic core, unit-tested

- Standards: Right-to-Work / immigration compliance; UK GDPR; ISO/IEC 27001 (joiner/leaver access controls); Payroll accuracy (PAYE/RTI)

### Risks

- A silent leaver-feed failure hides leaver-still-paid cases - the integrity check must run every cycle, not on-demand only.

- Auto-revoking access on a false leaver flag locks out an active worker - access changes require IT approval, never autonomous.

### Evaluation criteria

- Recall of leaver-still-paid / joiner-not-paid against a labelled historical set (target 100% on high-severity).

- % exceptions remediated within SLA; zero autonomous pay/access changes in backtesting.

### Maturity / demo posture

Built & tested — the cross-system integrity check that single-suite ERPs miss.

## 2. Talent Design to Evaluate - Continuous Workforce Development

**Owner persona:** HRBP + CLO / L&D

**Agents:** Learning & Skills Agent

**Behaviours:** Infer -\> Gap -\> Route -\> Recommend -\> (human) -\> Assign

### Purpose

Develop the whole workforce — build human skills and AI literacy, and continuously improve the agent workforce — so capability keeps pace with an AI-first operating model.

### Use case

For the capability plan, the agent infers skills demand and supply, computes a 1.0 FTE gap in Data & Analytics (40% agentifiable) and recommends a blended route (upskill + assistive agent), while Nursing (0% agentifiable) is routed to hire/upskill. The HRBP and CLO approve the development plan; ratings and promotions remain human.

### Inputs (entities read)

- Skills taxonomy, demand & supply

- Capability gaps & agentifiable ceilings

- Role & career frameworks

- Agent performance telemetry (drift, accuracy, cost)

### Outputs (entities written)

- DevelopmentPlan: capability, gap, route

### Deterministic calculation requirements

- Deterministic: gap_fte = demand_fte - supply_fte; dev_route by agentifiable threshold (\>=0.5 deploy-agent, \>=0.25 blended, else upskill/hire). Skills inference (matching people to skills) is probabilistic and build-next.

- No autonomous rating or promotion.

### Human-in-the-loop boundary

CHRO / HRBP own development, mobility and performance; AI Governance owns agent-tuning approvals. Escalates: All promotion, pay-affecting development and formal performance decisions — human-led; Agent retraining that changes scope — human-approved.

### Governance & compliance controls

- Development recommendations advisory only

- No autonomous performance rating

- Agent tuning logged & reversible

- Human owns career and rating decisions

- Standards: ISO 30414 (skills & development metrics); EU AI Act (worker evaluation kept advisory); UK GDPR; ISO/IEC 42001 (agent lifecycle for the digital workforce)

### Risks

- Skills inference bias skews development recommendations - inference is advisory and human-reviewed; build-next with fairness evaluation.

- Automating performance ratings breaches EU AI Act worker-evaluation constraints - kept human.

### Evaluation criteria

- Gap/route correctness vs a worked reference; internal-mobility fill rate.

- Skills-inference precision/recall once built; adverse-impact monitoring on development recommendations.

### Maturity / demo posture

Human learning & mobility recommendation is proven; continuous, closed-loop agent improvement (‘HR for agents’ development) is Emerging.

## 3. Measure to Reward - Optimised Business Partnering

**Owner persona:** Reward + HRBP

**Agents:** Workforce-Intelligence Copilot

**Behaviours:** Assemble -\> Compute equity -\> Evidence -\> (human) -\> Record

### Purpose

Give business leaders fast, evidence-based workforce recommendations — assembling planning data, policy and analytics into decision-ready packs — while HRBPs and leaders stay accountable.

### Use case

For the pay review, the copilot computes pay-equity gaps across four comparison groups, finds Engineering at 6.7% (above the 5% threshold) and Operations at 7.8%, assembles decision-ready evidence packs with rationale and an approval trail, and surfaces them to Reward and the HRBP - who decide. The agent makes no pay decision, and the packs double as EU pay-transparency evidence.

### Inputs (entities read)

- Workforce plan, gaps & scenarios

- People analytics & cost

- Policy & guidance

- Leader question / decision context

### Outputs (entities written)

- EvidencePack: gap, rationale, approval trail

### Deterministic calculation requirements

- Deterministic: pay_gap_pct = (avg_group_a - avg_group_b)/avg_group_a; flag if \|gap\| \> configurable threshold (default 5%). Evidence-pack assembly is deterministic aggregation; grounded LLM narrates, cited. Total-rewards agent build-next.

- No autonomous pay decision (advisory only).

### Human-in-the-loop boundary

HRBPs and business leaders own every workforce decision. Escalates: All workforce decisions — org design, hiring, restructuring — human-led; Low-confidence or sensitive questions.

### Governance & compliance controls

- Advisory only; documented rationale & approval trail

- No autonomous people decisions

- Provenance on every figure

- Standards: UK GDPR; EU AI Act (advisory, non-decisioning); ISO 30414 (workforce analytics)

### Risks

- A naive pay-gap comparison without controls (role, level, tenure) misleads - comparison groups must be like-for-like; methodology is a governed input.

- Acting on gaps autonomously is both unlawful and unwise - the agent evidences, humans decide.

### Evaluation criteria

- Pay-gap computation correctness vs a worked reference; coverage of comparison groups.

- % decisions supported by an evidence pack; grounding/faithfulness of the narrative.

### Maturity / demo posture

Assembling evidence packs from structured data is Built-ready; fully autonomous advisory is Emerging.

## 4. Manage Workforce Relations to Experience - Continuous Workforce Safeguarding

**Owner persona:** HR Operations / ER Specialist

**Agents:** Employee Service + ER/IR Intake Agents

**Behaviours:** Triage -\> Classify -\> Route/Resolve -\> (human for ER) -\> Close

### Purpose

Be the employee/manager front door — answer, triage, resolve bounded self-service, and route sensitive matters to a human — lowering cost-to-serve while protecting experience.

ER/IR: Take in and risk-classify employee/industrial-relations cases, retrieve policy and draft a timeline — accelerating specialists while keeping every determination human-led.

### Use case

Ten cases arrive at the front door. The Service agent auto-resolves five bounded, policy-covered self-service requests within the playbook (with provenance), routes two non-standard cases to an HR advisor, and hands three employee-relations cases to the ER/IR Intake agent, which classifies risk (grievance/disciplinary/wellbeing), flags union / psychosocial / legal exposure, retrieves policy and drafts a timeline - but makes no determination. An ER specialist owns each outcome.

### Inputs (entities read)

- Employee/manager query & identity

- Case category, priority, SLA

- Policy & knowledge base

### Outputs (entities written)

- Routing: auto_resolve / route_human / escalate_er

### Deterministic calculation requirements

- Deterministic triage: decision by category + priority + SLA rules (auto_resolve \| route_human \| escalate_er). ER risk classification by presence of union/psychosocial/legal flags -\> severity + routing. Grounded LLM drafts responses for bounded self-service only, with citations.

- Deflection rate = auto_resolved / total.

### Human-in-the-loop boundary

HR Operations owns exceptions, tier-2+ and all ER routing. Escalates: All ER-stream cases to a human specialist; Non-standard or high-priority to an HR advisor; Low-confidence answers.

### Governance & compliance controls

- ER cases never auto-actioned

- Provenance on every answer

- Human review of low-confidence / sensitive

- QA sampling of auto-resolved

- Standards: UK GDPR (employee data, records); Accessibility (WCAG) for the front door; Records-management / retention; Equality Act (consistent treatment)

### Risks

- An auto-resolved answer that misreads policy misinforms an employee - responses are grounded with provenance and QA-sampled.

- An ER case mis-triaged as service is a compliance and fairness risk - any ambiguity routes to a human; ER is never auto-actioned.

### Evaluation criteria

- Containment/deflection rate and first-contact resolution; reopen rate.

- ER routing precision (zero ER cases auto-resolved); grounding/faithfulness score on drafted responses.

### Maturity / demo posture

Built & tested. Tier-0/1 deflection is proven industry practice; broader autonomous resolution is Emerging.

## 5. Plan to Optimize Total Workforce - Continuous Workforce Shaping & Planning

**Owner persona:** CHRO / Workforce Strategy

**Agents:** Workforce Shaping Agent

**Behaviours:** Model -\> Gap -\> Scenario -\> Decide -\> (human) -\> Post establishment

### Purpose

Plan the total workforce — human, contingent and AI-agent — against demand, skills and cost, and answer whether work should be done by a person, a contractor or an agent.

### Use case

For the FY plan, the Shaping agent computes the total-workforce mix (13 employees, 2 contingent, 3 agents) and four capability gaps. For Payroll ops (55% agentifiable) it models shifting 1.1 FTE to an agent for a net GBP 3,520/month saving; Nursing (clinical) is flagged non-agentifiable. It recommends a blended mix, the CHRO and Finance approve, and the budgeted digital establishment is posted to the Finance EPM.

### Inputs (entities read)

- Workforce master (type, FTE, skills)

- Capability demand & supply

- Position budget / establishment

- Unit costs (human vs agent)

- Skills taxonomy

### Outputs (entities written)

- ShapingResult: mix, gaps, scenarios

### Deterministic calculation requirements

- Deterministic: gap_fte = demand_fte - supply_fte; scenario net = shift_fte x (agent_unit_cost - human_unit_cost), bounded by the capability's agentifiable ceiling; resource_decision by threshold (\>=0.5 -\> agent, \>=0.25 -\> blended, else human; clinical/safety-critical -\> human). No model call for the numbers.

- Digital-establishment cost = sum(agent_fte x agent_unit_cost).

### Human-in-the-loop boundary

CHRO / Workforce Strategy owns all org-design and resource-mix decisions. Escalates: All hire / agentify / redeployment decisions to CHRO / Workforce Strategy — advisory only.

### Governance & compliance controls

- Recommendations advisory only

- Clinical/safety-critical roles flagged non-agentifiable

- Assumptions & unit costs transparent and logged

- Deterministic core, unit-tested

- Standards: ISO 30414 (human-capital reporting); EU AI Act (workforce-management uses may be high-risk — kept advisory); Works-council / employee-consultation duties; UK GDPR

### Risks

- Agentifiable ceilings set too high recommend over-automation of nuanced work - ceilings are governed inputs, reviewed as tools mature.

- Establishment write-back to Finance without joint HR/Finance/IT authority breaks position control - write-back is approval-gated.

### Evaluation criteria

- Scenario-maths correctness vs a worked reference; clinical roles never recommended for agentification.

- Forecast-vs-actual demand accuracy over time; planning-cycle time reduction against the KR.

### Maturity / demo posture

Built & tested. Scenario maths deterministic; live cross-function demand sensing (HR+Finance+Procurement) is Emerging.

## 6. Workforce Schedule to Pay - Continuous Payroll Assurance

**Owner persona:** Payroll Controller

**Agents:** Payroll Assurance Agent

**Behaviours:** Detect -\> Explain -\> Diagnose -\> Options -\> Impact -\> Recommend -\> (human) -\> Commit -\> Validate -\> Close

### Purpose

Provide continuous, deterministic assurance that every employee-lifecycle change is correctly reflected in pay, before it becomes an employee-facing error or a compliance breach.

### Use case

Pre sign-off of the June run, the Detection agent flags seven anomalies (leaver-still-paid, joiner-not-paid, unexplained 45% variance, missing tax code, negative net, duplicate, unapproved change) and scores period risk at 88%. For each, the team diagnoses the cause, names the system of record, determines the permitted correction within tolerance, computes downstream impact (recalc, GL, comms, tax), and recommends. Within-tolerance items (duplicate, negative-net) are auto-corrected and logged; the rest are escalated to the Payroll Controller who approves, after which the correction is written back, validated and the case closed with a control recommendation.

### Inputs (entities read)

- Current & prior period pay records (gross, base, allowances, overtime, tax, NI, pension, deductions, net)

- Worker master & employment status

- Time & absence

- Lifecycle events (joiner/mover/leaver)

- Pay policy & statutory tables

### Outputs (entities written)

- AnomalyRegister: worker, kind, severity, amount

### Deterministic calculation requirements

- Deterministic: variance = (gross - prior_gross)/prior_gross; anomaly if \|variance\| \> configurable threshold AND no approved change. missing_tax_code if tax_code blank. leaver_still_paid if term_date \< period_end AND gross\>0. negative_net if net\<0. duplicate if count(pay records)\>1 per period. risk_score = escalated / lines.

- explain_pay: gross = base + allowances + overtime; net = gross - tax - NI - deductions. Exact arithmetic, no model call. Optional grounded LLM narrates the explanation only.

### Human-in-the-loop boundary

Payroll Controller approves all corrections and signs off the period. Escalates: Any pay correction; Comp-policy changes; Material variances above threshold — all to the Payroll Controller.

### Governance & compliance controls

- Segregation of duties — the agent never both changes and approves pay

- No auto-correction; human approval on every change

- Full action log to the AI Governance agent

- Deterministic core, unit-tested (12 tests)

- Standards: HMRC PAYE / Real-Time Information (RTI); Pensions Act 2008 auto-enrolment; National Minimum Wage Act; UK GDPR / DPA 2018 (employee data); ISO 30414 (workforce cost reporting); SOX-style payroll controls / audit evidence

### Risks

- An over-aggressive auto-correction tolerance recovers an overpayment that causes employee hardship - tolerance must be client-configured and conservative.

- A tax-code correction that mis-files RTI creates an HMRC exposure - tax corrections stay L2 (human-approved).

### Evaluation criteria

- Anomaly-detection precision/recall vs a labelled pay-error set; false-positive rate below target.

- % corrections approved without amendment; audit-evidence completeness = 100%; zero pay auto-corrected outside tolerance in backtesting.

### Maturity / demo posture

Built & tested. Anomaly detection on structured payroll data is proven at BlackLine/Trintech-class controls maturity; continuous cross-cycle assurance at scale is Emerging.

## 7. Govern to Evolve - Continuous Agent Workforce Management

**Owner persona:** AI Governance / AgentOps Lead

**Agents:** AgentOps Control Tower

**Behaviours:** Observe -\> Meter -\> Monitor -\> Recommend -\> (human) -\> Certify/Retire

### Purpose

Manage the digital workforce as a workforce — onboard, credential, meter, monitor, develop, safeguard and retire AI agents across HR, Finance and O2C — with the same rigour and control plane applied to people.

### Use case

Across the HR/Finance/O2C fleet, the control tower meters GBP 4,200/month of digital-labour cost, finds zero segregation-of-duties breaches, and flags one agent with a drift signal. It auto-certifies the compliant agents within policy and recommends tune + re-certify for the drifting one; the Governance Lead confirms. A quarterly conformance pack is produced against the EU AI Act and ISO/IEC 42001.

### Inputs (entities read)

- Agent registry (cost, tokens, status, drift, segregation-of-duties)

- Access & credential scope

- Incident & escalation log

- Responsible-AI policy & model cards

### Outputs (entities written)

- FleetGovernance: cost, drift, SoD, coverage

### Deterministic calculation requirements

- Deterministic: fleet cost = sum(cost_per_run x runs); sod_violation if the same agent both acts on and approves an item; drift flag from evaluation telemetry vs baseline; conformance coverage = conformant_agents / total. No model call.

- Auto-certification is L3 within policy; onboarding, scope change and retirement are human-confirmed.

### Human-in-the-loop boundary

AI Governance Lead operates the control tower; HR, Finance and IT jointly authorise the digital establishment. Escalates: Onboarding a new agent (scope & access); Any autonomy or scope increase; Kill-switch / retirement — all human-confirmed.

### Governance & compliance controls

- Human confirmation for onboarding, scope change and retirement

- Segregation of duties enforced fleet-wide

- Full action & decision logging

- Kill-switch always human-operated

- Standards: EU AI Act (governance, logging, human oversight, transparency); NIST AI RMF; ISO/IEC 42001 (AI management system); ISO/IEC 23894 (AI risk); UK GDPR (DPIA)

### Risks

- Metering blind spots understate digital-labour cost - all agent actions must emit cost/consumption telemetry.

- An un-governed cross-vendor agent escapes the control plane - the registry must be the single book of record for every agent.

### Evaluation criteria

- % of fleet registered and continuously monitored (target 100%); SoD breaches (target 0).

- Conformance coverage vs EU AI Act / ISO 42001 (target \>=90%); mean time to detect drift.

### Maturity / demo posture

Metering, monitoring and governance of a small fleet is Built & tested; a full people-style lifecycle for hundreds of agents is Emerging — a genuine white space.

# 6. Agent-level engineering design detail

## 6.1 Onboarding & Lifecycle Agent

| **Agent ID** | **HR-RTO-001** |
|----|----|
| Capability | Onboarding & Lifecycle Integrity |
| Domain | HR |
| Owner | HR Operations |
| Tech owner | TBD — not yet assigned |
| Criticality | Tier 2 |
| Risk | Medium |
| Autonomy | L3 — Augmented+ (flags cross-system control breaks; remediation human-approved) |
| Runtime | Python (tested reference implementation) |
| Model | TBD — no model selected yet |
| Skills file | SKILL_lifecycle-integrity.md |
| Version | v1.0 (tested) |
| Status | core built & tested |
| Deployment | TBD — see Enterprise AI Platform Reference Architecture; not yet a client decision |

### Data schema

**Worker** *(workers.json)*

| **Field** | **Type** | **Description**            |
|-----------|----------|----------------------------|
| worker_id | string   | PK                         |
| status    | string   | active\|onboarding\|leaver |
| hire_date | date     |                            |
| term_date | date     |                            |

**Event** *(events.json)*

| **Field** | **Type** | **Description**               |
|-----------|----------|-------------------------------|
| event_id  | string   | PK                            |
| type      | string   | joiner\|mover\|leaver\|payrun |
| worker_id | string   | FK → Worker                   |
| date      | date     |                               |

**PayItem** *(payroll_current.json)*

| **Field** | **Type** | **Description**             |
|-----------|----------|-----------------------------|
| worker_id | string   | presence = paid this period |

### Systems of record

HCM + Payroll + Identity/IT. Write-back: proposed -\> approved (HR Operations Lead) -\> committed -\> confirmed -\> evidenced.

### Generic agent script

on joiner/mover/leaver event OR pay run:  
ex = lifecycle_integrity(workers, events, payroll, access) \# L3 detect  
for e in ex:  
cause = classify(e) \# L2 (leaver-still-paid / joiner-not-paid / onboarding-incomplete)  
sor = locate(cause) \# HCM \| Payroll \| Identity  
opts = options(cause, policy) \# L2 (stop pay+revoke / off-cycle / complete tasks)  
rec = recommend(cause,sor,opts) \# L2  
escalate_to(HR Ops / IT); on approve: commit(sor); validate() \# human gate  
close_and_learn(case) \# L0 -\> Enterprise Memory

### Skills

SKILL_lifecycle-integrity.md - tools: Python (tested: hr_lifecycle_core.py — test_hr_other_cores.py); Joiner-to-pay / leaver-to-pay integrity check.

## 6.2 Learning & Skills Agent

| **Agent ID** | **HR-ETG-001**                                          |
|--------------|---------------------------------------------------------|
| Capability   | Continuous Workforce Development                        |
| Domain       | HR                                                      |
| Owner        | HRBP + CLO / L&D                                        |
| Tech owner   | TBD - not yet assigned                                  |
| Criticality  | TBD (build-next)                                        |
| Risk         | TBD                                                     |
| Autonomy     | L1-L3 (proposed)                                        |
| Runtime      | Python (build-next)                                     |
| Model        | TBD - none selected yet                                 |
| Skills file  | SKILL_talent.md (build-next)                            |
| Version      | proposed                                                |
| Status       | build-next                                              |
| Deployment   | TBD - see Enterprise AI Platform Reference Architecture |

### Data schema

Canonical schema to be defined at build (build-next). Draft entities: skills / capability_demand; workers; agents (performance).

### Systems of record

Skills taxonomy / HCM; LMS (build-next). Write-back: proposed -\> approved (HRBP + CLO / L&D) -\> committed -\> confirmed -\> evidenced.

### Generic agent script

on planning OR skills change:  
for cap in capabilities:  
gap = skills_gap(demand, supply) \# L2 deterministic  
route = dev_route(gap, agentifiable) \# upskill\|blended\|deploy-agent\|hire  
escalate_to(HRBP + CLO/L&D); on approve: assign_development() \# ratings/promotions human  
close_and_learn(case)

### Skills

tools: skills_gap · dev_route; skills_gap.

## 6.3 Workforce-Intelligence Copilot

| **Agent ID** | **HR-PTO-002**                                          |
|--------------|---------------------------------------------------------|
| Capability   | Optimised Business Partnering                           |
| Domain       | HR                                                      |
| Owner        | Reward + HRBP                                           |
| Tech owner   | TBD - not yet assigned                                  |
| Criticality  | TBD (build-next)                                        |
| Risk         | TBD                                                     |
| Autonomy     | L1-L3 (proposed)                                        |
| Runtime      | Python (build-next)                                     |
| Model        | TBD - none selected yet                                 |
| Skills file  | SKILL_reward.md (build-next)                            |
| Version      | proposed                                                |
| Status       | build-next                                              |
| Deployment   | TBD - see Enterprise AI Platform Reference Architecture |

### Data schema

Canonical schema to be defined at build (build-next). Draft entities: workers; capability_demand; scenarios; cost.

### Systems of record

HCM compensation / Reward analytics (build-next). Write-back: proposed -\> approved (Reward + HRBP) -\> committed -\> confirmed -\> evidenced.

### Generic agent script

on reward review OR leader question:  
for grp in comparison_groups:  
gap = pay_equity(grp.a, grp.b) \# L2 deterministic  
if gap \> threshold: pack = evidence_pack(grp, gap) \# decision-ready, cited  
escalate_to(Reward + HRBP) \# no autonomous pay decision  
on decide: record(rationale, approval_trail); close_and_learn(case)

### Skills

tools: pay_equity · evidence_pack; pay_equity.

## 6.4 Employee Service + ER/IR Intake Agents

| **Agent ID** | **HR-MTS-001/002** |
|----|----|
| Capability | Employee Service & Case Resolution |
| Domain | HR |
| Owner | HR Operations |
| Tech owner | TBD — not yet assigned |
| Criticality | Tier 2 |
| Risk | Low |
| Autonomy | L3 — Augmented+ (auto-resolves bounded self-service; ER & non-standard to a human) |
| Runtime | Python (tested reference implementation) |
| Model | TBD — no model selected yet |
| Skills file | SKILL_employee-service.md |
| Version | v1.0 (tested) |
| Status | core built & tested |
| Deployment | TBD — see Enterprise AI Platform Reference Architecture; not yet a client decision |

### Data schema

**Case** *(cases.json)*

| **Field**       | **Type** | **Description**     |
|-----------------|----------|---------------------|
| case_id         | string   | PK                  |
| worker_id       | string   | FK → Worker         |
| stream          | string   | service \| er       |
| category        | string   | topic               |
| priority        | string   | low\|medium\|high   |
| sla_hours       | int      |                     |
| age_hours       | int      |                     |
| channel         | string   | portal\|chat\|phone |
| auto_resolvable | bool     |                     |

**ERCase** *(er_cases.json)*

| **Field** | **Type** | **Description**                            |
|-----------|----------|--------------------------------------------|
| case_id   | string   | PK                                         |
| worker_id | string   | FK → Worker                                |
| risk_type | string   | grievance\|disciplinary\|wellbeing         |
| severity  | string   | low\|medium\|high                          |
| status    | string   |                                            |
| note      | string   | triaged for union/psychosocial/legal flags |

### Systems of record

HR knowledge base; case & ER systems. Write-back: proposed -\> approved (HR Operations / ER Specialist) -\> committed -\> confirmed -\> evidenced.

### Generic agent script

on case at front door:  
d = triage_case(case, policy) \# L3/L1 classify  
if d == auto_resolve: respond_from_playbook(); close() \# L3 auto (grounded, cited)  
elif d == route_human: assign(HR advisor) \# L1  
elif d == escalate_er:  
rc = er_triage(case) \# L1 risk + flags  
assign(ER specialist); retrieve_policy(); draft_timeline() \# assist only  
close_and_learn(case)

### Skills

SKILL_employee-service.md - tools: Python (tested: hr_service_desk_core.py — test_hr_other_cores.py); Deterministic SLA & triage; Grounded response drafting.

## 6.5 Workforce Shaping Agent

| **Agent ID** | **HR-PTO-001** |
|----|----|
| Capability | Total Workforce Shaping & Planning |
| Domain | HR |
| Owner | CHRO / Workforce Strategy |
| Tech owner | TBD — not yet assigned |
| Criticality | Tier 1 — strategic |
| Risk | Low |
| Autonomy | L2 — Augmented (models & recommends; org-design decisions human-led) |
| Runtime | Python (tested reference implementation) |
| Model | TBD — no model selected yet |
| Skills file | SKILL_workforce-shaping.md |
| Version | v1.0 (tested) |
| Status | core built & tested |
| Deployment | TBD — see Enterprise AI Platform Reference Architecture; not yet a client decision |

### Data schema

**Worker** *(workers.json)*

| **Field** | **Type** | **Description**             |
|-----------|----------|-----------------------------|
| worker_id | string   | PK                          |
| type      | string   | employee\|contingent\|agent |
| fte       | number   |                             |
| skills    | list     |                             |

**Position** *(positions.json)*

| **Field**    | **Type** | **Description** |
|--------------|----------|-----------------|
| position_id  | string   | PK              |
| job_id       | string   | FK → Job        |
| org_id       | string   | FK → OrgUnit    |
| budgeted_fte | number   | establishment   |
| status       | string   | filled\|vacant  |

**CapabilityDemand** *(capability_demand.json)*

| **Field**        | **Type** | **Description**               |
|------------------|----------|-------------------------------|
| capability       | string   |                               |
| demand_fte       | number   |                               |
| supply_fte       | number   |                               |
| agentifiable_pct | number   | ceiling on agent substitution |
| avg_cost_human   | number   |                               |
| avg_cost_agent   | number   |                               |

### Systems of record

Workforce plan / establishment (Finance EPM). Write-back: proposed -\> approved (CHRO / Workforce Strategy) -\> committed -\> confirmed -\> evidenced.

### Generic agent script

on planning cycle OR demand/supply change:  
mix = workforce_mix(workers) \# human/contingent/agent  
gaps = capability_gaps(demand, supply) \# L2  
for g in gaps:  
sc = agentify_scenario(g, costs, shift) \# L2 economics  
dec = resource_decision(g.agentifiable, g.clinical) \# agent/blended/human  
escalate_to(CHRO/Workforce Strategy + Finance); on approve: post_establishment(EPM)  
close_and_learn(case)

### Skills

SKILL_workforce-shaping.md - tools: Python (tested: hr_workforce_shaping_core.py — test_hr_other_cores.py); Deterministic mix, gap & scenario maths; ISO 30414 metric calculator.

## 6.6 Payroll Assurance Agent

| **Agent ID** | **HR-RTP-001** |
|----|----|
| Capability | Payroll Assurance |
| Domain | HR |
| Owner | Payroll Controller |
| Tech owner | TBD — not yet assigned |
| Criticality | Tier 1 — pay is legally and reputationally critical |
| Risk | Medium |
| Autonomy | L3 — Augmented+ (auto-detects & explains within policy; corrections human-approved) |
| Runtime | Python (tested reference implementation) |
| Model | TBD — no model selected yet |
| Skills file | SKILL_payroll-assurance.md |
| Version | v1.0 (tested) |
| Status | core built & tested |
| Deployment | TBD — see Enterprise AI Platform Reference Architecture; not yet a client decision |

### Data schema

**Worker** *(workers.json / HCM worker master)*

| **Field** | **Type** | **Description**                 |
|-----------|----------|---------------------------------|
| worker_id | string   | PK                              |
| type      | string   | employee \| contingent \| agent |
| status    | string   | active \| onboarding \| leaver  |
| hire_date | date     |                                 |
| term_date | date     | null unless leaver              |
| pay_group | string   | MONTHLY \| WEEKLY               |

**PayItem** *(payroll_current.json / payroll_prior.json)*

| **Field**      | **Type** | **Description**              |
|----------------|----------|------------------------------|
| worker_id      | string   | FK → Worker                  |
| gross          | number   | base+allowances+overtime     |
| tax            | number   | PAYE                         |
| ni             | number   | National Insurance           |
| tax_code       | string   | HMRC; blank = anomaly        |
| ni_category    | string   | NI letter (A/B/…)            |
| pension        | number   | auto-enrolment contribution  |
| rti_status     | string   | RTI submission state         |
| net            | number   | gross less deductions        |
| approved_by    | string   | blank + changed = unapproved |
| changed_fields | list     | fields changed this period   |

**TimeRecord** *(time.json)*

| **Field**        | **Type** | **Description** |
|------------------|----------|-----------------|
| worker_id        | string   | FK → Worker     |
| contracted_hours | number   |                 |
| worked_hours     | number   |                 |
| absence_days     | number   |                 |

### Systems of record

HCM + Payroll + Time + Benefits + Identity + GL. Write-back: proposed -\> approved (Payroll Controller) -\> committed -\> confirmed -\> evidenced.

### Generic agent script

on pay run (pre sign-off):  
reg = detect_anomalies(current, prior, workers) \# L3 detect - 7 checks  
risk = risk_score(reg)  
for a in reg:  
cause = classify_pay_anomaly(a) \# L2 diagnose  
sor = locate_source(cause) \# HCM\|Payroll\|Time\|Benefits  
opts = options(cause, policy, tolerance) \# L2  
impact = calc_impact(a, opts) \# recalc, GL, comms, tax  
rec = recommend(cause, sor, opts, impact) \# L2  
if within_tolerance(rec): commit(sor); validate() \# L3 auto (duplicate/negative-net)  
else: escalate_to(Payroll Controller); on approve: commit(sor); validate() \# human + SoD  
close_and_learn(case) \# L0 -\> Enterprise Memory

### Skills

SKILL_payroll-assurance.md - tools: Python (tested: hr_payroll_assurance_core.py, 12 passing tests); Deterministic anomaly detection & risk score; Explain-pay breakdown; Audit-evidence assembler.

## 6.7 AgentOps Control Tower

| **Agent ID** | **HR-GOV-001** |
|----|----|
| Capability | AI Governance / AgentOps |
| Domain | HR |
| Owner | HR Governance Lead |
| Tech owner | TBD — not yet assigned |
| Criticality | Tier 1 — control plane |
| Risk | Low |
| Autonomy | L2 — Augmented (monitors & flags; kill-switch & shutdowns human-confirmed) |
| Runtime | Python (tested reference implementation) |
| Model | TBD — no model selected yet |
| Skills file | SKILL_hr-agentops.md |
| Version | v1.0 (tested) |
| Status | core built & tested |
| Deployment | TBD — see Enterprise AI Platform Reference Architecture; not yet a client decision |

### Data schema

**AgentReg** *(agents.json)*

| **Field**   | **Type** | **Description**       |
|-------------|----------|-----------------------|
| agent_id    | string   | PK                    |
| name        | string   |                       |
| domain      | string   | HR\|Finance\|O2C      |
| agent_class | string   |                       |
| status      | string   | run\|idle\|esc        |
| cost        | number   | GBP                   |
| tokens      | int      |                       |
| drift       | bool     |                       |
| sod_ok      | bool     | segregation of duties |
| escalation  | string   |                       |

### Systems of record

Agent registry / model cards. Write-back: proposed -\> approved (AI Governance / AgentOps Lead) -\> committed -\> confirmed -\> evidenced.

### Generic agent script

continuous across fleet:  
s = fleet_summary(agents); meter = fleet_meter(cost, runs) \# L0 observe  
sod = sod_check(agents); cov = compliance_coverage(agents)  
for a in agents:  
if a.drift: rec = tune\|restrict\|retire \# L2 recommend  
else: certify(a) \# L3 within policy  
if consequential(rec): escalate_to(Governance Lead) \# onboarding/scope/retire  
commit(registry); validate(); close_and_learn(case)

### Skills

SKILL_hr-agentops.md - tools: Python (tested: hr_agentops_core.py — test_hr_other_cores.py); Fleet summary & governance alerts across domains.

# 7. Agent collaboration matrix

| **Agent** | **Delegates / signals to** | **Consumes from** | **Escalates to (human)** |
|----|----|----|----|
| Payroll Assurance | Onboarding & Lifecycle; GL; AgentOps | HCM, Payroll, Time, Benefits | Payroll Controller |
| Onboarding & Lifecycle | Identity/IT; Payroll | HCM, events, payroll, access | HR Ops + IT |
| Workforce Shaping | AgentOps; Finance EPM | workers, demand, unit costs | CHRO / Workforce Strategy + Finance |
| Employee Service | ER/IR Intake | case queue, knowledge base | HR advisor |
| ER/IR Intake | \- | ER cases, policy, law | ER specialist / counsel |
| Learning & Skills | AgentOps (agent tuning) | skills taxonomy, LMS | HRBP + CLO/L&D |
| Workforce-Intelligence Copilot | \- | analytics, comp, policy | Reward + HRBP |
| AgentOps Control Tower | all agents (govern) | agent registry (HR/Finance/O2C) | Governance Lead |

# 8. Build sequencing

## 8.1 Foundational dependencies (build first)

- Canonical Workforce data model + connectors to the client HCM and payroll (systems of record).

- Workforce knowledge graph and the AgentOps registry / audit-trail store.

- The deterministic-core / LLM boundary and the shared decision-cycle orchestration (Azure Durable Functions).

## 8.2 Build-now (tested cores exist)

- Payroll Assurance (hr_payroll_assurance_core.py, 12 tests)

- Workforce Shaping (hr_workforce_shaping_core.py)

- Employee Service + ER/IR Intake (hr_service_desk_core.py, hr_er_intake_core.py)

- Onboarding & Lifecycle (hr_lifecycle_core.py)

- AgentOps Control Tower + ISO coverage (hr_agentops_core.py, hr_iso_core.py)

## 8.3 Build-next

- Total Rewards / pay-equity (highest-value white space; EU Pay Transparency driver)

- Talent design / performance / succession (Section 2 capability)

- Time & attendance / scheduling and Learning operations (Section 6 stream)

- Separation / offboarding / alumni; contingent-labour integration

## 8.4 Deferred (and why)

- Persistent agent memory - platform-wide capability, not built in any domain yet.

- Full workforce digital twin and autonomous scheduling - require data foundations and higher assurance maturity.
