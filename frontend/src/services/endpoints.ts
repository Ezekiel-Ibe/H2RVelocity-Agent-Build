/**
 * Central map of backend API paths. These are served by the MSW mock worker in
 * development and by the governed backend-for-frontend (BFF) in real
 * environments. The BFF is the only tier that holds Microsoft Fabric and
 * Microsoft Foundry credentials — the frontend never contacts them directly.
 *
 * To point at real services, set VITE_API_BASE_URL and disable mocks
 * (VITE_USE_MOCKS=false). No component or service code needs to change.
 */
export const endpoints = {
  dashboard: "/api/dashboard",
  cases: "/api/cases",
  caseDetail: (id: string) => `/api/cases/${id}`,
  caseDecision: (id: string) => `/api/cases/${id}/decision`,
  exceptions: "/api/exceptions",
  audit: "/api/audit",
  insights: "/api/insights",
  periods: "/api/periods",
  reset: "/api/admin/reset",
  agentMessages: "/api/agent/messages",
  agentStream: "/api/agent/stream",
  runAssurance: "/api/run-assurance",
} as const;
