**KPMG**

**Payroll Assurance Agent**

**STAGE 6A - UPDATED DETAILED COMPONENT DESIGN**

*Component, control, handover and unit-test specification aligned to Stage 4 v2*

| **Document control** | **Details** |
|----|----|
| Version | Draft v2.0 |
| Status | Draft for SME and Factory Design Authority review |
| Updated reference | Payroll_Assurance_Agent_Stage_4_Classify_Capability_Based (2).docx |
| Owner persona | Payroll Controller |
| Business capability | Continuous Payroll Assurance |
| Classification | KPMG Confidential |

Primary update source: uploaded Stage 4 v2 capability-based model, including updated workflow ownership, handovers, control points and ABBA reuse assessment.

# Executive Summary

This updated Stage 6A design replaces the earlier Stage 6 baseline wherever the uploaded Stage 4 v2 changes agent ownership, handovers, controls or reuse decisions. The nine capability-agent model remains the design basis. The important updates are: ABBA is now fully assessed; A08 is mapped to W18-W20 in the workflow table; the Payroll Exception Processing Agent has a handover to the Onboarding & Lifecycle Agent for leaver-still-paid and joiner-not-paid cases; and several reusable validation/recalculation assets are now identified for adaptation.

| **Design authority issue** The updated Stage 4 assigns W20 to A08 in the workflow mapping, while CP10 names A02 as the owning agent. Stage 6A preserves both facts and requires a single accountability decision before build. |
|----|

# 1. Updated Stage 4 Design Baseline

| **ID** | **Agent** | **Class** | **Updated coverage** | **Stage 6A responsibility** |
|:--:|----|----|----|----|
| A01 | Payroll Assurance Workspace Agent | Experience | W13-W14 | Review, evidence access and decision capture |
| A02 | Payroll Assurance Orchestrator | Orchestration | W12, W15; case state across workflow | Routing, escalation, commit coordination and state |
| A03 | Payroll Data Management Agent | Task | W01, W16 | Data collection and recalculation |
| A04 | Payroll Exception Processing Agent | Task | W03, W09 | Anomaly detection and correction options |
| A05 | Payroll Analysis Agent | Insight | W04-W08 | Risk, classification, explanation, diagnosis and source location |
| A06 | Payroll Decision Intelligence Agent | Insight | W10-W11 | Impact and recommendation |
| A07 | Payroll Quality Control Agent | Control | W02, W17 | Input and post-correction validation |
| A08 | Payroll Governance & Audit Agent (AgentOps) | Control | W18-W20 | Audit evidence, governance logs and Stage 4 workflow closure |
| A09 | Human Approval Control Agent | Control | W13-W15 | Human approval, SoD and period sign-off |

## 1.1 Change impact from the previous Stage 6 design

| **Change** | **Stage 6A treatment** |
|----|----|
| ABBA previously treated as open/provisional | Replace with updated asset-level reuse decisions: Adapt, New Design or Not Suitable. |
| W20 ownership differs | Record A08 as Stage 4 workflow owner and A02 as CP10 owner; resolve through RACI/Design Authority decision. |
| Onboarding & Lifecycle handover introduced | Add external/cross-capability handover for joiner-not-paid and leaver-still-paid anomalies. |
| A08 explicitly labelled AgentOps | Design audit/governance behaviour and technical-operational evidence separation. |
| A09 includes payroll-period sign-off | Expand human-control design and tests to cover period sign-off evidence. |
| Seven anomaly classes made explicit | Use the seven listed classes as the minimum deterministic test catalogue. |

# 2. Updated End-to-End Workflow Design

