# Payroll Assurance Agent

KPMG-branded workspace for the Payroll Assurance Agent. The app has two parts:

- **Frontend** (`/`, `src/`) — React + TypeScript presentation layer.
- **BFF** (`bff/`) — a governed Python "backend-for-frontend" that owns the
  Microsoft Fabric (and, later, Microsoft Foundry) connections. The frontend
  never holds connection strings, tokens, or secrets.

The frontend can run against **sample fixtures** (no backend needed) or against
the **BFF serving live Microsoft Fabric data**.

## Tech stack

**Frontend:** React 19 · TypeScript (strict) · Vite · Fluent UI v9 · React Router ·
TanStack Query · CSS Modules + design tokens · Zod · Vitest + React Testing Library.

**BFF:** Python 3.12 · FastAPI · Uvicorn · pyodbc (ODBC Driver 18 for SQL Server) ·
azure-identity (`DefaultAzureCredential`).

## Prerequisites

- Node.js 20+ and npm (see `.nvmrc`).
- To run the BFF against live Fabric: Python 3.12, [`uv`](https://docs.astral.sh/uv/),
  the **ODBC Driver 18 for SQL Server**, the Azure CLI, and read access to the
  Fabric warehouse.

## Run — Option A: frontend only (sample data)

The Vite dev server includes a mock middleware that serves `/api/*` from the
synthetic fixtures in `src/fixtures/`. No backend, no sign-in.

```bash
npm install        # first time only
npm run dev
```

Open the URL printed by Vite (default http://localhost:5173). Ensure there is no
`.env.local`, or that it sets `VITE_USE_MOCKS=true`.

## Run — Option B: frontend + BFF (live Fabric data)

**1. Install BFF dependencies**

```bash
cd bff
uv venv
uv pip install -r requirements.txt
```

**2. Configure the BFF** — copy `bff/.env.example` to `bff/.env` and set:

```ini
DATA_SOURCE=fabric
FABRIC_SQL_ENDPOINT=<your-workspace>.datawarehouse.fabric.microsoft.com
FABRIC_DATABASE=edm_wh_dev
CORS_ORIGINS=http://localhost:5173,http://localhost:4173
# Local dev: skip the VM managed identity so the Azure CLI login is used.
# In Azure, set this to false so the managed identity is used instead.
AZURE_EXCLUDE_MANAGED_IDENTITY=true
```

**3. Sign in** so the BFF can acquire a Fabric token:

```bash
az login
```

**4. Start the BFF** (from `bff/`):

```bash
.venv/Scripts/python -m uvicorn app.main:app --port 8000        # Windows
# .venv/bin/python -m uvicorn app.main:app --port 8000          # macOS/Linux
```

Health check: http://localhost:8000/health should return
`{"status":"ok","dataSource":"fabric"}`.

**5. Point the frontend at the BFF** — create `.env.local` in the repo root:

```ini
VITE_API_BASE_URL=http://localhost:8000
VITE_USE_MOCKS=false
```

**6. Start the frontend** in a second terminal:

```bash
npm run dev
```

Home, Cases, Exceptions, and Audit will now show live Fabric data. To switch back
to offline sample data, set `DATA_SOURCE=sample` in `bff/.env` (or remove
`.env.local` and use Option A).

## Other commands

```bash
npm run build    # type-check + production build
npm run test     # frontend unit tests
```

## Data modes at a glance

| Mode | `bff/.env` `DATA_SOURCE` | `.env.local` `VITE_USE_MOCKS` | Backend needed |
| --- | --- | --- | --- |
| Fixtures (frontend only) | — | `true` (or no file) | No |
| Sample (via BFF) | `sample` | `false` | Yes |
| Live Fabric | `fabric` | `false` | Yes + `az login` |

## Architectural boundaries

The frontend is the presentation and interaction layer only. It must not:

- contain authoritative payroll calculation logic;
- approve or commit payroll adjustments;
- access Fabric directly with privileged credentials;
- expose prompts, secrets, tokens, or connection strings;
- place real payroll or personal data in source control.

The BFF is **read-only** against Fabric (SELECT queries only) and holds all
credentials. Secrets live in `bff/.env` and the root `.env.local` — both are
git-ignored and must never be committed. All fixture and demo data is
**synthetic** and must not be treated as validated business results.

## Structure

See `docs/architecture.md`. Feature folders live under `src/features/`, runtime
contracts under `src/contracts/`, the token-based theme under `src/design-system/`,
and the governed backend under `bff/`.
