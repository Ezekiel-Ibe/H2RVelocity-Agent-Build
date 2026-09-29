# Decision Log

Records implementation assumptions and architecture decisions.

| ID | Decision | Rationale | Status |
|----|----------|-----------|--------|
| ADR-001 | Use synthetic fixtures validated by Zod until approved API contracts exist | No development endpoints available yet; keeps UI honest about data provenance | Accepted |
| ADR-002 | Provisional brand tokens + placeholder KPMG mark isolated in `design-system/` | Official brand values/asset not supplied; must not present placeholders as official | Superseded (logo) — approved KPMG logo (rgb/white/black) now wired via `KpmgLogo`; colour tokens still provisional |
| ADR-003 | CSS Modules + CSS-variable tokens instead of hard-coded values | Required by plan; keeps theming centralised | Accepted |
| ADR-004 | Home dashboard mirrors the uploaded visual reference (Design 1) | Approved initial visual baseline | Accepted |
| ADR-005 | Agent chat returns a synthetic development response only | Frontend must not invent authoritative payroll results | Accepted |
| ADR-006 | Data reaches the frontend only via a governed backend-for-frontend (BFF); the BFF owns Microsoft Fabric and Microsoft Foundry connections | Frontend must not hold Fabric/Foundry credentials or access them directly (security boundaries) | Accepted |
| ADR-007 | Mock (MSW) vs real backend selected by env (`VITE_API_BASE_URL`, `VITE_USE_MOCKS`); endpoint paths centralised in `services/endpoints.ts` | Swapping synthetic fixtures for Fabric/Foundry-backed data is a config change, not a rewrite | Accepted |
| ADR-008 | This React/Fluent workspace is a **departure** from the Stage 7A Technology Decision (Experience = Copilot Studio + Power Apps/Dataverse) | Built to the requested React stack and the visual reference; treat as prototype/alternative pending Factory Design Authority direction | Accepted (needs FDA) |
| ADR-009 | Domain remodelled from "Engagements" to assurance **Cases** (`case_id`, W01–W20) with the seven approved anomaly classes | Aligns the frontend to Stage 4/5 approved capability and data model | Accepted |

## Assumptions

- Metric values, engagement rows, and exception values shown are **synthetic**
  development fixtures derived from the visual reference, not production data.
- Navigation targets (Tasks, Documents, etc.) are placeholders pending routed
  feature pages.
