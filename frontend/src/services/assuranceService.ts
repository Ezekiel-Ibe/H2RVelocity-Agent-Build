import { API_BASE_URL } from "./apiConfig";
import { endpoints } from "./endpoints";

/** Closure summary returned by the payroll-assurance-af hosted agent. */
export type AssuranceSummary = {
  runId: string | null;
  case_id?: string;
  case_state?: "CLOSED" | "HELD_FOR_REVIEW" | string;
  total_anomalies?: number;
  high_severity_count?: number;
  risk_score?: number;
  risk_band?: string;
  manifest_hash?: string;
  signoff_token?: string;
  committed_corrections?: number;
  success?: boolean;
  error?: string;
  detail?: string;
};

/** Explicit UI action — triggers the assurance workflow (writes handled by the agent). */
export async function runAssurance(
  payrollRunId: string,
  periodId: string,
): Promise<AssuranceSummary> {
  const response = await fetch(`${API_BASE_URL}${endpoints.runAssurance}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ payrollRunId, periodId }),
  });
  if (!response.ok) {
    throw new Error(`Failed to run assurance (${response.status})`);
  }
  return (await response.json()) as AssuranceSummary;
}
