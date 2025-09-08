
@description('Name used to identify the project; also used to generate a short, unique hash for each resource')
param projectName string

@description('Name representing the deployment environment (e.g., "dev", "test", "prod", "lab"); used to generate a short, unique hash for each resource')
param environmentName string

@description('Token or string used to uniquely identify this resource deployment (e.g., build ID, commit hash)')
param resourceToken string

@description('Azure region where all resources will be deployed (e.g., "eastus")')
param location string

@description('Name of the User Assigned Managed Identity to assign to deployed services')
param identityName string

@description('the Application Insights instance used for monitoring')
param appInsightsName string


@description('Resource ID of the Azure Storage Account used by the solution')
param storageAccountId string


@description('Resource ID of the Key Vault used for storing secrets and connection strings')
param keyVaultId string

@description('Resource ID of the Azure Container Registry used to store container images')
param containerRegistryID string


module aiaccount 'ai-account.bicep' = {
  name: 'aiServices'
  params: {
    accountName: 'fnd-${projectName}-${environmentName}-${resourceToken}'
    location: location
    identityName: identityName
    customSubdomain: 'fnd-${projectName}-${environmentName}-${resourceToken}'
    storageAccountResourceId:storageAccountId
    appInsightsName:appInsightsName
    
  }
}

module aiModels 'ai-models.bicep' = {
  name:'aiModels'
  params:{
    accountName:aiaccount.outputs.aiAccountName
  }
  dependsOn: [aiaccount]
}


module aiProjects 'ai-project.bicep' =  {
  name: 'aiProjects-${environmentName}'
  params: {
    accountName:aiaccount.outputs.aiAccountName
    location: location
    aiProjectName: 'proj-${projectName}-${environmentName}-${resourceToken}'
    aiProjectFriendlyName: 'AI Project - ${projectName}'
    aiProjectDescription: 'Project for Databricks'
  }
  dependsOn:[aiaccount]
}


output aiservicesTarget string = aiaccount.outputs.aiAccountTarget
output OpenAIEndPoint string = aiaccount.outputs.OpenAIEndPoint