<table>
<colgroup>
<col style="width: 6%" />
<col style="width: 17%" />
<col style="width: 19%" />
<col style="width: 28%" />
<col style="width: 27%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Step</strong></th>
<th style="text-align: center;"><strong>Activity</strong></th>
<th style="text-align: center;"><strong>Owner</strong></th>
<th style="text-align: center;"><strong>Key input</strong></th>
<th style="text-align: center;"><strong>Key output</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;">W01</td>
<td>Collect Payroll Data</td>
<td>A03</td>
<td>Payroll run scope; payroll/HCM/time/absence/benefits/policy/statutory data</td>
<td>Consolidated payroll assurance dataset</td>
</tr>
<tr>
<td style="text-align: center;">W02</td>
<td>Validate Input Data</td>
<td>A07</td>
<td>Consolidated dataset; completeness rules</td>
<td>Data quality result and gap list</td>
</tr>
<tr>
<td style="text-align: center;">W03</td>
<td>Detect Anomalies</td>
<td>A04</td>
<td>Validated dataset; approved anomaly rules</td>
<td>Anomaly register</td>
</tr>
<tr>
<td style="text-align: center;">W04</td>
<td>Calculate Risk Score</td>
<td>A05</td>
<td>Anomaly register; risk factors</td>
<td>Risk score and band</td>
</tr>
<tr>
<td style="text-align: center;">W05</td>
<td>Classify Anomaly</td>
<td>A05</td>
<td>Anomaly and <span class="comment-start" id="0" data-author="Kalimuthu, Karthik" data-date="2026-08-24T15:56:00Z">Need clarification</span>taxonomy<span class="comment-end" id="0"></span></td>
<td>Classified exception</td>
</tr>
<tr>
<td style="text-align: center;">W06</td>
<td>Explain Payroll Calculation</td>
<td>A05</td>
<td>Pay calculation trace and policy evidence</td>
<td>Calculation explanation with citations</td>
</tr>
<tr>
<td style="text-align: center;">W07</td>
<td>Determine Root Cause</td>
<td>A05</td>
<td>Anomaly, explanation and source variances</td>
<td>Root-cause assessment</td>
</tr>
<tr>
<td style="text-align: center;">W08</td>
<td>Locate System of Record</td>
<td>A05</td>
<td>Root cause and lineage</td>
<td>Source-system <span class="comment-start" id="1" data-author="Gale, Philip" data-date="1900-01-01T00:00:00Z"><a href="mailto:Ezekiel.Ibegbunam@kpmg.co.uk">@Ibegbunam, Ezekiel</a> <a href="mailto:Nick.Phillips@kpmg.co.uk">@Phillips, Nick</a><br />
In answer to<br />
Q: Determine whether root-cause visibility from upstream payroll processes is sufficiently represented<br />
PG Response: There is mention of identifying the source system and record (W8) but unlcear if W7 fully identifes root cause that the upstream or originating business process/control failure/missing human actions that causes anomaly<br />
e.g, Does it take into account failure types and process area including - incorrect or missing manager approvals, missed onboarding/offboarding activities, time-entry errors, benefits administration / HR master data issues</span>reference<span class="comment-end" id="1"></span></td>
</tr>
<tr>
<td style="text-align: center;">W09</td>
<td>Generate Correction Options</td>
<td>A06</td>
<td>Root cause, source system, policy and tolerance</td>
<td>Correction options</td>
</tr>
<tr>
<td style="text-align: center;">W10</td>
<td>Assess Impact</td>
<td>A06</td>
<td>Options; pay/tax/pension/GL/employee context</td>
<td>Impact assessment</td>
</tr>
<tr>
<td style="text-align: center;">W11</td>
<td>Create Recommendation</td>
<td>A06</td>
<td>Impact and evidence</td>
<td>Recommended action and rationale</td>
</tr>
<tr>
<td style="text-align: center;">W12</td>
<td>Escalate for Approval</td>
<td>A02</td>
<td>Recommendation package</td>
<td>Approval case</td>
</tr>
<tr>
<td style="text-align: center;">W13</td>
<td><span class="comment-start" id="4" data-author="Kalimuthu, Karthik" data-date="2026-08-25T11:25:00Z">Verify these steps with Neil &amp; Phil</span>Review Recommendation</td>
<td>A01 + A09<span class="comment-end" id="4"></span></td>
<td>Approval case, evidence and authority context</td>
<td>Review outcome</td>
</tr>
<tr>
<td style="text-align: center;">W14</td>
<td>Approve, Reject or Escalate</td>
<td>A01 + A09</td>
<td>Review outcome and human decision</td>
<td>ApprovalDecision / rework / escalation</td>
</tr>
<tr>
<td style="text-align: center;">W15</td>
<td>Commit Correction</td>
<td>A02 + A09</td>
<td>Approved correction and SoD result</td>
<td>Commit instruction and write-back receipt</td>
</tr>
<tr>
<td style="text-align: center;">W16</td>
<td>Recalculate Payroll</td>
<td>A03</td>
<td>Committed correction</td>
<td>Recalculated payroll result</td>
</tr>
<tr>
<td style="text-align: center;">W17</td>
<td>Validate Outcome</td>
<td>A07</td>
<td>Original anomaly; recalculated result</td>
<td>ValidationResult / rework route</td>
</tr>
<tr>
<td style="text-align: center;">W18</td>
<td>Create Audit Evidence</td>
<td>A08</td>
<td>Case history, decision, correction, validation</td>
<td>Audit evidence pack</td>
</tr>
<tr>
<td style="text-align: center;">W19</td>
<td>Log Governance Actions</td>
<td>A08</td>
<td>Actions, decisions, versions and evidence</td>
<td>Governance log</td>
</tr>
<tr>
<td style="text-align: center;">W20</td>
<td>Close Case</td>
<td>A08 per updated Stage 4 workflow mapping; CP10 accountability requires resolution</td>
<td>Audit pack, logs, open-action status</td>
<td>Closed case or open exception</td>
</tr>
</tbody>
</table>

