// Log Analytics workspace — central logs for Container Apps + App Insights.
param logName string
param location string
param tags object

resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logName
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

output id string = logAnalyticsWorkspace.id
output customerId string = logAnalyticsWorkspace.properties.customerId
@secure()
output sharedKey string = logAnalyticsWorkspace.listKeys().primarySharedKey
