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

@description('Resource ID of the Azure Container Registry used to store and manage container images')
param containerRegistryID string


@description('Resource ID of the Key Vault used for storing secrets and connection strings')
param keyVaultId string



module aifoundry 'aifoundry/main.bicep' = {
  name: 'aifoundry'
  params: { 
    location:location
    environmentName: environmentName
    identityName: identityName
    keyVaultId: keyVaultId
    projectName: projectName
    resourceToken: resourceToken
    appInsightsName:appInsightsName
    storageAccountId:storageAccountId
    containerRegistryID: containerRegistryID

  }

}



output aiservicesTarget string = aifoundry.outputs.aiservicesTarget
output OpenAIEndPoint string = aifoundry.outputs.OpenAIEndPoint

