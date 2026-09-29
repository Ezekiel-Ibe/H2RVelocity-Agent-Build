import { http, HttpResponse } from "msw";
import { dashboardFixture } from "@/fixtures/dashboard";
import { casesFixture } from "@/fixtures/cases";
import { caseDetailsFixture } from "@/fixtures/caseDetails";
import { exceptionsFixture } from "@/fixtures/exceptions";
import { auditFixture } from "@/fixtures/audit";
import { insightsFixture } from "@/fixtures/insights";
import { periodsFixture } from "@/fixtures/periods";
import { generateAgentReply } from "@/fixtures/agent";
import { agentRequestSchema, decisionRequestSchema } from "@/contracts/schemas";

/**
 * Mock API handlers. Serve synthetic development fixtures over HTTP so the app
 * exercises the same fetch + validation path it will use against governed
 * backend services. Replace these handlers with real endpoints when available.
 */
export const handlers = [
  http.get("/api/dashboard", () => HttpResponse.json(dashboardFixture)),

  http.get("/api/cases", () => HttpResponse.json(casesFixture)),

  http.get("/api/cases/:id", ({ params }) => {
    const detail = caseDetailsFixture[String(params.id)];
    return detail
      ? HttpResponse.json(detail)
      : HttpResponse.json({ error: "Not found" }, { status: 404 });
  }),

  http.post("/api/cases/:id/decision", async ({ params, request }) => {
    const parsed = decisionRequestSchema.safeParse(await request.json());
    if (!parsed.success) {
      return HttpResponse.json({ error: "Invalid decision" }, { status: 400 });
    }
    return HttpResponse.json({
      caseId: String(params.id),
      action: parsed.data.action,
      outcome: `Decision recorded: ${parsed.data.action}. Routed to Human Approval Control (A09).`,
      recordedAt: "Just now",
    });
  }),

  http.get("/api/exceptions", () => HttpResponse.json(exceptionsFixture)),

  http.get("/api/audit", () => HttpResponse.json(auditFixture)),

  http.get("/api/insights", () => HttpResponse.json(insightsFixture)),

  http.get("/api/periods", () => HttpResponse.json(periodsFixture)),

  http.post("/api/admin/reset", () => HttpResponse.json({ status: "ok", clearedDecisions: 0 })),

  http.post("/api/agent/messages", async ({ request }) => {
    const parsed = agentRequestSchema.safeParse(await request.json());
    if (!parsed.success) {
      return HttpResponse.json({ error: "Invalid request" }, { status: 400 });
    }
    const reply = generateAgentReply(parsed.data.prompt);
    return HttpResponse.json({
      id: `agent-${Date.now()}`,
      author: "agent",
      body: reply.body,
      timestamp: "Just now",
      evidenceStatus: reply.evidenceStatus,
      citations: reply.citations,
      conversationId: parsed.data.conversationId ?? "mock-conversation",
    });
  }),
];
