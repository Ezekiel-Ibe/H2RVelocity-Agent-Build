targetScope = 'subscription'

// ==============================================================================
// Payroll Assurance Agent — Azure App Onboard generated infrastructure
// Frontend (Static Web Apps) + FastAPI BFF (Container Apps) + supporting telemetry.
// Reuses an existing Microsoft AI Foundry project (no AI resources provisioned here).
// ==============================================================================

@minLength(1)
@maxLength(64)
param environmentName string

@minLength(1)
param location string = 'uksouth'

@description('Static Web Apps control-plane region (no UK South control plane; served globally via CDN).')
param swaLocation string = 'westeurope'

param sessionId string

param deployedBy string

// createdAt is passed in parameters.json (never utcNow() default — crashes the Portal blade)
param createdAt string

@description('BFF container image. Defaults to a public placeholder; deploy phase rebuilds from bff/Dockerfile via ACR.')
param containerImage string = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'

@description('Existing Microsoft AI Foundry project endpoint the BFF calls for the agent-chat panel.')
param foundryProjectEndpoint string

@description('BFF data source: "fabric" (live, read-only Fabric SQL) or "sample".')
param dataSource string = 'fabric'

@description('Fabric SQL endpoint host for DATA_SOURCE=fabric. Fill post-deploy to serve live data.')
param fabricSqlEndpoint string = ''

@description('Fabric warehouse/database name.')
param fabricDatabase string = 'edm_wh_dev'

var tags = {
  'app-onboard-skill': 'true'
  'app-onboard-session-id': sessionId
  'created-at': createdAt
  environment: environmentName
  'deployed-by': deployedBy
}

var appPort = 8000

// Deterministic resource names (equal to prepare-plan.json.naming.resources[]).
var logName = 'log-${environmentName}'
var appiName = 'appi-${environmentName}'
var uamiName = 'id-${environmentName}'
var acrName = 'cr${replace(environmentName, '-', '')}'
var caeName = 'cae-${environmentName}'
var caName = 'ca-${environmentName}'
var swaName = 'swa-${environmentName}'

resource rg 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: 'rg-${environmentName}'
  location: location
  tags: tags
}

module logAnalytics './modules/log-analytics.bicep' = {
  name: 'log-analytics'
  scope: rg
  params: {
    logName: logName
    location: location
    tags: tags
  }
}

module appInsights './modules/app-insights.bicep' = {
  name: 'app-insights'
  scope: rg
  params: {
    appiName: appiName
    location: location
    tags: tags
    workspaceId: logAnalytics.outputs.id
  }
}

module identity './modules/identity.bicep' = {
  name: 'identity'
  scope: rg
  params: {
    uamiName: uamiName
    location: location
    tags: tags
  }
}

module registry './modules/container-registry.bicep' = {
  name: 'container-registry'
  scope: rg
  params: {
    acrName: acrName
    location: location
    tags: tags
  }
}

module environment './modules/container-app-environment.bicep' = {
  name: 'container-app-environment'
  scope: rg
  params: {
    caeName: caeName
    location: location
    tags: tags
    workspaceCustomerId: logAnalytics.outputs.customerId
    workspaceSharedKey: logAnalytics.outputs.sharedKey
  }
}

module frontend './modules/static-web-app.bicep' = {
  name: 'static-web-app'
  scope: rg
  params: {
    swaName: swaName
    location: swaLocation
    tags: tags
  }
}

module bff './modules/container-app.bicep' = {
  name: 'container-app'
  scope: rg
  params: {
    containerAppName: caName
    location: location
    tags: tags
    environmentId: environment.outputs.id
    containerImage: containerImage
    appPort: appPort
    acrLoginServer: registry.outputs.loginServer
    uamiId: identity.outputs.id
    uamiClientId: identity.outputs.clientId
    allowedOrigin: 'https://${frontend.outputs.defaultHostname}'
    foundryProjectEndpoint: foundryProjectEndpoint
    dataSource: dataSource
    fabricSqlEndpoint: fabricSqlEndpoint
    fabricDatabase: fabricDatabase
    appInsightsConnectionString: appInsights.outputs.connectionString
  }
}

module roleAssignments './modules/role-assignments.bicep' = {
  name: 'role-assignments'
  scope: rg
  params: {
    acrName: acrName
    principalId: identity.outputs.principalId
  }
  dependsOn: [
    registry
  ]
}

output resourceGroupName string = rg.name
output containerAppName string = bff.outputs.name
output bffFqdn string = bff.outputs.fqdn
output staticWebAppName string = frontend.outputs.name
output staticWebAppHostname string = frontend.outputs.defaultHostname
output acrName string = registry.outputs.name
output acrLoginServer string = registry.outputs.loginServer
output uamiClientId string = identity.outputs.clientId
