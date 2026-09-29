import { describe, it, expect } from "vitest";
import { dashboardSchema } from "@/contracts/schemas";
import { dashboardFixture } from "@/fixtures/dashboard";

describe("dashboard fixture", () => {
  it("matches the runtime contract", () => {
    const result = dashboardSchema.safeParse(dashboardFixture);
    expect(result.success).toBe(true);
  });

  it("has an assurance score within range", () => {
    expect(dashboardFixture.overview.score).toBeGreaterThanOrEqual(0);
    expect(dashboardFixture.overview.score).toBeLessThanOrEqual(100);
  });

  it("risk breakdown percentages sum to 100", () => {
    const sum = dashboardFixture.overview.breakdown.reduce(
      (acc, row) => acc + row.percentage,
      0,
    );
    expect(sum).toBe(100);
  });
});
