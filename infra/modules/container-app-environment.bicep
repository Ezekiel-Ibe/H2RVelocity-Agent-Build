// Container Apps managed environment wired to Log Analytics.
param caeName string
param location string
param tags object
param workspaceCustomerId string
@secure()
param workspaceSharedKey string

resource managedEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: caeName
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: workspaceCustomerId
        sharedKey: workspaceSharedKey
      }
    }
  }
}

output id string = managedEnvironment.id
