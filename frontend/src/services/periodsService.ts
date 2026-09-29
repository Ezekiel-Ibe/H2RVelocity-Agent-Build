import { periodsResponseSchema, type Period } from "@/contracts/schemas";
import { API_BASE_URL } from "./apiConfig";
import { endpoints } from "./endpoints";

export async function fetchPeriods(): Promise<Period[]> {
  const response = await fetch(`${API_BASE_URL}${endpoints.periods}`);
  if (!response.ok) {
    throw new Error(`Failed to load periods (${response.status})`);
  }
  const payload: unknown = await response.json();
  return periodsResponseSchema.parse(payload);
}
