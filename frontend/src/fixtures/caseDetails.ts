import type { PayrollCaseDetail } from "@/contracts/schemas";
import { casesFixture } from "./cases";

/**
 * SYNTHETIC DEVELOPMENT FIXTURE ONLY — not validated business data.
 * Fully-populated case detail for the flagship "Awaiting Approval" case, plus a
 * generic builder for the remaining cases so every row opens a coherent view.
 * The frontend never computes these values — deterministic services are
 * authoritative; this is illustrative development data only.
 */

const flagship: PayrollCaseDetail = {
  ...casesFixture[0],
  anomalyDescription:
    "Worker WKR-10233 has a termination date of 30 Apr 2024 but received a full net payment in the May 2024 run.",
  ruleId: "R-ANOM-LEAVER-STILL-PAID",
  ruleVersion: "v3.2",
  riskFactors: [
    { name: "Employment status", weight: 0.4, contribution: 38, note: "Terminated before period start" },
    { name: "Payment amount", weight: 0.3, contribution: 27, note: "Full-period gross paid" },
    { name: "Recurrence", weight: 0.2, contribution: 15, note: "First occurrence for this worker" },
    { name: "Approval history", weight: 0.1, contribution: 8, note: "No approved change on file" },
  ],
  rootCause:
    "Termination effective date was recorded in HRIS after the payroll cut-off, so the leaver was not excluded from the May run.",
  correctionOptions: [
    {
      id: "OPT-1",
      label: "Recover overpayment and stop future pay",
      description: "Raise recovery for the May net payment and exclude the worker from future runs.",
      recommended: true,
    },
    {
      id: "OPT-2",
      label: "Stop future pay only",
      description: "Exclude from future runs; do not recover the May payment.",
      recommended: false,
    },
  ],
  impact: [
    { label: "Gross", value: "£3,420.00" },
    { label: "Tax (PAYE)", value: "£548.00" },
    { label: "National Insurance", value: "£312.40" },
    { label: "Pension", value: "£171.00" },
    { label: "Net (recoverable)", value: "£2,388.60" },
    { label: "Cost centre", value: "CC-4021" },
    { label: "GL account", value: "GL-6000-Payroll" },
  ],
  recommendation: {
    summary: "Recover the May overpayment and stop future payments (Option 1).",
    rationale:
      "The worker was terminated before the period and no approved change exists. Recovery limits leakage and aligns with policy.",
    confidence: "High",
    citations: ["EV-01", "EV-02", "EV-04"],
  },
  controls: [
    { id: "CP01", name: "Input completeness", owner: "A07", result: "Pass", detail: "All required records present." },
    { id: "CP02", name: "Approved anomaly rule", owner: "A04", result: "Pass", detail: "Rule R-ANOM-LEAVER-STILL-PAID v3.2." },
    { id: "CP03", name: "Risk and severity", owner: "A05", result: "Pass", detail: "Risk 88 (High) within approved bands." },
    { id: "CP04", name: "Evidence sufficiency", owner: "A06", result: "Pass", detail: "Impact, rationale and evidence present." },
    { id: "CP05", name: "Mandatory human approval", owner: "A09", result: "Pending", detail: "Awaiting Payroll Controller decision." },
    { id: "CP06", name: "Segregation of duties", owner: "A09", result: "Pending", detail: "Agent recommends; human approves." },
    { id: "CP07", name: "Post-correction validation", owner: "A07", result: "N/A", detail: "Runs after commit." },
    { id: "CP08", name: "Audit evidence completeness", owner: "A08", result: "Pending", detail: "Pack assembled at closure." },
    { id: "CP09", name: "Governance logging", owner: "A08", result: "Pending", detail: "Decision log pending approval." },
    { id: "CP10", name: "Case closure", owner: "A02", result: "N/A", detail: "Closes after actions complete." },
  ],
  evidence: [
    { id: "EV-01", label: "HRIS termination record", source: "HRIS", hash: "sha256:9f2a…c41", capturedOn: "27 May 2024" },
    { id: "EV-02", label: "May payroll line", source: "silver.payroll_line", hash: "sha256:1bd7…88e", capturedOn: "27 May 2024" },
    { id: "EV-03", label: "Prior-period comparison", source: "gold.fact_payroll_line", hash: "sha256:44a0…2f9", capturedOn: "27 May 2024" },
    { id: "EV-04", label: "Approval history (none)", source: "Dataverse", hash: "sha256:0c53…7ab", capturedOn: "27 May 2024" },
  ],
  allowedActions: ["Approve", "Reject", "Escalate"],
  decision: null,
};

