import { describe, it, expect } from "vitest";
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ExceptionsPage } from "./ExceptionsPage";
import { renderWithProviders } from "@/test/renderWithProviders";

describe("ExceptionsPage", () => {
  it("renders exceptions from the mock API", async () => {
    renderWithProviders(<ExceptionsPage />);
    await waitFor(() =>
      expect(screen.getByText("Leaver still paid")).toBeInTheDocument(),
    );
    expect(screen.getByText("Missing tax code")).toBeInTheDocument();
  });

  it("filters by severity and can show an empty result", async () => {
    const user = userEvent.setup();
    renderWithProviders(<ExceptionsPage />);
    await waitFor(() =>
      expect(screen.getByText("Leaver still paid")).toBeInTheDocument(),
    );

    await user.click(screen.getByRole("button", { name: "Low" }));
    expect(screen.queryByText("Leaver still paid")).not.toBeInTheDocument();
    expect(screen.getByText("Unapproved change")).toBeInTheDocument();
  });
});
