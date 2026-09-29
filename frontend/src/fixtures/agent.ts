import type { AgentEvidenceStatus } from "@/contracts/schemas";

/**
 * SYNTHETIC DEVELOPMENT FIXTURE ONLY — canned agent replies.
 * The agent performs NO authoritative payroll reasoning here. Per Stage 7A §4.5,
 * material statements must cite evidence_id / calculation_id, and the agent must
 * return INSUFFICIENT_EVIDENCE when grounding is missing, stale or contradictory.
 */
export type AgentReply = {
  body: string;
  citations: string[];
  evidenceStatus: AgentEvidenceStatus;
};

const cannedReplies: { match: RegExp; reply: AgentReply }[] = [
  {
    // No grounded basis — must decline rather than invent.
    match: /forecast|predict|future|guarantee|estimate next/i,
    reply: {
      body: "INSUFFICIENT_EVIDENCE: I can't answer that from the available grounded evidence. Forecasts and predictions aren't supported by the current case data. Please narrow the question to an existing case, anomaly or payroll run.",
      citations: [],
      evidenceStatus: "insufficient_evidence",
    },
  },
  {
    match: /summari[sz]e.*(case|exception|anomal)/i,
    reply: {
      body: "Development response: open cases include a leaver-still-paid (PA-2024-0512, high), an unexplained variance (PA-2024-0508, high) and a duplicate pay record (PA-2024-0509, medium). Authoritative detail comes from governed backend services, not this agent.",
      citations: ["EV-01", "EV-02", "EV-04"],
      evidenceStatus: "grounded",
    },
  },
  {
    match: /assurance score|92%/i,
    reply: {
      body: "Development response: the illustrative assurance score reflects the proportion of assurance checks passed on the latest run. Authoritative scoring is produced by deterministic services (calculation CAL-RISK-88), not by this agent.",
      citations: ["CAL-RISK-88"],
      evidenceStatus: "grounded",
    },
  },
  {
    match: /high[- ]?risk|anomal/i,
    reply: {
      body: "Development response: high-risk anomalies in the sample include 'Leaver still paid' and 'Unexplained variance'. See the Exceptions page for the full synthetic list of the seven anomaly classes.",
      citations: ["EV-01"],
      evidenceStatus: "grounded",
    },
  },
  {
    match: /PA-2024|explain case|case/i,
    reply: {
      body: "Development response: case PA-2024-0512 is a leaver-still-paid anomaly (risk 88) awaiting Payroll Controller approval at step W13. Any correction requires human approval — this agent is advisory only.",
      citations: ["EV-01", "EV-02", "EV-04"],
      evidenceStatus: "grounded",
    },
  },
];

export function generateAgentReply(prompt: string): AgentReply {
  const matched = cannedReplies.find((r) => r.match.test(prompt));
  return (
    matched?.reply ?? {
      body: "This is a synthetic development response. Connect a governed backend service to return evidence-backed assurance answers.",
      citations: [],
      evidenceStatus: "grounded",
    }
  );
}