## 2.1 Cross-capability lifecycle handover

Where A04 detects “leaver still paid” or “joiner not paid”, the updated Stage 4 handover matrix routes the identified lifecycle issue to the Onboarding & Lifecycle Agent. Stage 6A treats this as an external capability handover rather than a tenth Payroll Assurance agent. The handover must include case, worker, lifecycle event, payroll run, anomaly type, evidence, expected response and return route.

# 3. Updated Agent Handover Contract

| **From** | **To** | **Required payload** | **Expected evidence** |
|:--:|----|----|----|
| A01 Workspace | A02 Orchestrator | User request, payroll run, approval action | Case initiated or decision captured |
| A02 | A03 | Data request and payroll scope | Consolidated dataset |
| A03 | A07 | Payroll/workforce dataset and source context | DQ result and gap list |
| A07 | A04 | Validated dataset and control status | Anomaly register |
| A04 | A05 | Anomaly register and rule evidence | Risk/classification/explanation/root cause |
| A04 | Onboarding & Lifecycle Agent | Lifecycle anomaly, worker and event evidence | Lifecycle investigation/result and return status |
| A05 | A06 | Classified anomaly, explanation, root cause and lineage | Impact and recommendation |
| A06 | A02 | Recommendation, impact, rationale and evidence | Approval required |
| A02 | A09/A01 | Approval case and permitted decisions | Human decision and rationale |
| A09 | A02/A03 | Approved/rejected/escalated state and authority evidence | Commit/rework/close route |
| A03 | A07 | Approved correction, recalculation and receipt | Validation result |
| A07 | A08 | Validation and correction evidence | Audit pack and governance log |
| A08 | A02 or closure service | Evidence completeness, logs and open-action state | Closed case or open exception |

# 4. Component Behaviour Specifications

## A01 Payroll Assurance Workspace Agent

| **Aspect** | **Specification** |
|:--:|----|
| Class and purpose | **Experience**. User-facing review, evidence and approval workspace. (**Experience**; W13-W14.) |
| Trigger | User opens workspace or receives an assigned review |
| Core behaviour | Payroll Controller review and decision capture. Validate input contract, execute only permitted operations, persist output, attach evidence and return explicit next state. |
| Decision boundary | Do not infer missing payroll facts. Do not bypass failed controls. Consequential action is blocked unless authorised approval exists. |
| Failure behaviour | Return structured error with category, evidence of failure, retry eligibility, owner and safe next state. |
| Audit fields | case_id, execution_id, actor/service identity, input/output version, event time, rule/model/prompt version and evidence reference. |

## A02 Payroll Assurance Orchestrator

| **Aspect** | **Specification** |
|----|----|
| Class and purpose | **Orchestration**. Coordinates end-to-end case state, routing, escalation and closure.(W12, W15; case state across workflow.) |
| Trigger | New case, completed handover, timeout or control event |
| Core behaviour | State transitions and traceable handovers. Validate input contract, execute only permitted operations, persist output, attach evidence and return explicit next state. |
| Decision boundary | Do not infer missing payroll facts. Do not bypass failed controls. Consequential action is blocked unless authorised approval exists. |
| Failure behaviour | Return structured error with category, evidence of failure, retry eligibility, owner and safe next state. |
| Audit fields | case_id, execution_id, actor/service identity, input/output version, event time, rule/model/prompt version and evidence reference. |

## A03 Payroll Data Management Agent

| **Aspect** | **Specification** |
|----|----|
| Class and purpose | **Task**. Collects and consolidates payroll/workforce data; supports recalculation. (W01, W16) |
| Trigger | Data collection or approved recalculation request |
| Core behaviour | Trusted run dataset and recalculated output. Validate input contract, execute only permitted operations, persist output, attach evidence and return explicit next state. |
| Decision boundary | Do not infer missing payroll facts. Do not bypass failed controls. Consequential action is blocked unless authorised approval exists. |
| Failure behaviour | Return structured error with category, evidence of failure, retry eligibility, owner and safe next state. |
| Audit fields | case_id, execution_id, actor/service identity, input/output version, event time, rule/model/prompt version and evidence reference. |