function genericDetail(index: number): PayrollCaseDetail {
  const c = casesFixture[index];
  const awaiting = c.status === "Awaiting Approval";
  return {
    ...c,
    anomalyDescription: `${c.anomalyTitle} detected for ${c.workerName} in run ${c.payrollRunId}.`,
    ruleId: `R-ANOM-${c.anomalyType.toUpperCase()}`,
    ruleVersion: "v3.2",
    riskFactors: [
      { name: "Primary indicator", weight: 0.5, contribution: Math.round(c.riskScore * 0.5), note: "Matched anomaly rule" },
      { name: "Amount", weight: 0.3, contribution: Math.round(c.riskScore * 0.3), note: "Within materiality review" },
      { name: "History", weight: 0.2, contribution: Math.round(c.riskScore * 0.2), note: "Recurrence considered" },
    ],
    rootCause: "Root-cause assessment produced by the Analysis Agent (A05); see evidence.",
    correctionOptions: [
      { id: "OPT-1", label: "Apply recommended correction", description: "Deterministic correction per policy.", recommended: true },
      { id: "OPT-2", label: "Route for manual investigation", description: "Escalate to SME review.", recommended: false },
    ],
    impact: [
      { label: "Gross", value: "£—" },
      { label: "Net", value: "£—" },
      { label: "Cost centre", value: "CC-4021" },
    ],
    recommendation: {
      summary: "Review the recommended correction and evidence before deciding.",
      rationale: "Advisory recommendation generated from deterministic analysis; human approval required.",
      confidence: c.severity === "high" ? "High" : c.severity === "medium" ? "Medium" : "Low",
      citations: ["EV-01", "EV-02"],
    },
    controls: [
      { id: "CP01", name: "Input completeness", owner: "A07", result: "Pass", detail: "Required records present." },
      { id: "CP02", name: "Approved anomaly rule", owner: "A04", result: "Pass", detail: `Rule ${c.anomalyType}.` },
      { id: "CP03", name: "Risk and severity", owner: "A05", result: "Pass", detail: `Risk ${c.riskScore}.` },
      { id: "CP04", name: "Evidence sufficiency", owner: "A06", result: awaiting ? "Pass" : "Pending", detail: "Evidence pack status." },
      { id: "CP05", name: "Mandatory human approval", owner: "A09", result: awaiting ? "Pending" : "N/A", detail: "Human decision gate." },
      { id: "CP06", name: "Segregation of duties", owner: "A09", result: awaiting ? "Pending" : "N/A", detail: "Agent recommends; human approves." },
    ],
    evidence: [
      { id: "EV-01", label: "Source record", source: "HRIS", hash: "sha256:aa11…22b", capturedOn: c.detectedOn },
      { id: "EV-02", label: "Payroll line", source: "silver.payroll_line", hash: "sha256:cc33…44d", capturedOn: c.detectedOn },
    ],
    allowedActions: awaiting ? ["Approve", "Reject", "Escalate"] : [],
    decision:
      c.status === "Closed"
        ? { action: "Approve", rationale: "Correction approved and validated.", decidedBy: "KPMG User", decidedOn: c.lastUpdated }
        : null,
  };
}

export const caseDetailsFixture: Record<string, PayrollCaseDetail> = Object.fromEntries(
  casesFixture.map((c, i) => [c.id, i === 0 ? flagship : genericDetail(i)]),
);
