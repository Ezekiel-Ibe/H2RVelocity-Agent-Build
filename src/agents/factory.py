"""
Agent Factory & Azure AI Foundry Registration Manager.
Instantiates and binds the 9 capability agents to Azure AI Foundry projects and endpoints.
"""
import os
import logging
from typing import Dict, Any, Optional
from src.config.settings import settings
from src.agents.a01_workspace_agent import PayrollAssuranceWorkspaceAgent
from src.agents.a02_orchestrator_agent import PayrollAssuranceOrchestratorAgent
from src.agents.a03_data_management_agent import PayrollDataManagementAgent
from src.agents.a04_exception_processing_agent import PayrollExceptionProcessingAgent
from src.agents.a05_analysis_agent import PayrollAnalysisAgent
from src.agents.a06_decision_intelligence_agent import PayrollDecisionIntelligenceAgent
from src.agents.a07_quality_control_agent import PayrollQualityControlAgent
from src.agents.a08_governance_audit_agent import PayrollGovernanceAuditAgent
from src.agents.a09_human_approval_agent import HumanApprovalControlAgent

logger = logging.getLogger("foundry_agent_factory")

class FoundryAgentFactory:
    def __init__(self):
        self.settings = settings
        self.a01 = PayrollAssuranceWorkspaceAgent()
        self.a02 = PayrollAssuranceOrchestratorAgent()
        self.a03 = PayrollDataManagementAgent()
        self.a04 = PayrollExceptionProcessingAgent()
        self.a05 = PayrollAnalysisAgent()
        self.a06 = PayrollDecisionIntelligenceAgent()
        self.a07 = PayrollQualityControlAgent()
        self.a08 = PayrollGovernanceAuditAgent()
        self.a09 = HumanApprovalControlAgent()

    def get_all_agents(self) -> Dict[str, Any]:
        """Returns map of all 9 initialized capability agents."""
        return {
            "A01": self.a01,
            "A02": self.a02,
            "A03": self.a03,
            "A04": self.a04,
            "A05": self.a05,
            "A06": self.a06,
            "A07": self.a07,
            "A08": self.a08,
            "A09": self.a09
        }

    def register_agents_with_azure_ai_foundry(self) -> Dict[str, Any]:
        """
        Provisions or updates the 9 agent definitions in Azure AI Foundry project using azure-ai-projects SDK.
        Falls back smoothly if running in local offline mode.
        """
        registered = {}
        try:
            from azure.identity import DefaultAzureCredential
            from azure.ai.projects import AIProjectClient

            project_client = AIProjectClient.from_connection_string(
                conn_str=f"{self.settings.azure_subscription_id};{self.settings.azure_resource_group};{self.settings.foundry_project_name}",
                credential=DefaultAzureCredential()
            )

            agent_meta = [
                ("A01_Workspace", "src/agents/prompts/a01_workspace.md", "gpt-4o"),
                ("A02_Orchestrator", "src/agents/prompts/a02_orchestrator.md", "gpt-4o"),
                ("A03_DataManagement", "src/agents/prompts/a03_data_management.md", "gpt-4o-mini"),
                ("A04_ExceptionProcessing", "src/agents/prompts/a04_exception_processing.md", "gpt-4o-mini"),
                ("A05_Analysis", "src/agents/prompts/a05_analysis.md", "gpt-4o"),
                ("A06_DecisionIntelligence", "src/agents/prompts/a06_decision_intelligence.md", "gpt-4o"),
                ("A07_QualityControl", "src/agents/prompts/a07_quality_control.md", "gpt-4o-mini"),
                ("A08_GovernanceAudit", "src/agents/prompts/a08_governance_audit.md", "gpt-4o-mini"),
                ("A09_HumanApproval", "src/agents/prompts/a09_human_approval.md", "gpt-4o-mini")
            ]

            for name, prompt_path, model in agent_meta:
                if os.path.exists(prompt_path):
                    with open(prompt_path, "r", encoding="utf-8") as f:
                        instructions = f.read()
                else:
                    instructions = f"Capability agent {name}"

                agent = project_client.agents.create_agent(
                    model=model,
                    name=name,
                    instructions=instructions
                )
                registered[name] = agent.id
                logger.info(f"Registered {name} with Foundry ID: {agent.id}")

            return {"status": "SUCCESS", "registered_agents": registered}

        except Exception as e:
            logger.warning(f"Could not connect to live Azure AI Foundry Project ({e}). Registered in local simulation mode.")
            return {
                "status": "LOCAL_SIMULATION",
                "registered_agents": {
                    "A01": "local-foundry-a01",
                    "A02": "local-foundry-a02",
                    "A03": "local-foundry-a03",
                    "A04": "local-foundry-a04",
                    "A05": "local-foundry-a05",
                    "A06": "local-foundry-a06",
                    "A07": "local-foundry-a07",
                    "A08": "local-foundry-a08",
                    "A09": "local-foundry-a09"
                }
            }

agent_factory = FoundryAgentFactory()
