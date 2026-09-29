import { describe, it, expect } from "vitest";
import { Routes, Route } from "react-router-dom";
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { CaseDetailPage } from "./CaseDetailPage";
import { renderWithProviders } from "@/test/renderWithProviders";

function renderDetail(id: string) {
  return renderWithProviders(
    <Routes>
      <Route path="/cases/:id" element={<CaseDetailPage />} />
    </Routes>,
    { route: `/cases/${id}` },
  );
}

describe("CaseDetailPage", () => {
  it("renders case detail, controls and evidence", async () => {
    renderDetail("PA-2024-0512");
    await waitFor(() =>
      expect(screen.getByRole("heading", { name: "PA-2024-0512", level: 1 })).toBeInTheDocument(),
    );
    expect(screen.getByText(/Mandatory human approval/i)).toBeInTheDocument();
    expect(screen.getByText("EV-01")).toBeInTheDocument();
  });

  it("requires a rationale before recording a decision", async () => {
    const user = userEvent.setup();
    renderDetail("PA-2024-0512");
    await waitFor(() => expect(screen.getByText("Human decision")).toBeInTheDocument());

    await user.click(screen.getByRole("radio", { name: "Approve" }));
    await user.click(screen.getByRole("button", { name: /Submit decision/i }));
    expect(screen.getByRole("alert")).toHaveTextContent(/rationale/i);
  });

  it("records an approve decision with a rationale", async () => {
    const user = userEvent.setup();
    renderDetail("PA-2024-0512");
    await waitFor(() => expect(screen.getByText("Human decision")).toBeInTheDocument());

    await user.click(screen.getByRole("radio", { name: "Approve" }));
    await user.type(
      screen.getByLabelText(/Rationale/i),
      "Leaver confirmed; recover overpayment per policy.",
    );
    await user.click(screen.getByRole("button", { name: /Submit decision/i }));

    await waitFor(() =>
      expect(screen.getByText(/Decision recorded: Approve/i)).toBeInTheDocument(),
    );
  });
});
