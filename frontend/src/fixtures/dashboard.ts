import type { Dashboard, ChatMessage } from "@/contracts/schemas";

/**
 * SYNTHETIC DEVELOPMENT FIXTURES ONLY.
 * These values mirror the approved visual reference. They are NOT validated
 * business results and MUST NOT be used as authoritative payroll data.
 */

export const dashboardFixture: Dashboard = {
  stats: [
    {
      id: "payrolls",
      label: "Payrolls Processed",
      value: "24",
      caption: "This period",
      icon: "payrolls",
      trend: { direction: "up", value: "20%", label: "vs last period" },
    },
    {
      id: "employees",
      label: "Employees Covered",
      value: "3,842",
      caption: "This period",
      icon: "employees",
      trend: { direction: "up", value: "15%", label: "vs last period" },
    },
    {
      id: "exceptions",
      label: "Exceptions Identified",
      value: "56",
      caption: "This period",
      icon: "exceptions",
      trend: { direction: "down", value: "10%", label: "vs last period" },
    },
    {
      id: "score",
      label: "Assurance Score",
      value: "92%",
      caption: "This period",
      icon: "score",
      trend: { direction: "up", value: "8%", label: "vs last period" },
    },
  ],
  overview: {
    score: 92,
    total: 56,
    breakdown: [
      { level: "high", label: "High Risk", count: 7, percentage: 12 },
      { level: "medium", label: "Medium Risk", count: 18, percentage: 32 },
      { level: "low", label: "Low Risk", count: 31, percentage: 56 },
    ],
  },
  exceptions: [
    {
      id: "exc-1",
      anomalyType: "leaver-still-paid",
      severity: "high",
      title: "Leaver still paid",
      employeesAffected: 3,
      count: 3,
    },
    {
      id: "exc-2",
      anomalyType: "unexplained-variance",
      severity: "high",
      title: "Unexplained variance",
      employeesAffected: 5,
      count: 5,
    },
    {
      id: "exc-3",
      anomalyType: "missing-tax-code",
      severity: "medium",
      title: "Missing tax code",
      employeesAffected: 6,
      count: 6,
    },
  ],
  cases: [
    {
      id: "PA-2024-0512",
      workerRef: "WKR-10233",
      workerName: "A. Okafor",
      payrollRunId: "PR-2024-05-UK",
      payPeriod: "May 2024",
      anomalyType: "leaver-still-paid",
      anomalyTitle: "Leaver still paid",
      severity: "high",
      riskScore: 88,
      status: "Awaiting Approval",
      currentStep: "W13 Review Recommendation",
      detectedOn: "27 May 2024",
      lastUpdated: "28 May 2024",
    },
    {
      id: "PA-2024-0509",
      workerRef: "WKR-10044",
      workerName: "S. Kaur",
      payrollRunId: "PR-2024-05-UK",
      payPeriod: "May 2024",
      anomalyType: "duplicate-pay-record",
      anomalyTitle: "Duplicate pay record",
      severity: "medium",
      riskScore: 61,
      status: "Awaiting Approval",
      currentStep: "W14 Approve, Reject or Escalate",
      detectedOn: "26 May 2024",
      lastUpdated: "27 May 2024",
    },
    {
      id: "PA-2024-0498",
      workerRef: "WKR-10120",
      workerName: "L. Chen",
      payrollRunId: "PR-2024-04-UK",
      payPeriod: "Apr 2024",
      anomalyType: "joiner-not-paid",
      anomalyTitle: "Joiner not paid",
      severity: "high",
      riskScore: 74,
      status: "Closed",
      currentStep: "W20 Close Case",
      detectedOn: "29 Apr 2024",
      lastUpdated: "30 Apr 2024",
    },
  ],
};

export const suggestedPrompts: string[] = [
  "Summarize current open cases",
  "Why is the assurance score 92%?",
  "Show high risk anomalies",
  "Explain case PA-2026-0512",
];

export const initialChatMessages: ChatMessage[] = [
  {
    id: "msg-1",
    author: "agent",
    body: "Hello! I'm your Payroll Assurance Agent.\n\nI can help you analyze payroll data, explain exceptions, and provide assurance recommendations.\n\nHow can I assist you today?",
    timestamp: "Just now",
    status: "complete",
  },
];
