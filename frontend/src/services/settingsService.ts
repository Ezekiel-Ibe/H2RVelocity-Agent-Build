import { clearDecisions } from "./decisionsStore";

export type ResetResult = { status: string; clearedDecisions: number };

/** Reset demo state — clears this session's recorded decisions (client-side only). */
export function resetDemoData(): Promise<ResetResult> {
  const clearedDecisions = clearDecisions();
  return Promise.resolve({ status: "ok", clearedDecisions });
}
