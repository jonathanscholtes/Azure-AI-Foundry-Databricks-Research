targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name representing the deployment environment (e.g., "dev", "test", "prod", "lab"); used to generate a short, unique hash for each resource')
param environmentName string

@minLength(1)
@maxLength(64)
@description('Name used to identify the project; also used to generate a short, unique hash for each resource')
param projectName string

@minLength(1)
@description('Azure region where all resources will be deployed (e.g., "eastus")')
param location string

@description('Name of the resource group where resources will be deployed')
param resourceGroupName string

@description('Token or string used to uniquely identify this resource deployment (e.g., build ID, commit hash)')
param resourceToken string

@description('Name of the User Assigned Managed Identity to assign to deployed services')
param managedIdentityName string

@description('Name of the Log Analytics Workspace for centralized monitoring')
param logAnalyticsWorkspaceName string

@description('Name of the Application Insights instance for telemetry')
param appInsightsName string

@description('Name of the App Service Plan for hosting web apps or APIs')
param appServicePlanName string

@description('Name of the Azure Key Vault used to store secrets and keys securely')
param keyVaultUri string

resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-03-01' existing =  {
  name: resourceGroupName
}



module apiWebApp 'api-web-app.bicep' = {
  name: 'apiWebApp'
  scope: resourceGroup
  params: { 
    location: location
    identityName: managedIdentityName
    webAppName: 'api-${projectName}-${environmentName}-${resourceToken}'
    appServicePlanName: appServicePlanName
    logAnalyticsWorkspaceName: logAnalyticsWorkspaceName
    appInsightsName: appInsightsName
    keyVaultUri:keyVaultUri
  }
}


output apiAppName string =  apiWebApp.outputs.webAppName