## A04 Payroll Exception Processing Agent

| **Aspect** | **Specification** |
|----|----|
| Class and purpose | **Task**. Runs approved anomaly rules and creates correction options. (W03, W09) |
| Trigger | Validated dataset available or rework requested |
| Core behaviour | Anomaly detection and resolution options. Validate input contract, execute only permitted operations, persist output, attach evidence and return explicit next state. |
| Decision boundary | Do not infer missing payroll facts. Do not bypass failed controls. Consequential action is blocked unless authorised approval exists. |
| Failure behaviour | Return structured error with category, evidence of failure, retry eligibility, owner and safe next state. |
| Audit fields | case_id, execution_id, actor/service identity, input/output version, event time, rule/model/prompt version and evidence reference. |

## A05 Payroll Analysis Agent

| **Aspect** | **Specification** |
|----|----|
| Class and purpose | **Insight**. Scores risk, classifies, explains and diagnoses root cause. (W04-W08) |
| Trigger | Anomaly registered |
| Core behaviour | Risk, classification, explanation and root cause. Validate input contract, execute only permitted operations, persist output, attach evidence and return explicit next state. |
| Decision boundary | Do not infer missing payroll facts. Do not bypass failed controls. Consequential action is blocked unless authorised approval exists. |
| Failure behaviour | Return structured error with category, evidence of failure, retry eligibility, owner and safe next state. |
| Audit fields | case_id, execution_id, actor/service identity, input/output version, event time, rule/model/prompt version and evidence reference. |

## A06 Payroll Decision Intelligence Agent

| **Aspect** | **Specification** |
|----|----|
| Class and purpose | **Insight**. Assesses impact and creates evidence-backed recommendation. (W10-W11) |
| Trigger | Root cause and correction options available |
| Core behaviour | Impact assessment and recommendation. Validate input contract, execute only permitted operations, persist output, attach evidence and return explicit next state. |
| Decision boundary | Do not infer missing payroll facts. Do not bypass failed controls. Consequential action is blocked unless authorised approval exists. |
| Failure behaviour | Return structured error with category, evidence of failure, retry eligibility, owner and safe next state. |
| Audit fields | case_id, execution_id, actor/service identity, input/output version, event time, rule/model/prompt version and evidence reference. |

## A07 Payroll Quality Control Agent

| **Aspect** | **Specification** |
|----|----|
| Class and purpose | **Control**. Validates input completeness and post-correction outcome. (W02, W17) |
| Trigger | Dataset or recalculation ready for control |
| Core behaviour | Control results, breaks and remediation route. Validate input contract, execute only permitted operations, persist output, attach evidence and return explicit next state. |
| Decision boundary | Do not infer missing payroll facts. Do not bypass failed controls. Consequential action is blocked unless authorised approval exists. |
| Failure behaviour | Return structured error with category, evidence of failure, retry eligibility, owner and safe next state. |
| Audit fields | case_id, execution_id, actor/service identity, input/output version, event time, rule/model/prompt version and evidence reference. |

## A08 Payroll Governance & Audit Agent

| **Aspect** | **Specification** |
|----|----|
| Class and purpose | **Control**. Creates evidence packs, decision logs and lineage. (W18-W20) |
| Trigger | Material case event or evidence assembly request |
| Core behaviour | Immutable audit evidence and governance record. Validate input contract, execute only permitted operations, persist output, attach evidence and return explicit next state. |
| Decision boundary | Do not infer missing payroll facts. Do not bypass failed controls. Consequential action is blocked unless authorised approval exists. |
| Failure behaviour | Return structured error with category, evidence of failure, retry eligibility, owner and safe next state. |
| Audit fields | case_id, execution_id, actor/service identity, input/output version, event time, rule/model/prompt version and evidence reference. |

## A09 Human Approval Control Agent

| **Aspect** | **Specification** |
|----|----|
| Class and purpose | **Control**. Enforces human authority, SoD and decision capture. (W13-W15) |
| Trigger | Decision-ready recommendation submitted |
| Core behaviour | Approval, rejection or escalation decision. Validate input contract, execute only permitted operations, persist output, attach evidence and return explicit next state. |
| Decision boundary | Do not infer missing payroll facts. Do not bypass failed controls. Consequential action is blocked unless authorised approval exists. |
| Failure behaviour | Return structured error with category, evidence of failure, retry eligibility, owner and safe next state. |
| Audit fields | case_id, execution_id, actor/service identity, input/output version, event time, rule/model/prompt version and evidence reference. |

