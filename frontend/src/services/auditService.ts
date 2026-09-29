import { auditResponseSchema, type AuditEvent } from "@/contracts/schemas";
import { API_BASE_URL } from "./apiConfig";
import { endpoints } from "./endpoints";
import { allDecisions } from "./decisionsStore";

export async function fetchAuditTrail(): Promise<AuditEvent[]> {
  const response = await fetch(`${API_BASE_URL}${endpoints.audit}`);
  if (!response.ok) {
    throw new Error(`Failed to load audit trail (${response.status})`);
  }
  const payload: unknown = await response.json();
  const events = auditResponseSchema.parse(payload);
  // Surface this session's recorded decisions (CP05) at the top — client-side only.
  const decisionEvents: AuditEvent[] = Object.entries(allDecisions()).map(
    ([caseId, d]) => ({
      id: `DEC-${caseId}`,
      timestamp: d.decidedOn,
      caseRef: caseId,
      actor: d.decidedBy,
      action: `Human decision recorded: ${d.action}`,
      control: "CP05",
      detail: d.rationale,
    }),
  );
  return [...decisionEvents, ...events];
}
