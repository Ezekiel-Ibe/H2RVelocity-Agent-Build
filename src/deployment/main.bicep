// ==============================================================================
// Azure Bicep Template: Microsoft AI Foundry & Supporting Services
// Subscription: FO-BSDEV_DYN_AX (853a151d-93f2-492d-aaa3-2058ce27e753)
// Resource Group: bsdevVelocityAI2
// Tenant: mbsukdemo.com
// ==============================================================================

@description('Azure region for deployment')
param location string = 'uksouth'

@description('Prefix for naming resources')
param prefix string = 'bsdev-h2r'

@description('Unique suffix for resource names')
param uniqueSuffix string = uniqueString(resourceGroup().id)

// 1. Log Analytics & Application Insights (Telemetry & AgentOps)
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${prefix}-log-${uniqueSuffix}'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 90
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${prefix}-appi-${uniqueSuffix}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

// 2. Azure Key Vault (Secrets & Credentials for Fabric)
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: take('${prefix}-kv-${uniqueSuffix}', 24)
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
  }
}

// 3. Azure AI Services / AI Foundry Account
resource aiServicesAccount 'Microsoft.CognitiveServices/accounts@2024-04-01-preview' = {
  name: '${prefix}-foundry-${uniqueSuffix}'
  location: location
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    customSubDomainName: '${prefix}-foundry-${uniqueSuffix}'
    publicNetworkAccess: 'Enabled'
  }
}

// 4. Model Deployments in AI Foundry: gpt-4o & text-embedding-3-large
resource gpt4oDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-04-01-preview' = {
  parent: aiServicesAccount
  name: 'gpt-4o'
  sku: {
    name: 'Standard'
    capacity: 30
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4o'
      version: '2024-05-13'
    }
  }
}

resource embeddingDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-04-01-preview' = {
  parent: aiServicesAccount
  name: 'text-embedding-3-large'
  sku: {
    name: 'Standard'
    capacity: 50
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'text-embedding-3-large'
      version: '1'
    }
  }
}

// 5. Azure AI Search (for HMRC Statutory Knowledge Base RAG)
resource searchService 'Microsoft.Search/searchServices@2023-11-01' = {
  name: '${prefix}-srch-${uniqueSuffix}'
  location: location
  sku: {
    name: 'standard'
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    authOptions: {
      aadOrApiKey: {
        aadAuthFailureMode: 'http401WithBearerChallenge'
      }
    }
  }
}

output foundryEndpoint string = aiServicesAccount.properties.endpoint
output foundryAccountName string = aiServicesAccount.name
output appInsightsConnectionString string = appInsights.properties.ConnectionString
output keyVaultName string = keyVault.name
output searchServiceName string = searchService.name
