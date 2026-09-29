import type { Period } from "@/contracts/schemas";

// Synthetic development pay periods (mock mode only).
export const periodsFixture: Period[] = [
  { id: "PP-2024-05", name: "May 2024", start: "2024-05-01", end: "2024-05-31", status: "CLOSED" },
  { id: "PP-2024-04", name: "April 2024", start: "2024-04-01", end: "2024-04-30", status: "CLOSED" },
];
