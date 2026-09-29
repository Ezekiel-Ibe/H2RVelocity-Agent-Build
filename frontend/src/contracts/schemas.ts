import { z } from "zod";

/**
 * Runtime contracts for API responses. All data flowing into the UI is
 * validated against these schemas. Fixtures are synthetic development data
 * and MUST NOT be treated as validated business results.
 */

export const riskLevelSchema = z.enum(["high", "medium", "low"]);
export type RiskLevel = z.infer<typeof riskLevelSchema>;

/** The seven approved payroll anomaly classes (Stage 4 §8 A04 / Stage 7A §4.4). */
export const anomalyTypeSchema = z.enum([
  "leaver-still-paid",
  "joiner-not-paid",
  "unexplained-variance",
  "missing-tax-code",
  "negative-net-pay",
  "duplicate-pay-record",
  "unapproved-change",
]);
export type AnomalyType = z.infer<typeof anomalyTypeSchema>;

export const anomalyTypeLabels: Record<AnomalyType, string> = {
  "leaver-still-paid": "Leaver still paid",
  "joiner-not-paid": "Joiner not paid",
  "unexplained-variance": "Unexplained variance",
  "missing-tax-code": "Missing tax code",
  "negative-net-pay": "Negative net pay",
  "duplicate-pay-record": "Duplicate pay record",
  "unapproved-change": "Unapproved change",
};

/** Simplified case lifecycle status derived from workflow W01–W20 phases. */
export const caseStatusSchema = z.enum([
  "Detected",
  "In Analysis",
  "Awaiting Approval",
  "Approved",
  "Correcting",
  "Validating",
  "Closed",
  "Escalated",
]);
export type CaseStatus = z.infer<typeof caseStatusSchema>;

export const trendSchema = z.object({
  direction: z.enum(["up", "down"]),
  value: z.string(),
  label: z.string(),
});

export const statCardSchema = z.object({
  id: z.string(),
  label: z.string(),
  value: z.string(),
  caption: z.string(),
  icon: z.enum(["payrolls", "employees", "exceptions", "score"]),
  trend: trendSchema,
});
export type StatCard = z.infer<typeof statCardSchema>;

export const riskBreakdownSchema = z.object({
  level: riskLevelSchema,
  label: z.string(),
  count: z.number().int().nonnegative(),
  percentage: z.number().min(0).max(100),
});
export type RiskBreakdown = z.infer<typeof riskBreakdownSchema>;

export const assuranceOverviewSchema = z.object({
  score: z.number().min(0).max(100),
  breakdown: z.array(riskBreakdownSchema),
  total: z.number().int().nonnegative(),
});
export type AssuranceOverview = z.infer<typeof assuranceOverviewSchema>;

export const exceptionSchema = z.object({
  id: z.string(),
  anomalyType: anomalyTypeSchema,
  severity: riskLevelSchema,
  title: z.string(),
  employeesAffected: z.number().int().nonnegative(),
  count: z.number().int().nonnegative(),
});
export type PayrollException = z.infer<typeof exceptionSchema>;

export const caseSchema = z.object({
  id: z.string(),
  workerRef: z.string(),
  workerName: z.string(),
  payrollRunId: z.string(),
  payPeriod: z.string(),
  anomalyType: anomalyTypeSchema,
  anomalyTitle: z.string(),
  severity: riskLevelSchema,
  riskScore: z.number().min(0).max(100),
  status: caseStatusSchema,
  currentStep: z.string(),
  detectedOn: z.string(),
  lastUpdated: z.string(),
});
export type PayrollCase = z.infer<typeof caseSchema>;

// --- Case detail (A05 analysis, A06 recommendation, A07/A08/A09 controls) ---

export const decisionActionSchema = z.enum(["Approve", "Reject", "Escalate"]);
export type DecisionAction = z.infer<typeof decisionActionSchema>;

export const riskFactorSchema = z.object({
  name: z.string(),
  weight: z.number().min(0).max(1),
  contribution: z.number().min(0).max(100),
  note: z.string(),
});
export type RiskFactor = z.infer<typeof riskFactorSchema>;

export const correctionOptionSchema = z.object({
  id: z.string(),
  label: z.string(),
  description: z.string(),
  recommended: z.boolean(),
});
export type CorrectionOption = z.infer<typeof correctionOptionSchema>;

export const impactLineSchema = z.object({
  label: z.string(),
  value: z.string(),
});
export type ImpactLine = z.infer<typeof impactLineSchema>;

export const recommendationSchema = z.object({
  summary: z.string(),
  rationale: z.string(),
  confidence: z.enum(["High", "Medium", "Low"]),
  citations: z.array(z.string()),
});
export type Recommendation = z.infer<typeof recommendationSchema>;

/** Control result CP01–CP10 (owning agents A07/A08/A09/A02/A04/A05/A06). */
export const controlResultSchema = z.object({
  id: z.string(),
  name: z.string(),
  owner: z.string(),
  result: z.enum(["Pass", "Fail", "Pending", "N/A"]),
  detail: z.string(),
});
export type ControlResult = z.infer<typeof controlResultSchema>;

export const evidenceItemSchema = z.object({
  id: z.string(),
  label: z.string(),
  source: z.string(),
  hash: z.string(),
  capturedOn: z.string(),
});
export type EvidenceItem = z.infer<typeof evidenceItemSchema>;

export const caseDecisionSchema = z.object({
  action: z.enum(["Approve", "Reject", "Escalate"]),
  rationale: z.string(),
  decidedBy: z.string(),
  decidedOn: z.string(),
});
export type CaseDecision = z.infer<typeof caseDecisionSchema>;

