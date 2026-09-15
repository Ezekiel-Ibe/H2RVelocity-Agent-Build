"""
Deployment and Provisioning Script for Microsoft AI Foundry Agents.
Connects to Microsoft AI Foundry Project and registers all 9 capability agents.
"""
import sys
import logging
from src.config.settings import settings
from src.agents.factory import agent_factory

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("deploy_foundry")

def main():
    logger.info("=================================================================")
    logger.info("Deploying 9 HR Capability Agents to Microsoft AI Foundry")
    logger.info(f"Tenant:       {settings.azure_tenant_id}")
    logger.info(f"Subscription: {settings.azure_subscription_id}")
    logger.info(f"Resource Grp: {settings.azure_resource_group}")
    logger.info(f"Foundry Proj: {settings.foundry_project_name}")
    logger.info(f"Fabric Host:  {settings.fabric_server}")
    logger.info(f"Fabric DB:    {settings.fabric_database}")
    logger.info("=================================================================")

    result = agent_factory.register_agents_with_azure_ai_foundry()
    logger.info(f"Deployment Result: {result}")
    if result["status"] != "SUCCESS":
        raise RuntimeError(f"Foundry deployment did not complete successfully: {result['status']}")

    logger.info("All 9 Capability Agents successfully registered in Microsoft Foundry.")

if __name__ == "__main__":
    main()
