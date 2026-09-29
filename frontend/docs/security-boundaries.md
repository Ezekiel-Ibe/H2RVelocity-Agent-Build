# Security Boundaries

The React application is the presentation and interaction layer only.

## The frontend MUST NOT

- contain authoritative payroll calculation logic;
- determine final control outcomes;
- approve or commit payroll adjustments;
- access Microsoft Fabric directly using privileged credentials;
- expose prompts, secrets, tokens or connection strings;
- place real payroll or personal data in source control;
- invent API fields, business rules, thresholds or approval logic;
- treat fixture data as validated business results.

## The frontend MUST

- perform all authoritative operations through governed backend APIs;
- validate every API response at the boundary (Zod contracts in `src/contracts/`);
- use synthetic fixture data until approved contracts and endpoints exist;
- clearly label synthetic development data as such.

## Data handling

- No secrets are stored in source. `.env*` files are git-ignored.
- The agent chat produces a synthetic development response and performs no
  authoritative reasoning over payroll data.
