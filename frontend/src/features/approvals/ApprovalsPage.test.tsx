import { describe, it, expect } from "vitest";
import { screen, waitFor } from "@testing-library/react";
import { ApprovalsPage } from "./ApprovalsPage";
import { renderWithProviders } from "@/test/renderWithProviders";

describe("ApprovalsPage", () => {
  it("lists only cases awaiting approval", async () => {
    renderWithProviders(<ApprovalsPage />);
    await waitFor(() =>
      expect(screen.getByText("PA-2024-0512")).toBeInTheDocument(),
    );
    // Closed case should not appear.
    expect(screen.queryByText("PA-2024-0498")).not.toBeInTheDocument();
    expect(screen.getAllByText(/Review & decide/i).length).toBeGreaterThan(0);
  });
});
