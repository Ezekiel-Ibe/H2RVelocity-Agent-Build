# Architecture

## Overview

The application is a single-page React 19 workspace. It renders a three-region
desktop layout that mirrors the approved visual reference:

1. **Primary navigation** (`src/features/navigation/Sidebar.tsx`) — brand mark,
   navigation items, and user footer.
2. **Main content** (`src/features/home/`) — page header, welcome banner, key
   metric cards, assurance overview, recent exceptions, and active engagements.
3. **Agent workspace** (`src/features/agent-chat/AgentChatPanel.tsx`) — agent
   identity, AI status, suggested prompts, conversation, and composer.

## Data flow

```
MSW mock (dev) ──► fetch /api/dashboard ──► Zod validation ──► TanStack Query ──► components
                                   (later: governed backend at VITE_API_BASE_URL)
```

- `src/contracts/schemas.ts` — Zod runtime contracts + inferred TypeScript types.
- `src/services/dashboardService.ts` — fetches `/api/dashboard` and validates the
  response against the contract at the boundary.
- `src/services/apiConfig.ts` — API base URL + mock toggle (`USE_MOCKS`).
- `src/services/endpoints.ts` — central map of backend paths.
- `src/mocks/` — MSW handlers/worker/server that serve synthetic fixtures over HTTP.
- `src/fixtures/` — synthetic development data only.

### Real backend (Fabric + Foundry)

In real environments the same endpoints are served by a governed
backend-for-frontend (BFF) instead of MSW. The BFF is the only tier that connects
to **Microsoft Fabric** (payroll/assurance tables) and **Microsoft Foundry** (the
Payroll Assurance Agent); it holds all credentials. The frontend holds none and
never contacts Fabric or Foundry directly. Switch over by setting
`VITE_API_BASE_URL` and `VITE_USE_MOCKS=false`. See `docs/api-contracts.md`.

## Styling

- `src/design-system/tokens.css` — design tokens (colour, type, spacing, radius,
  shadow, focus, status, data-viz).
- Feature components use **CSS Modules** and reference tokens via CSS variables.
- Fluent UI v9 provides the component and icon primitives.

## Structure

```
src/
├── app/                # application shell + routing
├── design-system/      # tokens, global styles, brand asset placeholder
├── features/           # feature-oriented UI (navigation, home, agent-chat)
├── services/           # data services (fixtures today, APIs later)
├── contracts/          # Zod schemas + types
├── fixtures/           # synthetic development data
└── test/               # test setup
```