# 5. Data Mapping and Stage 5B Alignment (Silver Entity)

| <span class="comment-start" id="5" author="Ibegbunam, Ezekiel" date="2026-08-25T16:08:00Z">Subject to the Gold layer data model for the inputs and outputs</span>**Agent** | **Stage 5B inputs** | **Stage 5B outputs** |
|:--:|----|----|
| A01 | AssuranceCase, PayrollAnomaly, PayrollRisk, AuditEvidence | ApprovalDecision, comments, escalation choice |
| A02 | AssuranceCase, AgentExecution, control results | State transition, routing event, commit/closure instruction |
| A03 | Worker, PayrollRun, PayItem, TimeRecord, BenefitsRecord, LifecycleEvent | Source snapshot, PayrollCalculation, write-back/recalculation receipt |
| A04 | Validated snapshot, PayrollPolicy, DataQualityRule | PayrollAnomaly, PayrollException, correction options |
| A05 | PayrollAnomaly, PayrollCalculation, PayrollPolicy, DataLineageRecord | PayrollRisk, explanation, RootCauseAssessment, source reference |
| A06 | RootCauseAssessment, options, Tax/Pension/GL context | Impact assessment, recommendation, evidence references |
| A07 | Source snapshot or recalculated output; DataQualityRule | Control result, gap list, ValidationResult |
| A08 | Case events, decisions, versions, receipts and validation | AuditEvidence, DataLineageRecord, evidence manifest, governance log, closure status |
| A09 | Recommendation, ApprovalDecision context, IdentityAccount | ApprovalDecision, SoD result, period sign-off evidence<span class="comment-end" id="5"></span> |

# 6. Deterministic Logic and Seven-Anomaly Catalogue