/** Grounding status for agent narrative (Stage 7A §4.5). */
export const agentEvidenceStatusSchema = z.enum(["grounded", "insufficient_evidence"]);
export type AgentEvidenceStatus = z.infer<typeof agentEvidenceStatusSchema>;

export const chatMessageSchema = z.object({
  id: z.string(),
  author: z.enum(["agent", "user"]),
  body: z.string(),
  timestamp: z.string(),
  status: z.enum(["complete", "streaming"]).default("complete"),
  statusNote: z.string().optional(),
  citations: z.array(z.string()).optional(),
  evidenceStatus: agentEvidenceStatusSchema.optional(),
});
export type ChatMessage = z.infer<typeof chatMessageSchema>;

export const dashboardSchema = z.object({
  stats: z.array(statCardSchema),
  overview: assuranceOverviewSchema,
  exceptions: z.array(exceptionSchema),
  cases: z.array(caseSchema),
});
export type Dashboard = z.infer<typeof dashboardSchema>;

export const casesResponseSchema = z.array(caseSchema);

export const caseDetailSchema = caseSchema.extend({
  anomalyDescription: z.string(),
  ruleId: z.string(),
  ruleVersion: z.string(),
  riskFactors: z.array(riskFactorSchema),
  rootCause: z.string(),
  correctionOptions: z.array(correctionOptionSchema),
  impact: z.array(impactLineSchema),
  recommendation: recommendationSchema,
  controls: z.array(controlResultSchema),
  evidence: z.array(evidenceItemSchema),
  allowedActions: z.array(decisionActionSchema),
  decision: caseDecisionSchema.nullable(),
});
export type PayrollCaseDetail = z.infer<typeof caseDetailSchema>;

// Human decision capture (A01 → A09). Rationale is mandatory (CP05/CP06).
export const decisionRequestSchema = z.object({
  action: decisionActionSchema,
  rationale: z.string().min(10, "A rationale of at least 10 characters is required"),
});
export type DecisionRequest = z.infer<typeof decisionRequestSchema>;

export const decisionResponseSchema = z.object({
  caseId: z.string(),
  action: decisionActionSchema,
  outcome: z.string(),
  recordedAt: z.string(),
});
export type DecisionResponse = z.infer<typeof decisionResponseSchema>;

export const exceptionStatusSchema = z.enum(["Open", "Under Review", "Resolved"]);
export type ExceptionStatus = z.infer<typeof exceptionStatusSchema>;

export const exceptionDetailSchema = exceptionSchema.extend({
  description: z.string(),
  caseRef: z.string(),
  workerName: z.string(),
  payPeriod: z.string(),
  status: exceptionStatusSchema,
  detectedOn: z.string(),
});
export type ExceptionDetail = z.infer<typeof exceptionDetailSchema>;

export const exceptionsResponseSchema = z.array(exceptionDetailSchema);

// --- Audit trail (A08 governance & audit: CP08 evidence, CP09 logging) ---

export const auditEventSchema = z.object({
  id: z.string(),
  timestamp: z.string(),
  caseRef: z.string(),
  actor: z.string(),
  action: z.string(),
  control: z.string(),
  detail: z.string(),
});
export type AuditEvent = z.infer<typeof auditEventSchema>;

export const auditResponseSchema = z.array(auditEventSchema);

// --- Insights (assurance analytics, API-driven) ---

export const insightsSchema = z.object({
  assuranceScore: z.number().min(0).max(100),
  summary: z.object({
    totalCases: z.number().int().nonnegative(),
    openCases: z.number().int().nonnegative(),
    resolvedCases: z.number().int().nonnegative(),
    totalAnomalies: z.number().int().nonnegative(),
    evidencePacks: z.number().int().nonnegative(),
  }),
  funnel: z.array(z.object({ stage: z.string(), count: z.number().int().nonnegative() })),
  anomalyTypes: z.array(
    z.object({ type: z.string(), count: z.number().int().nonnegative(), maxRisk: z.number().min(0).max(100) }),
  ),
  severityMix: z.array(riskBreakdownSchema),
  topRiskCases: z.array(
    z.object({
      id: z.string(),
      workerName: z.string(),
      anomalyTitle: z.string(),
      severity: riskLevelSchema,
      riskScore: z.number().min(0).max(100),
      status: z.string(),
    }),
  ),
  controlActivity: z.array(z.object({ control: z.string(), count: z.number().int().nonnegative() })),
});
export type Insights = z.infer<typeof insightsSchema>;

// --- Pay periods (period/date filter) ---

export const periodSchema = z.object({
  id: z.string(),
  name: z.string(),
  start: z.string(),
  end: z.string(),
  status: z.string(),
});
export type Period = z.infer<typeof periodSchema>;
export const periodsResponseSchema = z.array(periodSchema);

export const agentRequestSchema = z.object({
  prompt: z.string().min(1),
  conversationId: z.string().nullish(),
});
export type AgentRequest = z.infer<typeof agentRequestSchema>;

export const agentResponseSchema = z.object({
  id: z.string(),
  author: z.literal("agent"),
  body: z.string(),
  timestamp: z.string(),
  evidenceStatus: agentEvidenceStatusSchema.default("grounded"),
  citations: z.array(z.string()).default([]),
  conversationId: z.string().nullish(),
  source: z.enum(["foundry", "fabric", "none"]).optional(),
  notice: z.string().nullish(),
});
export type AgentResponse = z.infer<typeof agentResponseSchema>;
