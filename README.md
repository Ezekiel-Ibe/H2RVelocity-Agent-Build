# H2RVelocity-Agent-Build
Hire to Retire Agent Development 

A Microsoft AI Foundry and Microsoft Fabric-based multi-agent platform for continuous payroll assurance and hire-to-retire operational governance.

## Project purpose

H2RVelocity-Agent-Build is designed to automate and govern payroll exception handling across the hire-to-retire lifecycle. The project models a set of specialist AI agents that work together to collect payroll data, validate inputs, detect anomalies, assess risk, recommend corrective actions, enforce governance controls, and maintain an immutable audit trail.

The solution is intended for enterprise HR and payroll operations teams that need:

- consistent, auditable payroll assurance processes
- AI-assisted anomaly detection and investigation
- controlled human approval gates for pay-impacting decisions
- traceability for compliance and internal governance
- integration with Azure AI Foundry and Fabric for production-ready deployment

## Main features

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

### Core agent set

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

## How to run locally

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

## Environment and setup steps

### Required configuration

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

### Local prerequisites

- Python 3.10+
- Azure CLI authentication for service access (if connecting to live resources)
- Access to the target Azure AI Foundry project and Microsoft Fabric environment
- Appropriate RBAC permissions for the tenant and data platform

## Deployment details

This repository is structured for deployment in an Azure-based enterprise environment, with AI capability deployment and data plane access separated from orchestration logic.

### Deployment model

- Azure AI Foundry is used to register and manage the nine capability agents.
- Microsoft Fabric provides the data warehouse context and operational data layer.
- The project uses `azure-ai-projects` and `DefaultAzureCredential` to register agents in the configured AI Foundry project.
- The deployment entry point is:

  ```bash
  python -m src.deployment.deploy_foundry_agents
  ```

### Runtime behaviour

When Azure connectivity is available, the system registers the full set of agents in the target AI Foundry project. If live endpoints are unavailable, the application falls back to a local simulation mode so the workflow can still run for testing and environment validation.

### Governance and compliance

The implementation is built with controls for:

- human approval checkpoints
- segregation of duties checks
- immutable evidence packs and hash validation
- compliance-oriented audit logging for payroll assurance decisions

## Contact and contributors

This project is maintained under the `Ezekiel-Ibe/H2RVelocity-Agent-Build` repository.

For questions, issues, or updates:

- Open an issue in the GitHub repository
- Contribute via pull requests
- Contact the repository owner through the GitHub profile associated with the project

Contributions are welcome for documentation improvements, workflow enhancements, governance controls, and deployment automation.

## Repository structure

```text
.
├── .env.example
├── README.md
├── requirements.txt
├── run_assurance_pipeline.py
├── src/
│   ├── agents/
│   ├── config/
│   ├── core/
│   ├── deployment/
│   ├── fabric/
│   ├── orchestration/
│   ├── telemetry/
│   └── tests/
├── Agent Factory Stages/
└── AgentFactoryStages-Diagrams/
```

