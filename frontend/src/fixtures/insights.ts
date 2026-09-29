import type { Insights } from "@/contracts/schemas";

// Synthetic development insights (mock mode only).
export const insightsFixture: Insights = {
  assuranceScore: 92,
  summary: {
    totalCases: 56,
    openCases: 25,
    resolvedCases: 31,
    totalAnomalies: 56,
    evidencePacks: 48,
  },
  funnel: [
    { stage: "Detected", count: 12 },
    { stage: "In Analysis", count: 9 },
    { stage: "Awaiting Approval", count: 4 },
    { stage: "Escalated", count: 2 },
    { stage: "Resolved / Closed", count: 31 },
  ],
  anomalyTypes: [
    { type: "Unexplained variance", count: 14, maxRisk: 91 },
    { type: "Unapproved change", count: 8, maxRisk: 55 },
    { type: "Missing tax code", count: 12, maxRisk: 62 },
    { type: "Duplicate pay record", count: 9, maxRisk: 70 },
    { type: "Leaver still paid", count: 7, maxRisk: 88 },
    { type: "Joiner not paid", count: 6, maxRisk: 74 },
  ],
  severityMix: [
    { level: "high", label: "High Risk", count: 7, percentage: 12 },
    { level: "medium", label: "Medium Risk", count: 18, percentage: 32 },
    { level: "low", label: "Low Risk", count: 31, percentage: 56 },
  ],
  topRiskCases: [
    { id: "PA-2026-0512", workerName: "A. Okafor", anomalyTitle: "Leaver still paid", severity: "high", riskScore: 88, status: "Awaiting Approval" },
    { id: "PA-2026-0498", workerName: "L. Chen", anomalyTitle: "Joiner not paid", severity: "high", riskScore: 74, status: "Closed" },
    { id: "PA-2026-0509", workerName: "S. Kaur", anomalyTitle: "Duplicate pay record", severity: "medium", riskScore: 61, status: "Awaiting Approval" },
  ],
  controlActivity: [
    { control: "CP02 Anomaly detection", count: 56 },
    { control: "CP05 Human approval", count: 31 },
    { control: "CP08 Evidence pack", count: 48 },
    { control: "CP10 Case closure", count: 31 },
  ],
};
