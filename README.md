# 🚀 H2RVelocity-Agent-Build
Hire to Retire Agent Development 

A Microsoft AI Foundry and Microsoft Fabric-based multi-agent platform for continuous payroll assurance and hire-to-retire operational governance.

## 🎯 Project purpose

H2RVelocity-Agent-Build is designed to automate and govern payroll exception handling across the hire-to-retire lifecycle. The project models a set of specialist AI agents that work together to collect, analyze, and remediate payroll exceptions while maintaining segregation of duties and governance controls.

The solution is intended for enterprise HR and payroll operations teams that need:

- consistent, auditable payroll assurance processes
- AI-assisted anomaly detection and investigation
- controlled human approval gates for pay-impacting decisions
- traceability for compliance and internal governance
- integration with Azure AI Foundry and Fabric for production-ready deployment

## ⭐ Main features

- Multi-agent workflow spanning nine capability agents from workspace orchestration to governance sign-off
- Continuous payroll assurance pipeline for payroll runs and periods
- Automated anomaly detection and classification for payroll exceptions
- Risk scoring and root-cause analysis for identified issues
- Decision intelligence for recommended remediation options
- Post-correction validation and evidence capture
- Segregation-of-duties checks and approval controls for pay-impacting actions
- Immutable audit manifest generation with SHA-256 hash support
- Azure AI Foundry registration for agent deployment
- Microsoft Fabric connectivity for enterprise data access and telemetry

### 👥 Core agent set

The project includes the following agents:

- A01 - Workspace Agent
- A02 - Orchestrator Agent
- A03 - Data Management Agent
- A04 - Exception Processing Agent
- A05 - Analysis Agent
- A06 - Decision Intelligence Agent
- A07 - Quality Control Agent
- A08 - Governance Audit Agent
- A09 - Human Approval Agent

## 🖥️ Web application (Payroll Assurance Workspace)

In addition to the Python multi-agent platform, the repository includes a **production web application** that surfaces the payroll assurance workflow and its Foundry agents to Payroll Controllers through a governed, three-tier architecture.

### 🏗️ Architecture

```text
React 19 / Vite SPA            FastAPI BFF                     Governed data & agents
(Azure Static Web Apps)  →   (Azure Container Apps)   →   ├─ Microsoft Fabric (read-only, ODBC)
                                                          └─ Microsoft Foundry agents (Responses API)
```

- The **frontend never holds any credentials** — it talks only to the backend-for-frontend (BFF) via `VITE_API_BASE_URL`.
- The **BFF is the only tier** with Microsoft Fabric and Microsoft Foundry connections. It reads Fabric read-only and invokes the Foundry agents on the frontend's behalf.
- All pay-impacting `silver.*` write-back happens under the assurance agent's own managed identity — never the BFF.

### ✨ Application features

- Live dashboard, cases, exceptions, audit trail, and insights sourced from Microsoft Fabric (`edm_wh_dev`)
- **Streaming agent chat** that routes questions through the `payroll-assurance-af` orchestrator to the right capability agent (A01/A03/A05/A06/A08), with the sub-agent narration streamed first
- **Run Assurance** action that invokes the hosted orchestrator agent to execute the end-to-end W01–W20 workflow
- Per-session decision capture (approve / reject / escalate) with graceful fallback to sample data when Fabric capacity is throttled

### 🏃 Running the web app locally

**Backend (BFF):**

```bash
cd bff
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env      # set DATA_SOURCE, Fabric + Foundry endpoints
uvicorn app.main:app --port 8000
```

**Frontend (SPA):**

```bash
cd frontend
npm install
npm run dev                 # uses MSW mock data by default
# To hit a live BFF instead of mocks:
#   set VITE_API_BASE_URL=http://localhost:8000 and VITE_USE_MOCKS=false
```

### 🚀 Deploying the web app to Azure

Infrastructure is defined as Bicep in `infra/` (Container App, Static Web App, Container Registry, user-assigned managed identity, Log Analytics, App Insights).

```bash
# 1. Provision / update infrastructure (subscription-scoped Bicep)
az deployment sub create --location <region> --template-file infra/main.bicep \
  --parameters infra/main.parameters.json

# 2. Build & push the BFF image
az acr build --registry <acrName> --image bff:latest bff

# 3. Build the SPA (bake the BFF URL) and deploy to Static Web Apps
cd frontend
$env:VITE_API_BASE_URL = "https://<bff-container-app-host>"; $env:VITE_USE_MOCKS = "false"
npm run build
npx @azure/static-web-apps-cli deploy dist --app-name <swaName> --env production
```