<table>
<colgroup>
<col style="width: 28%" />
<col style="width: 71%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><strong>Rule area</strong></th>
<th style="text-align: center;"><strong>Updated deterministic requirement</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Leaver still paid</td>
<td>Termination date precedes period end and p<span class="comment-start" id="6" data-author="Kluck, Saskia" data-date="2026-08-25T15:12:00Z">to confirm with SME if tolerance should always be 0</span><span class="comment-start" id="7" data-author="Gale, Philip" data-date="2026-09-01T12:17:00Z">There may be instances when holiday pay, benefit refunds, PAYE etc may be paid after last pay date so tolerance would be above zero for non-pay specific categories <a href="mailto:Nick.Phillips@kpmg.co.uk">@Phillips, Nick</a> Thoughts?</span><span class="comment-start" id="8" data-author="Phillips, Nick" data-date="2026-09-01T14:51:00Z">Phil’s spot on. Zero tolerance for any post-termination pay would generate false positives every pay run — holiday pay, PAYE refunds, and other one-off adjustments are routine.<br />
The rule should distinguish <strong>payment type</strong>, not just amount:<br />
<strong>Recurring/basic pay after termination</strong> → anomaly at zero tolerance<br />
<strong>One-off statutory/refund components</strong> → exempt, or flagged separately with a higher tolerance/materiality threshold<br />
That keeps the “no invented default” principle intact without treating legitimate leaver payments as errors. Worth updating the anomaly catalogue (section 6) to reflect this.</span>ay remains above approved toleranc<span class="comment-end" id="6"><span class="comment-end" id="7"><span class="comment-end" id="8"></span></span></span>e; lifecycle evidence required.</td>
</tr>
<tr>
<td>Joiner not paid</td>
<td>Expected eligible payment exists but no payroll result is present; lifecycle and pay-period evidence required.</td>
</tr>
<tr>
<td><span class="comment-start" id="11" data-author="Ibegbunam, Ezekiel" data-date="2026-08-25T16:25:00Z">Needs confirmation from SME to understand the metric behind the percentage</span><span class="comment-start" id="12" data-author="Gale, Philip [2]" data-date="2026-09-01T10:29:00Z"><a href="mailto:Nick.Phillips@kpmg.co.uk">@Phillips, Nick</a> commented on the call that there is no recognised industry-standard.<br />
Suggest 45% could be retained as a placeholder pending confirmation of a known client example.</span><span class="comment-start" id="13" data-author="Phillips, Nick [2]" data-date="2026-09-01T14:57:00Z">@Gale, Philip yes, that’s right.</span><span class="comment-start" id="14" data-author="Hicks, Paula" data-date="2026-09-09T15:03:00Z">The % would need to be configurable at individual client level</span>Unexplained 45% variance</td>
<td>Apply the approved variance rule and comparison basis; the Stage 4 reference uses 45% as an in-scope anomaly label.<span class="comment-end" id="11"><span class="comment-end" id="12"><span class="comment-end" id="13"><span class="comment-end" id="14"></span></span></span></span></td>
</tr>
<tr>
<td><span class="comment-start" id="16" data-author="Hicks, Paula" data-date="2026-09-09T15:08:00Z">Can this be changed to missing mandatory item that can be flagged? The majority of payroll systems will pick up a missing mandatory item that is needed for tax calculations, apply a default. What typically causes more problems is other items that are mandatory for tax filings, that a HR system might not send i.e. gender, and will cause a file to fail, or even things like postcodes that cause pension files to fail, costcodes causing GL files to fail</span>Missing tax code</td>
<td>Detect missing required tax code; route as controlled statutory exposure.<span class="comment-end" id="16"></span></td>
</tr>
<tr>
<td>Negative net pay</td>
<td>Detect net pay below zero and route for urgent review.</td>
</tr>
<tr>
<td><span class="comment-start" id="17" data-author="Hicks, Paula" data-date="2026-09-09T15:09:00Z">Is this where we may have 2 x values of the same i.e. 2 bonuses, or where we have 2 worker records</span>Duplicate pay record</td>
<td>Use approved worker-period-component composite key and duplicate window.<span class="comment-end" id="17"></span></td>
</tr>
<tr>
<td><span class="comment-start" id="18" data-author="Ibegbunam, Ezekiel" data-date="2026-08-24T13:01:00Z">Subject to confirmation</span><span class="comment-start" id="19" data-author="Hicks, Paula" data-date="2026-09-09T15:16:00Z">We may need a further discussion on this. Is an example of this a salary change that hasn’t been approved, or a bonus that hasn’t been approved? If so there’d be no way to check this from payroll reports. The audit of approval is likely to sit in the HR system and not be sent to payroll, so unless you were unable to run cross database checks this wouldn’t be possible as a payroll output.</span>unapproved change<span class="comment-end" id="18"><span class="comment-end" id="19"></span></span></td>
<td>Changed payroll field lacks required approval evidence.</td>
</tr>
<tr>
<td>Variance calculation</td>
<td><span class="comment-start" id="20" data-author="Hicks, Paula" data-date="2026-09-09T15:22:00Z">Would this also highlight where an employee wasn’t paid last time, but being paid this time? I have seen instances where someone on long-term sick has had pay re-instated following a NMW or pay update,</span>current - comparison; percentage only when the comparison denominator is non-zero. (: variance = (gross - prior_gross)/prior_gross;)<span class="comment-end" id="20"></span></td>
</tr>
<tr>
<td>Gross-to-net</td>
<td>gross - deductions - tax - pension +/- approved adjustments = expected net.</td>
</tr>
<tr>
<td>Closure</td>
<td>All mandatory controls pass, no open action, decision/sign-off captured, validation and evidence complete.</td>
</tr>
</tbody>
</table>

| <span class="comment-start" id="21" author="Ibegbunam, Ezekiel" date="2026-08-25T16:40:00Z">Clarification needed for the specifications</span><span class="comment-start" id="22" author="Ibegbunam, Ezekiel" date="2026-09-02T12:30:00Z">Pay group band can be applied as the Materiality band</span>**Logic** | **Specification** | **Output / boundary** |
|----|----|----|
| Completeness | Required field count passed / required field count evaluated; blocking fields fail closed. | Pass/fail, missing fields and source snapshot. |
| Materiality | Configured threshold by legal entity/pay group/category and effective date. | Materiality band; no invented default. |
| Risk score | Versioned weighted factors: severity, financial impact, population impact, compliance exposure, recurrence, ageing and data confidence. | Factor-level explanation; weights and bands require approval. |
| SoD | Reject when preparer, approver or deployer identities conflict under active role rules. | Pass/fail, conflict rule and authority snapshot.<span class="comment-end" id="21"><span class="comment-end" id="22"></span></span> |

# 7. Updated ABBA Reuse Assessment

