"""
Configuration and Settings module for Microsoft AI Foundry & Microsoft Fabric.
Loads environment variables and sets defaults for Tenant, Subscription, Resource Group.
"""
import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class AppSettings(BaseModel):
    # Azure Configuration
    azure_tenant_id: str = Field(
        default=os.getenv("AZURE_TENANT_ID", "mbsukdemo.com")
    )
    azure_subscription_id: str = Field(
        default=os.getenv("AZURE_SUBSCRIPTION_ID", "853a151d-93f2-492d-aaa3-2058ce27e753")
    )
    azure_resource_group: str = Field(
        default=os.getenv("AZURE_RESOURCE_GROUP", "bsdevVelocityAI2")
    )
    azure_location: str = Field(
        default=os.getenv("AZURE_LOCATION", "uksouth")
    )

    # Azure AI Foundry Configuration
    foundry_project_name: str = Field(
        default=os.getenv("AZURE_AI_FOUNDRY_PROJECT_NAME", "bsdev-velocity-foundry-proj")
    )
    foundry_endpoint: str = Field(
        default=os.getenv("AZURE_AI_FOUNDRY_ENDPOINT", "https://bsdev-velocity-foundry-proj.services.ai.azure.com/api/v1")
    )
    foundry_model_deployment: str = Field(
        default=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4o")
    )
    foundry_embedding_deployment: str = Field(
        default=os.getenv("AZURE_AI_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-3-large")
    )

    # Microsoft Fabric Connection
    fabric_server: str = Field(
        default=os.getenv(
            "FABRIC_SERVER",
            "emmyyfoj4mkuvbfl3hzr2r5wqe-uk5syzrintyuvnan5ivreqn7ku.datawarehouse.fabric.microsoft.com"
        )
    )
    fabric_database: str = Field(
        default=os.getenv("FABRIC_DATABASE", "edm_wh_dev")
    )
    fabric_auth_type: str = Field(
        default=os.getenv("FABRIC_AUTH_TYPE", "ActiveDirectoryDefault")
    )

    # Telemetry
    app_insights_connection_string: str = Field(
        default=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING", "")
    )

    # Anomaly Detection & Assurance Thresholds
    gross_variance_tolerance_pct: float = Field(
        default=float(os.getenv("GROSS_VARIANCE_TOLERANCE_PCT", "0.40"))
    )
    period_risk_high_threshold: float = Field(
        default=float(os.getenv("PERIOD_RISK_HIGH_THRESHOLD", "0.75"))
    )

settings = AppSettings()
