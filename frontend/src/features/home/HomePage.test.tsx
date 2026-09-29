import { describe, it, expect } from "vitest";
import { screen, waitFor } from "@testing-library/react";
import { HomePage } from "./HomePage";
import { renderWithProviders } from "@/test/renderWithProviders";

describe("HomePage", () => {
  it("renders dashboard data fetched from the mock API", async () => {
    renderWithProviders(<HomePage />);

    await waitFor(() =>
      expect(screen.getByText("Assurance Overview")).toBeInTheDocument(),
    );

    expect(screen.getByRole("heading", { name: "Payroll Assurance Agent", level: 1 })).toBeInTheDocument();
    expect(screen.getByText("Employees Covered")).toBeInTheDocument();
    expect(screen.getByText("Recent Cases")).toBeInTheDocument();
    expect(screen.getByText("PA-2024-0512")).toBeInTheDocument();
  });
});
