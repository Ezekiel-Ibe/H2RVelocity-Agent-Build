import { dashboardSchema, type Dashboard } from "@/contracts/schemas";
import { API_BASE_URL } from "./apiConfig";
import { endpoints } from "./endpoints";
import { periodQuery, type PeriodFilterValue } from "./periodFilter";

/**
 * Fetches the dashboard from the API and validates it against the runtime
 * contract at the boundary. In development the request is served by the MSW
 * mock worker (synthetic fixtures); in other environments it targets the
 * governed backend at VITE_API_BASE_URL.
 */
export async function fetchDashboard(filter?: PeriodFilterValue | null): Promise<Dashboard> {
  const response = await fetch(`${API_BASE_URL}${endpoints.dashboard}${periodQuery(filter)}`);
  if (!response.ok) {
    throw new Error(`Failed to load dashboard (${response.status})`);
  }
  const payload: unknown = await response.json();
  return dashboardSchema.parse(payload);
}