See [`deploy-brief.md`](deploy-brief.md) for the full deployment brief.

## 🏃 How to run locally

1. Clone the repository:

   ```bash
   git clone https://github.com/Ezekiel-Ibe/H2RVelocity-Agent-Build.git
   cd H2RVelocity-Agent-Build
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   ```bash
   copy .env.example .env
   ```

   Update the values in `.env` for your own Azure tenant, subscription, resource group, AI Foundry project, and Fabric connection.

5. Run the assurance pipeline:

   ```bash
   python run_assurance_pipeline.py
   ```

The default execution simulates a payroll run and prints the anomaly register, period risk summary, and governance telemetry output.

## ⚙️ Environment and setup steps

### 📋 Required configuration

The project loads environment variables from a `.env` file using `python-dotenv`. The repository includes a sample configuration in `.env.example`.

Key settings include:

- Azure tenant and subscription identifiers
- Azure resource group and location
- Azure AI Foundry project and model deployment names
- Microsoft Fabric server and database details
- Application Insights connection string
- variance and risk thresholds used during assurance workflows

Example environment values are defined in `.env.example` and include:

- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`
- `AZURE_RESOURCE_GROUP`
- `AZURE_LOCATION`
- `AZURE_AI_FOUNDRY_PROJECT_NAME`
- `AZURE_AI_FOUNDRY_ENDPOINT`
- `AZURE_AI_MODEL_DEPLOYMENT_NAME`
- `AZURE_AI_EMBEDDING_DEPLOYMENT_NAME`
- `FABRIC_SERVER`
- `FABRIC_DATABASE`
- `FABRIC_AUTH_TYPE`
- `APPLICATIONINSIGHTS_CONNECTION_STRING`
- `GROSS_VARIANCE_TOLERANCE_PCT`
- `PERIOD_RISK_HIGH_THRESHOLD`

### 📦 Local prerequisites

- Python 3.10+
- Azure CLI authentication for service access (if connecting to live resources)
- Access to the target Azure AI Foundry project and Microsoft Fabric environment
- Appropriate RBAC permissions for the tenant and data platform

## 🚀 Deployment details

This repository is structured for deployment in an Azure-based enterprise environment, with AI capability deployment and data plane access separated from orchestration logic.

### 📐 Deployment model

- Azure AI Foundry is used to register and manage the nine capability agents.
- Microsoft Fabric provides the data warehouse context and operational data layer.
- The project uses `azure-ai-projects` and `DefaultAzureCredential` to register agents in the configured AI Foundry project.
- The deployment entry point is:

  ```bash
  python -m src.deployment.deploy_foundry_agents
  ```

### ⚡ Runtime behaviour

When Azure connectivity is available, the system registers the full set of agents in the target AI Foundry project. If live endpoints are unavailable, the application falls back to a local simulation mode.

### 🛡️ Governance and compliance

The implementation is built with controls for:

- human approval checkpoints
- segregation of duties checks
- immutable evidence packs and hash validation
- compliance-oriented audit logging for payroll assurance decisions

## 📞 Contact and contributors

This project is maintained under the `Ezekiel-Ibe/H2RVelocity-Agent-Build` repository.

For questions, issues, or updates:

- Open an issue in the GitHub repository
- Contribute via pull requests
- Contact the repository owner through the GitHub profile associated with the project

Contributions are welcome for documentation improvements, workflow enhancements, governance controls, and deployment automation.

### 🙌 Credits

- **Web application** (React SPA, FastAPI BFF, Azure infrastructure, and the Microsoft Foundry agent integration) designed and developed by **Neil Zahra**.
- Multi-agent platform and Agent Factory stages maintained under the `Ezekiel-Ibe/H2RVelocity-Agent-Build` repository.

## 📁 Repository structure

```text
.
├── .env.example
├── README.md
├── requirements.txt
├── run_assurance_pipeline.py
├── deploy-brief.md
├── src/                     # Python multi-agent platform
│   ├── agents/
│   ├── config/
│   ├── core/
│   ├── deployment/
│   ├── fabric/
│   ├── orchestration/
│   ├── telemetry/
│   └── tests/
├── bff/                     # FastAPI backend-for-frontend (Fabric + Foundry)
├── frontend/                # React 19 / Vite single-page app
├── infra/                   # Bicep infrastructure as code
├── Agent Factory Stages/
└── AgentFactoryStages-Diagrams/
```
