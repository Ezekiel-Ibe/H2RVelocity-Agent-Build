import { describe, it, expect } from "vitest";
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { CasesPage } from "./CasesPage";
import { renderWithProviders } from "@/test/renderWithProviders";
import { server } from "@/mocks/server";

describe("CasesPage", () => {
  it("renders cases from the mock API", async () => {
    renderWithProviders(<CasesPage />);
    await waitFor(() =>
      expect(screen.getByText("PA-2024-0512")).toBeInTheDocument(),
    );
    expect(screen.getByText("A. Okafor")).toBeInTheDocument();
  });

  it("filters to closed cases", async () => {
    const user = userEvent.setup();
    renderWithProviders(<CasesPage />);
    await waitFor(() =>
      expect(screen.getByText("PA-2024-0512")).toBeInTheDocument(),
    );
    await user.click(screen.getByRole("button", { name: "Closed" }));
    expect(screen.queryByText("PA-2024-0512")).not.toBeInTheDocument();
    expect(screen.getByText("PA-2024-0498")).toBeInTheDocument();
  });

  it("shows an error state when the API fails", async () => {
    server.use(http.get("/api/cases", () => HttpResponse.json({}, { status: 500 })));
    renderWithProviders(<CasesPage />);
    await waitFor(() => expect(screen.getByRole("alert")).toBeInTheDocument());
  });
});