| **Component / workflow** | **Candidate** | **Disposition** | **Stage 6A design implication** |
|----|----|----|----|
| A03 / W01 | No suitable match | New design | Source collection and Fabric-aligned consolidation remain new. |
| A07 / W02 | VA-1246, VA-1172, VA-1279 | Adapt | Combine payroll, employee and time validation capabilities inside Quality Control. |
| A04 / W03 | VA-1149, VA-1266 | Not suitable | Compensation-anomaly scope does not match the seven in-scope payroll anomalies. |
| A05 / W04-W05 | No match | New design | Payroll-specific risk scoring and classification required. |
| A05 / W06 | VA-1267, VA-1253 | Not suitable | Experience-agent capability is not evidenced as sufficient for in-scope anomaly explanation. |
| A05 / W07-W08 | No match | New design | Payroll root cause and system-of-record location required. |
| A04 / W09 | No match | New design | Payroll correction-option generation required. |
| A06 / W10-W11 | No match | New design | Impact and recommendation logic required. |
| A02/A01/A09 / W12-W15 | No match | New design | Payroll-specific orchestration, review and approval control required. |
| A03 / W16 | VA-1145, VA-1248, VA-11343 | Adapt | Calculation capability is reusable subject to Fabric/source and correction-format fit. |
| A07 / W17 | VA-1246 | Adapt | Payroll result validation can be incorporated into Quality Control. |
| A08 / W18 | No match | New design | Audit pack assembly required. |
| A08 / W19 | VA-1304 | Not suitable | Governance monitoring is not equivalent to action and decision logging. |
| W20 closure | VA-1249, VA-1251 | Not suitable | General payroll workflow closure does not match this assurance flow. |

| **Reuse rule** Adaptation is permitted only after source, schema, rule scope, security, evidence, human boundary and unit-test fit are confirmed. “Not suitable” assets are not part of the build baseline. |
|----|

# 8. Control Operation and Evidence

| **ID** | **Control** | **Owner** | **Coverage** |
|:--:|----|----|----|
| CP01 | Input completeness | A07 | W02 |
| CP02 | Approved anomaly rule | A04 | W03 |
| CP03 | Risk and severity | A05 | W04-W05 |
| CP04 | Evidence sufficiency | A06 | W10-W11 |
| CP05 | Mandatory human approval | A09 | W13-W15 |
| CP06 | Segregation of duties | A09 | W14-W15 |
| CP07 | Post-correction validation | A07 | W17 |
| CP08 | Audit evidence completeness | A08 | W18 |
| CP09 | Governance logging | A08 | W19 |
| CP10 | Case closure | A02 in control table; A08 in workflow mapping | W20 |

## 8.1 CP10 ownership resolution

Proposed operating model for Design Authority decision: A08 attests evidence completeness and prepares the closure recommendation; A02 executes the final state transition only after CP10 confirms no open actions or incomplete evidence. This proposal reconciles the updated Stage 4 workflow mapping with the CP10 control table, but remains a design decision rather than an approved fact.

# 9. AI Instructions, Responses and Human Boundary

| **System instruction:** Use only supplied case data, deterministic calculations, effective policy, control results and cited evidence. Separate verified facts, calculations, recommendations and missing information. Never approve, commit, sign off or invent payroll values. |
|----|

## System instruction pattern

> Role: You are the Payroll Assurance explanation and recommendation component for an authorised assurance case.  
> Objective: Explain verified deterministic results and assemble a decision-ready summary.  
> Grounding: Use only supplied case data, calculation trace, effective Payroll Policy, control results and cited evidence references.  
> Rules: Never invent values, payroll policy or employee facts. Never approve, commit or sign off. Clearly separate verified facts, deterministic calculations, suggestions and missing information.  
> Output: Return the required JSON schema and a concise user narrative. Every material statement and every number must reference an evidence_id or calculation_id.  
> Failure: If evidence is missing, stale or contradictory, return INSUFFICIENT_EVIDENCE and specify the missing items and escalation route.

## 7.2 Prompt catalogue

|  |  |  |  |
|:--:|:--:|:--:|:--:|
| **Prompt ID** | **Used by** | **Purpose** | **Mandatory output** |
| <span class="comment-start" id="23" author="Yuen, Kit Shun Jackson" date="2026-08-26T14:05:00Z">Is there any example of actual prompt to be used for P-01 to P-05?</span><span class="comment-start" id="24" author="Yuen, Kit Shun Jackson" date="2026-08-26T14:10:00Z">Resolved, detailed will be defined in build stage</span>P-01<span class="comment-end" id="23"><span class="comment-end" id="24"></span></span> | A05 | Explain a payroll variance from deterministic calculation trace | What changed, why, values, policy/rule, evidence citations, uncertainty. |
| P-02 | A05 | Classify anomaly and propose root-cause category | Category, confidence, evidence, alternatives and missing checks. |
| P-03 | A06 | Create recommendation from approved options and impact | Options compared, impacts, constraints, recommendation and human decision requested. |
| P-04 | A01 | Summarise approval case for Payroll Controller | Decision question, affected scope, financial impact, risk, evidence and actions. |
| P-05 | A08 | Create audit narrative from immutable events | Chronology, actors, versions, controls, decision, outcome and evidence manifest. |

