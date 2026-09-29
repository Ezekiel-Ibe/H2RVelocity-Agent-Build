import { insightsSchema, type Insights } from "@/contracts/schemas";
import { API_BASE_URL } from "./apiConfig";
import { endpoints } from "./endpoints";
import { periodQuery, type PeriodFilterValue } from "./periodFilter";

export async function fetchInsights(filter?: PeriodFilterValue | null): Promise<Insights> {
  const response = await fetch(`${API_BASE_URL}${endpoints.insights}${periodQuery(filter)}`);
  if (!response.ok) {
    throw new Error(`Failed to load insights (${response.status})`);
  }
  const payload: unknown = await response.json();
  return insightsSchema.parse(payload);
}
