"""Runtime configuration loaded from environment / .env."""
import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# Load the .env that sits next to the bff package, regardless of cwd.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
load_dotenv()  # also honour a cwd .env / real environment variables


def _origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:4173")
    return [o.strip() for o in raw.split(",") if o.strip()]


@dataclass(frozen=True)
class Settings:
    data_source: str = os.getenv("DATA_SOURCE", "sample").lower()
    # Accept this repo's FABRIC_SERVER name as well as the BFF's own FABRIC_SQL_ENDPOINT.
    fabric_sql_endpoint: str = os.getenv("FABRIC_SQL_ENDPOINT") or os.getenv("FABRIC_SERVER", "")
    fabric_database: str = os.getenv("FABRIC_DATABASE", "edm_wh_dev")
    cors_origins: list[str] = field(default_factory=_origins)
    # Locally, exclude the VM managed identity so the Azure CLI (az login) is used.
    # In Azure, leave this false so the managed identity is used.
    exclude_managed_identity: bool = (
        os.getenv("AZURE_EXCLUDE_MANAGED_IDENTITY", "false").lower() == "true"
    )
    # Fabric Data Agent (conversational NL Q&A) for the agent-chat panel.
    data_agent_name: str = os.getenv("FABRIC_DATA_AGENT_NAME", "a01_workspace_agent")
    data_agent_url: str = os.getenv("FABRIC_DATA_AGENT_URL", "")
    data_agent_scope: str = os.getenv(
        "FABRIC_DATA_AGENT_SCOPE", "https://api.fabric.microsoft.com/.default"
    )

    # Microsoft Foundry prompt agent that powers the agent-chat panel.
    foundry_project_endpoint: str = os.getenv("FOUNDRY_PROJECT_ENDPOINT") or os.getenv(
        "AZURE_AI_FOUNDRY_ENDPOINT",
        "https://velocity-h2r-proj-resource.services.ai.azure.com/api/projects/velocity-h2r-proj",
    )
    foundry_agent_name: str = os.getenv("FOUNDRY_AGENT_NAME", "payroll-assurance-af")
    foundry_api_version: str = os.getenv("FOUNDRY_API_VERSION", "2025-05-15-preview")
    foundry_scope: str = os.getenv("FOUNDRY_SCOPE", "https://ai.azure.com/.default")

    # payroll-assurance-af Foundry hosted agent (Run Assurance button → synchronous Responses API).
    foundry_endpoint: str = os.getenv(
        "FOUNDRY_ENDPOINT",
        "https://velocity-h2r-proj-resource.services.ai.azure.com/api/projects/velocity-h2r-proj",
    )
    foundry_audience: str = os.getenv("FOUNDRY_AUDIENCE", "https://ai.azure.com/.default")
    foundry_responses_api_version: str = os.getenv("FOUNDRY_RESPONSES_API_VERSION", "2025-11-15-preview")
    assurance_agent_model: str = os.getenv("ASSURANCE_AGENT_MODEL", "payroll-assurance-af")

    @property
    def use_fabric(self) -> bool:
        return self.data_source == "fabric"

    @property
    def use_data_agent(self) -> bool:
        return bool(self.data_agent_url)

    @property
    def use_foundry_agent(self) -> bool:
        return bool(self.foundry_project_endpoint and self.foundry_agent_name)


settings = Settings()
