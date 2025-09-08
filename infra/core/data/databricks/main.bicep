@description('The name of the Azure Databricks workspace to create.')
param workspaceName string

@minLength(1)
@description('Azure region where all resources will be deployed (e.g., "eastus")')
param location string

module dbworkspace 'workspace.bicep' = {
name: 'dbworkspace'
params:{

   location:location
   workspaceName:workspaceName

}
}
