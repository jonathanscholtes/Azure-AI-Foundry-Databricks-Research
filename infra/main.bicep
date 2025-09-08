targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name representing the deployment environment (e.g., "dev", "test", "prod", "lab"); used to generate a short, unique hash for each resource')
param environmentName string


@minLength(1)
@maxLength(64)
@description('Name used to identify the project; also used to generate a short, unique hash for each resource')
param projectName string

@description('Token or string used to uniquely identify this resource deployment (e.g., build ID, commit hash)')
param resourceToken string


@minLength(1)
@description('Azure region where all resources will be deployed (e.g., "eastus")')
param location string

resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'rg-${projectName}-${environmentName}-${location}-${resourceToken}'
  location: location
}


module security 'core/security/main.bicep' = {
  name: 'security'
  scope: resourceGroup
  params:{
    keyVaultName: 'kv${projectName}${resourceToken}'
    managedIdentityName: 'id-${projectName}-${environmentName}'
    location: location
  }
  
}

module monitor 'core/monitor/main.bicep' = { 
  name:'monitor'
  scope: resourceGroup
  params:{ 
   location:location 
   logAnalyticsName: 'log-${projectName}-${environmentName}-${resourceToken}'
   applicationInsightsName: 'appi-${projectName}-${environmentName}-${resourceToken}'
  }
}


module data 'core/data/main.bicep' = {
  name: 'data'
  scope: resourceGroup
  params:{
    projectName:projectName
    resourceToken:resourceToken
    environmentName:environmentName
    location: location
    identityName:security.outputs.managedIdentityName
  }
}

module platform 'core/platform/main.bicep' = { 
  name: 'platform'
  scope: resourceGroup
  params: { 
    containerRegistryName: 'cr${projectName}${environmentName}${resourceToken}'
    location:location

  }
}


module ai 'core/ai/main.bicep' = {
  name: 'ai'
  scope: resourceGroup
  params: { 
    projectName:projectName
    environmentName:environmentName
    resourceToken:resourceToken
    location: location
    keyVaultId: security.outputs.keyVaultID
    appInsightsName: monitor.outputs.applicationInsightsName
    identityName:security.outputs.managedIdentityName
    storageAccountId:data.outputs.storageAccountId
    containerRegistryID: platform.outputs.containerRegistryID
  }
}


module apps 'core/app/main.bicep' ={ 
  name: 'apps'
  scope: resourceGroup
  params:{
    projectName:projectName
    environmentName:environmentName
    resourceToken:resourceToken
    location: location
  }
}




output managedIdentityName string = security.outputs.managedIdentityName
output appServicePlanName string = apps.outputs.appServicePlanName 
output resourceGroupName string = resourceGroup.name
output storageAccountName string = data.outputs.storageAccountName 
output logAnalyticsWorkspaceName string = monitor.outputs.logAnalyticsWorkspaceName
output applicationInsightsName string = monitor.outputs.applicationInsightsName
output keyVaultUri string = security.outputs.keyVaultUri
output OpenAIEndPoint string = ai.outputs.OpenAIEndPoint 
output containerRegistryName string = platform.outputs.containerRegistryName