| **Response** | **Required content** |
|----|----|
| Workspace review | Case status, anomaly, explanation, impact, recommendation, controls, evidence and allowed actions. |
| Approval request | Decision required, authority, amount/population, risk, rationale, evidence, expiry and sign-off context. |
| Lifecycle handover | Anomaly class, lifecycle event, payroll evidence, requested investigation and return contract. |
| Exception | Safe summary, owner, SLA, secure context and re-entry state. |
| Audit pack | Chronology, versions, inputs, deterministic results, decisions, commit, validation, logs and closure status. |

# 10. Updated Unit-Test Scenarios

| **ID** | **Scope** | **Scenario** | **Expected result** |
|:--:|----|----|----|
| UT-01 | W01/A03 | Complete source snapshot | Dataset and lineage created. |
| UT-02 | W02/CP01 | Mandatory field absent | Progress blocked; gap evidence recorded. |
| UT-03 | W03/A04 | Each of seven anomaly classes | Correct anomaly and rule version produced. |
| UT-04 | W03 lifecycle | Joiner/leaver anomaly | Lifecycle handover created with return contract. |
| UT-05 | W04-W05 | Risk/classification boundary | Expected band/class with factors and version. |
| UT-06 | W06 | Complete calculation trace | Explanation cites every material number. |
| UT-07 | W06 | Unsupported evidence | INSUFFICIENT_EVIDENCE returned. |
| UT-08 | W09-W11 | Multiple options | Impact comparison and advisory recommendation. |
| UT-09 | W13-W15 | Missing approval | Commit blocked. |
| UT-10 | W14/CP06 | SoD conflict | Decision rejected and conflict logged. |
| UT-11 | W14-W15 | Period sign-off required | Sign-off captured before final authorised progression. |
| UT-12 | W16 ABBA asset | Adapted calculation candidate | Passes Fabric/source-fit contract before use. |
| UT-13 | W17 | Validation failure | Case returns to approved rework state. |
| UT-14 | W18-W19 | Evidence/log incomplete | Closure blocked. |
| UT-15 | W20 | A08 attestation + A02 transition proposal | Single closure event after CP10 pass. |
| UT-16 | Security | Unauthorised worker detail | Access denied and event logged. |
| UT-17 | Resilience | AI unavailable | Deterministic result remains available. |
| UT-18 | Idempotency | Duplicate commit request | Single consequential update. |

# 11. Stage 6A Issues, Assumptions and Decisions

| **ID** | **Item** | **Treatment** |
|:--:|----|----|
| 6A-01 | Resolve A08 versus A02 W20 ownership | FDA decision and final RACI. |
| 6A-02 | Confirm Onboarding & Lifecycle Agent return contract | Define response, ownership, SLA and re-entry. |
| 6A-03 | Approve seven-anomaly rule catalogue | Versioned rules, thresholds and evidence. |
| 6A-04 | Approve ABBA adapted assets | Complete technical and control fit-gap. |
| 6A-05 | Approve period sign-off semantics in A09 | Authority, scope and evidence. |
| 6A-06 | Resolve Stage 5B DA-01 to DA-08 | Close or accept as Build entry conditions. |
| 6A-07 | Approve write-back, idempotency and rollback | Integration contract required. |
| 6A-08 | Approve retention, immutable evidence and legal hold | Governance decision required. |

# Appendix A. Updated Source Register

| **Source** | **Use** |
|----|----|
| Payroll_Assurance_Agent_Stage_4_Classify_Capability_Based (2).docx | Primary updated classification, workflow ownership, handovers, controls, frameworks and ABBA assessment. |
| Payroll_Assurance_Agent_Stage_3_Decompose.docx | Overall AI Framework, W01-W20 business workflow and human boundary. |
| Payroll_Assurance_Stage_5_5B_Enterprise_Data_Model (1).docx | Canonical entities, lineage, controls, Fabric design and DA conditions. |
| Payroll_Assurance_Agent_Stage_6_Detailed_Design_Final.docx | Previous Stage 6 design used as a superseded baseline where Stage 4 v2 changes apply. |
