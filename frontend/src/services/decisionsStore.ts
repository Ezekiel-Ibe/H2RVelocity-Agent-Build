/**
 * Per-session, client-side decision overlay.
 *
 * Human decisions (Approve/Reject/Escalate) are a demo overlay only — they never
 * touch Fabric. Storing them in sessionStorage keeps them isolated per browser
 * session (each tester sees only their own) and independent of how many BFF
 * replicas are running. Cleared on tab close or via Settings → Reset.
 */
import type { CaseDecision, DecisionAction } from "@/contracts/schemas";

const KEY = "payassure.decisions.v1";

const STATUS_FOR_ACTION: Record<DecisionAction, string> = {
  Approve: "Approved",
  Reject: "Closed",
  Escalate: "Escalated",
};

function read(): Record<string, CaseDecision> {
  try {
    const raw = sessionStorage.getItem(KEY);
    return raw ? (JSON.parse(raw) as Record<string, CaseDecision>) : {};
  } catch {
    return {};
  }
}

function write(data: Record<string, CaseDecision>): void {
  try {
    sessionStorage.setItem(KEY, JSON.stringify(data));
  } catch {
    /* storage unavailable — decisions simply won't persist this session */
  }
}

export function allDecisions(): Record<string, CaseDecision> {
  return read();
}

export function getDecision(caseId: string): CaseDecision | null {
  return read()[caseId] ?? null;
}

export function statusForAction(action: DecisionAction): string {
  return STATUS_FOR_ACTION[action];
}

export function recordDecision(
  caseId: string,
  action: DecisionAction,
  rationale: string,
): CaseDecision {
  const now = new Date();
  const decidedOn =
    now.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" }) +
    " " +
    now.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit", hour12: false });
  const decision: CaseDecision = {
    action,
    rationale,
    decidedBy: "KPMG User (Payroll Controller)",
    decidedOn,
  };
  const data = read();
  data[caseId] = decision;
  write(data);
  return decision;
}

export function clearDecisions(): number {
  const count = Object.keys(read()).length;
  try {
    sessionStorage.removeItem(KEY);
  } catch {
    /* ignore */
  }
  return count;
}
