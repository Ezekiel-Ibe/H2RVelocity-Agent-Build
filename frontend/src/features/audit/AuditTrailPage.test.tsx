import { describe, it, expect } from "vitest";
import { screen, waitFor } from "@testing-library/react";
import { AuditTrailPage } from "./AuditTrailPage";
import { renderWithProviders } from "@/test/renderWithProviders";

describe("AuditTrailPage", () => {
  it("renders governance events from the mock API", async () => {
    renderWithProviders(<AuditTrailPage />);
    await waitFor(() =>
      expect(screen.getByText("Anomaly detected")).toBeInTheDocument(),
    );
    expect(screen.getByText("Audit evidence pack assembled")).toBeInTheDocument();
    expect(screen.getAllByText("CP08").length).toBeGreaterThan(0);
  });
});
