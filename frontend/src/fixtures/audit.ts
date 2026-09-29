import type { AuditEvent } from "@/contracts/schemas";

/**
 * SYNTHETIC DEVELOPMENT FIXTURE ONLY — not validated business data.
 * Governance and audit events recorded by A08 (CP08 evidence completeness,
 * CP09 governance logging) and A02 (CP10 closure).
 */
export const auditFixture: AuditEvent[] = [
  {
    id: "AUD-1042",
    timestamp: "30 Apr 2024 16:22",
    caseRef: "PA-2024-0498",
    actor: "A02 Orchestrator",
    action: "Case closed",
    control: "CP10",
    detail: "All actions complete; evidence pack attested.",
  },
  {
    id: "AUD-1041",
    timestamp: "30 Apr 2024 16:20",
    actor: "A08 Governance & Audit",
    caseRef: "PA-2024-0498",
    action: "Audit evidence pack assembled",
    control: "CP08",
    detail: "Manifest EV-01…EV-04 hashed and stored.",
  },
  {
    id: "AUD-1040",
    timestamp: "30 Apr 2024 15:58",
    caseRef: "PA-2024-0498",
    actor: "KPMG User (Payroll Controller)",
    action: "Decision recorded: Approve",
    control: "CP05",
    detail: "Joiner payment authorised after validation.",
  },
  {
    id: "AUD-1039",
    timestamp: "28 May 2024 09:14",
    caseRef: "PA-2024-0512",
    actor: "A05 Analysis",
    action: "Risk scored",
    control: "CP03",
    detail: "Risk 88 (High) with factor breakdown.",
  },
  {
    id: "AUD-1038",
    timestamp: "27 May 2024 22:03",
    caseRef: "PA-2024-0512",
    actor: "A04 Exception Processing",
    action: "Anomaly detected",
    control: "CP02",
    detail: "Rule R-ANOM-LEAVER-STILL-PAID v3.2 matched.",
  },
  {
    id: "AUD-1037",
    timestamp: "27 May 2024 22:01",
    caseRef: "PA-2024-0512",
    actor: "A07 Quality Control",
    action: "Input validated",
    control: "CP01",
    detail: "All required records present for the run.",
  },
];
