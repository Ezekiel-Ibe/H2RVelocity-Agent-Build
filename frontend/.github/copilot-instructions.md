# Copilot Instructions — Payroll Assurance Agent Workspace

## Purpose
Frontend presentation/interaction layer for the Payroll Assurance Agent. Synthetic
fixtures only; no authoritative payroll logic.

## Hard rules
- Do not add authoritative payroll calculation, approval, or commit logic.
- Do not access Fabric directly or embed secrets, tokens, or connection strings.
- Do not commit real payroll or personal data.
- Do not invent API fields, thresholds, or business rules. Record gaps in
  `docs/open-questions.md`.
- Do not treat fixtures as validated business results.
- Do not recreate the KPMG logo — use the approved supplied asset.

## Conventions
- React 19 + strict TypeScript. Function components only.
- Fluent UI v9 components before custom interactive components.
- Style with CSS Modules referencing tokens in `src/design-system/tokens.css`.
  No hard-coded colours, type, spacing, radius, or shadows in feature components.
- Validate all API responses with Zod contracts in `src/contracts/`.
- Data fetching via TanStack Query through `src/services/`.
- Target WCAG 2.2 AA (see `docs/accessibility-standard.md`).
