"""
Agent Factory & Azure AI Foundry Registration Manager.
Instantiates and binds the 9 capability agents to Azure AI Foundry projects and endpoints.
"""
import os
import logging
from pathlib import Path
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
            from azure.ai.projects.models import PromptAgentDefinition

            project_client = AIProjectClient(
                endpoint=self.settings.foundry_endpoint,
                credential=DefaultAzureCredential()
            )

            agent_meta = [
                ("a01-workspace", "a01_workspace.md"),
                ("a02-orchestrator", "a02_orchestrator.md"),
                ("a03-data-management", "a03_data_management.md"),
                ("a04-exception-processing", "a04_exception_processing.md"),
                ("a05-analysis", "a05_analysis.md"),
                ("a06-decision-intelligence", "a06_decision_intelligence.md"),
                ("a07-quality-control", "a07_quality_control.md"),
                ("a08-governance-audit", "a08_governance_audit.md"),
                ("a09-human-approval", "a09_human_approval.md")
            ]

            prompt_dir = Path(__file__).resolve().parent / "prompts"
            for name, prompt_file in agent_meta:
                prompt_path = prompt_dir / prompt_file
                if not prompt_path.exists():
                    raise FileNotFoundError(f"Missing prompt file for {name}: {prompt_path}")

                instructions = prompt_path.read_text(encoding="utf-8")

                agent = project_client.agents.create_version(
                    agent_name=name,
                    definition=PromptAgentDefinition(
                        model=self.settings.foundry_model_deployment,
                        instructions=instructions
                    )
                )
                registered[name] = agent.id
                logger.info(f"Registered {name} with Foundry ID: {agent.id}")

            return {"status": "SUCCESS", "registered_agents": registered}

        except Exception as e:
            logger.error("Microsoft Foundry agent registration failed: %s", e)
            if not self.settings.allow_local_simulation:
                raise RuntimeError("Microsoft Foundry agent registration failed") from e

            logger.warning("Continuing in local simulation mode because FOUNDRY_ALLOW_LOCAL_SIMULATION=true")
            return {"status": "LOCAL_SIMULATION", "registered_agents": {f"A0{i}": f"local-foundry-a0{i}" for i in range(1, 10)}}

agent_factory = FoundryAgentFactory()
