import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { FluentProvider, webLightTheme } from "@fluentui/react-components";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter } from "react-router-dom";
import App from "./app/App";
import "./design-system/global.css";

const queryClient = new QueryClient({
  // Refetch whenever a page mounts (tab change) or the window regains focus, so
  // actions like an approval show up across views without a manual refresh.
  defaultOptions: {
    queries: { refetchOnWindowFocus: true, refetchOnMount: "always", staleTime: 15_000 },
  },
});

// The mock API is served by the Vite dev middleware (see vite.config.ts), so no
// service worker is needed. Remove any stale MSW worker from earlier sessions.
if (import.meta.env.DEV && "serviceWorker" in navigator) {
  navigator.serviceWorker
    .getRegistrations()
    .then((regs) => regs.forEach((r) => r.unregister()))
    .catch(() => {});
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <FluentProvider theme={webLightTheme}>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter
          future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
        >
          <App />
        </BrowserRouter>
      </QueryClientProvider>
    </FluentProvider>
  </StrictMode>,
);
