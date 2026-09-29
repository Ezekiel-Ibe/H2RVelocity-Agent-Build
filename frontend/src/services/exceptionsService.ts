import { exceptionsResponseSchema, type ExceptionDetail } from "@/contracts/schemas";
import { API_BASE_URL } from "./apiConfig";
import { endpoints } from "./endpoints";

export async function fetchExceptions(): Promise<ExceptionDetail[]> {
  const response = await fetch(`${API_BASE_URL}${endpoints.exceptions}`);
  if (!response.ok) {
    throw new Error(`Failed to load exceptions (${response.status})`);
  }
  const payload: unknown = await response.json();
  return exceptionsResponseSchema.parse(payload);
}
