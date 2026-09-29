import type { ReactElement, ReactNode } from "react";
import { render } from "@testing-library/react";
import { FluentProvider, webLightTheme } from "@fluentui/react-components";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import { PeriodFilterProvider } from "@/features/common/PeriodFilterContext";

export function renderWithProviders(
  ui: ReactElement,
  { route = "/" }: { route?: string } = {},
) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  function Wrapper({ children }: { children: ReactNode }) {
    return (
      <FluentProvider theme={webLightTheme}>
        <QueryClientProvider client={queryClient}>
          <MemoryRouter
            initialEntries={[route]}
            future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
          >
            <PeriodFilterProvider>{children}</PeriodFilterProvider>
          </MemoryRouter>
        </QueryClientProvider>
      </FluentProvider>
    );
  }

  return render(ui, { wrapper: Wrapper });
}
