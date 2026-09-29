import {
  casesResponseSchema,
  caseDetailSchema,
  type PayrollCase,
  type PayrollCaseDetail,
  type DecisionAction,
  type DecisionResponse,
} from "@/contracts/schemas";
import { API_BASE_URL } from "./apiConfig";
import { endpoints } from "./endpoints";
import {
  allDecisions,
  getDecision,
  recordDecision,
  statusForAction,
} from "./decisionsStore";

export async function fetchCases(): Promise<PayrollCase[]> {
  const response = await fetch(`${API_BASE_URL}${endpoints.cases}`);
  if (!response.ok) {
    throw new Error(`Failed to load cases (${response.status})`);
  }
  const payload: unknown = await response.json();
  const cases = casesResponseSchema.parse(payload);
  // Overlay this session's decisions (client-side only — never written to Fabric).
  const decisions = allDecisions();
  return cases.map((c) =>
    decisions[c.id]
      ? { ...c, status: statusForAction(decisions[c.id].action) as PayrollCase["status"] }
      : c,
  );
}

export async function fetchCaseDetail(id: string): Promise<PayrollCaseDetail> {
  const response = await fetch(`${API_BASE_URL}${endpoints.caseDetail(id)}`);
  if (!response.ok) {
    throw new Error(`Failed to load case ${id} (${response.status})`);
  }
  const payload: unknown = await response.json();
  const detail = caseDetailSchema.parse(payload);
  const decision = getDecision(id);
  if (!decision) {
    return detail;
  }
  return {
    ...detail,
    decision,
    status: statusForAction(decision.action) as PayrollCaseDetail["status"],
    allowedActions: [],
  };
}

const OUTCOME: Record<DecisionAction, string> = {
  Approve: "approved and routed to Data Management (A03) for the governed commit",
  Reject: "rejected — no pay-impacting change will be made",
  Escalate: "escalated for senior review",
};

export function submitCaseDecision(
  id: string,
  action: DecisionAction,
  rationale: string,
): Promise<DecisionResponse> {
  // Per-session, client-side only — records to sessionStorage, no server/Fabric write.
  const decision = recordDecision(id, action, rationale);
  return Promise.resolve({
    caseId: id,
    action,
    outcome: `Decision recorded: ${action}. Case ${OUTCOME[action]}.`,
    recordedAt: decision.decidedOn,
  });
}
