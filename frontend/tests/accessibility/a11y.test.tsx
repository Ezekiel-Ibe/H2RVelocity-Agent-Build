import { describe, it, expect } from "vitest";
import { axe } from "vitest-axe";
import { Sidebar } from "@/features/navigation/Sidebar";
import { QuickActions } from "@/features/home/QuickActions";
import { renderWithProviders } from "@/test/renderWithProviders";

describe("accessibility", () => {
  it("Sidebar has no detectable axe violations", async () => {
    const { container } = renderWithProviders(<Sidebar collapsed={false} onToggle={() => {}} />);
    const results = await axe(container, {
      rules: { "color-contrast": { enabled: false } },
    });
    expect(results).toHaveNoViolations();
  });

  it("QuickActions has no detectable axe violations", async () => {
    const { container } = renderWithProviders(<QuickActions />);
    const results = await axe(container, {
      rules: { "color-contrast": { enabled: false } },
    });
    expect(results).toHaveNoViolations();
  });
});
