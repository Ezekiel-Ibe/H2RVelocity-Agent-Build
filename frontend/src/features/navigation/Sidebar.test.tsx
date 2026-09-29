import { describe, it, expect } from "vitest";
import { screen } from "@testing-library/react";
import { Sidebar } from "./Sidebar";
import { renderWithProviders } from "@/test/renderWithProviders";

describe("Sidebar", () => {
  it("renders the primary navigation landmark", () => {
    renderWithProviders(<Sidebar collapsed={false} onToggle={() => {}} />);
    expect(screen.getByRole("navigation", { name: "Primary" })).toBeInTheDocument();
  });

  it("renders all navigation links", () => {
    renderWithProviders(<Sidebar collapsed={false} onToggle={() => {}} />);
    for (const label of [
      "Home",
      "Cases",
      "Exceptions",
      "Approvals",
      "Audit Trail",
      "Reports",
      "Insights",
      "Settings",
    ]) {
      expect(screen.getByRole("link", { name: new RegExp(label, "i") })).toBeInTheDocument();
    }
  });

  it("marks the current route with aria-current", () => {
    renderWithProviders(<Sidebar collapsed={false} onToggle={() => {}} />, { route: "/exceptions" });
    const current = screen.getByRole("link", { name: /Exceptions/i });
    expect(current).toHaveAttribute("aria-current", "page");
  });
});
