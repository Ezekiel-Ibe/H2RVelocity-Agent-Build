// Azure Container Registry (Basic) — hosts the BFF image built during deploy.
param acrName string
param location string
param tags object

resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: acrName
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false
  }
}

output loginServer string = acr.properties.loginServer
output name string = acr.name
output id string = acr.id
