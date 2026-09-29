// FastAPI backend-for-frontend on Container Apps (Consumption, scale-to-zero).
// Two-phase image wiring: placeholder first, real ACR image on redeploy.
param containerAppName string
param location string
param tags object
param environmentId string
param containerImage string = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
param appPort int = 8000
param acrLoginServer string
param uamiId string
param uamiClientId string
param allowedOrigin string = ''
param foundryProjectEndpoint string
param dataSource string = 'fabric'
param fabricSqlEndpoint string = ''
param fabricDatabase string = 'edm_wh_dev'
param appInsightsConnectionString string

// Placeholder image listens on 80; the real BFF listens on appPort.
var isPlaceholder = containerImage == 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
var effectivePort = isPlaceholder ? 80 : appPort

resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: containerAppName
  location: location
  tags: tags
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${uamiId}': {}
    }
  }
  properties: {
    managedEnvironmentId: environmentId
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: effectivePort
        allowInsecure: false
        transport: 'auto'
      }
      registries: isPlaceholder ? [] : [
        {
          server: acrLoginServer
          identity: uamiId
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'bff'
          image: containerImage
          resources: {
            cpu: json('1.0')
            memory: '2Gi'
          }
          env: [
            { name: 'PORT', value: string(effectivePort) }
            { name: 'DATA_SOURCE', value: dataSource }
            { name: 'FABRIC_SQL_ENDPOINT', value: fabricSqlEndpoint }
            { name: 'FABRIC_DATABASE', value: fabricDatabase }
            { name: 'CORS_ORIGINS', value: allowedOrigin }
            { name: 'AZURE_EXCLUDE_MANAGED_IDENTITY', value: 'false' }
            { name: 'AZURE_CLIENT_ID', value: uamiClientId }
            { name: 'FOUNDRY_PROJECT_ENDPOINT', value: foundryProjectEndpoint }
            { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: appInsightsConnectionString }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 5
        rules: [
          {
            name: 'http-scale'
            http: {
              metadata: {
                concurrentRequests: '4'
              }
            }
          }
        ]
      }
    }
  }
}

output name string = containerApp.name
output fqdn string = containerApp.properties.configuration.ingress.fqdn
