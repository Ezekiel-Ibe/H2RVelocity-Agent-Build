/// <reference types="vitest" />
import { defineConfig, type Plugin, type Connect } from "vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath, URL } from "node:url";

function readJsonBody(req: Connect.IncomingMessage): Promise<unknown> {
  return new Promise((resolve) => {
    let data = "";
    req.on("data", (chunk) => (data += chunk));
    req.on("end", () => {
      try {
        resolve(data ? JSON.parse(data) : {});
      } catch {
        resolve({});
      }
    });
  });
}

/**
 * Serves the mock API from the dev server (no service worker), so local dev
 * data loads reliably in any browser. Tests use the MSW node server separately.
 */
function mockApiPlugin(): Plugin {
  return {
    name: "mock-api",
    configureServer(server) {
      server.middlewares.use(async (req, res, next) => {
        const url = req.url ?? "";
        if (!url.startsWith("/api/")) return next();

        const path = url.split("?")[0].replace(/\/$/, "");
        const method = req.method ?? "GET";
        const send = (status: number, data: unknown) => {
          res.statusCode = status;
          res.setHeader("Content-Type", "application/json");
          res.end(JSON.stringify(data));
        };
        const load = (p: string) => server.ssrLoadModule(p);

        try {
          if (method === "GET" && path === "/api/dashboard") {
            const { dashboardFixture } = await load("/src/fixtures/dashboard.ts");
            return send(200, dashboardFixture);
          }
          if (method === "GET" && path === "/api/cases") {
            const { casesFixture } = await load("/src/fixtures/cases.ts");
            return send(200, casesFixture);
          }
          const caseMatch = path.match(/^\/api\/cases\/([^/]+)$/);
          if (method === "GET" && caseMatch) {
            const { caseDetailsFixture } = await load("/src/fixtures/caseDetails.ts");
            const detail = caseDetailsFixture[decodeURIComponent(caseMatch[1])];
            return detail ? send(200, detail) : send(404, { error: "Not found" });
          }
          const decisionMatch = path.match(/^\/api\/cases\/([^/]+)\/decision$/);
          if (method === "POST" && decisionMatch) {
            const body = (await readJsonBody(req)) as { action?: string; rationale?: string };
            if (!body.action || !body.rationale || body.rationale.length < 10) {
              return send(400, { error: "Invalid decision" });
            }
            return send(200, {
              caseId: decodeURIComponent(decisionMatch[1]),
              action: body.action,
              outcome: `Decision recorded: ${body.action}. Routed to Human Approval Control (A09).`,
              recordedAt: "Just now",
            });
          }
          if (method === "GET" && path === "/api/exceptions") {
            const { exceptionsFixture } = await load("/src/fixtures/exceptions.ts");
            return send(200, exceptionsFixture);
          }
          if (method === "GET" && path === "/api/audit") {
            const { auditFixture } = await load("/src/fixtures/audit.ts");
            return send(200, auditFixture);
          }
          if (method === "POST" && path === "/api/agent/messages") {
            const body = (await readJsonBody(req)) as { prompt?: string };
            if (!body.prompt) return send(400, { error: "Invalid request" });
            const { generateAgentReply } = await load("/src/fixtures/agent.ts");
            const reply = generateAgentReply(body.prompt);
            return send(200, {
              id: `agent-${Date.now()}`,
              author: "agent",
              body: reply.body,
              timestamp: "Just now",
              evidenceStatus: reply.evidenceStatus,
              citations: reply.citations,
            });
          }
          return next();
        } catch (error) {
          send(500, { error: String(error) });
        }
      });
    },
  };
}

export default defineConfig({
  plugins: [react(), mockApiPlugin()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
    css: true,
    // Force tests onto the MSW mocks (relative URLs), never the live BFF.
    env: {
      VITE_API_BASE_URL: "",
      VITE_USE_MOCKS: "true",
    },
    include: [
      "src/**/*.{test,spec}.{ts,tsx}",
      "tests/accessibility/**/*.{test,spec}.{ts,tsx}",
    ],
    exclude: ["tests/e2e/**", "node_modules/**", "dist/**"],
  },
});
