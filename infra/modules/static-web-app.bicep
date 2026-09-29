// Detached Static Web App (Standard) for the React SPA. Deployed via token, not GitHub.
param swaName string
param location string
param tags object

resource staticWebApp 'Microsoft.Web/staticSites@2023-12-01' = {
  name: swaName
  location: location
  tags: tags
  sku: {
    name: 'Standard'
    tier: 'Standard'
  }
  properties: {}
}

output name string = staticWebApp.name
output defaultHostname string = staticWebApp.properties.defaultHostname
