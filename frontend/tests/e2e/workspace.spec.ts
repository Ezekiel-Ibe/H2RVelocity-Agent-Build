import { test, expect } from "@playwright/test";

test.describe("Payroll Assurance workspace", () => {
  test("renders the dashboard and key regions", async ({ page }) => {
    await page.goto("/");

    await expect(
      page.getByRole("heading", { name: "Payroll Assurance Agent", level: 1 }),
    ).toBeVisible();
    await expect(page.getByRole("navigation", { name: "Primary" })).toBeVisible();
    await expect(page.getByRole("complementary", { name: "Agent chat" })).toBeVisible();
    await expect(page.getByText("Assurance Overview")).toBeVisible();
    await expect(page.getByText("Active Engagements")).toBeVisible();
  });

  test("navigates to a feature route", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("link", { name: /Exceptions/i }).click();
    await expect(
      page.getByRole("heading", { name: "Exceptions", level: 1 }),
    ).toBeVisible();
  });

  test("sends a suggested prompt to the agent", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: /Show high risk exceptions/i }).click();
    await expect(page.getByText("Show high risk exceptions")).toBeVisible();
  });
});
