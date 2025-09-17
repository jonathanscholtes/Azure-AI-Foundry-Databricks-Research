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

@description('Name of the User Assigned Managed Identity to assign to deployed services')
param identityName string

var storageAccountName ='sa${projectName}${resourceToken}'
var databricksName ='adb-${projectName}-${environmentName}-${resourceToken}'

module storage 'storage/main.bicep' = {
name: 'storage'
params:{
  identityName:identityName
   location:location
   storageAccountName:storageAccountName

}
}


module databricks 'databricks/main.bicep' = {
  name: 'databricks'
  params: {
    location: location
     workspaceName: databricksName
  }

}

module cosmosDb 'cosmosdb/main.bicep' = {
  name: 'cosmosDb'
 
  params: {
    accountName: 'cosmos-${projectName}-${environmentName}-${resourceToken}'
    location: location
    databaseName: 'chatdatabase'
    containers: [
  {
    name: 'chathistory' // Container for storing chat sessions and messages (chat history)
    partitionKeyPaths: [
      '/id' 
    ]
    ttlValue: 86400 // Time-to-live (TTL) for automatic deletion of data after 24 hours (86400 seconds)
    indexingPolicy: {
      automatic: true // Automatically index new data
      indexingMode: 'consistent' // Ensure data is indexed immediately
      includedPaths: [
        {
          path: '/sessionId/?' 
        }
      ]
      excludedPaths: [
        {
          path: '/*' // Exclude all other paths from indexing
        }
      ]
    }
    vectorEmbeddingPolicy: {
      vectorEmbeddings: [] // Placeholder for future vector embedding configuration
    }
  }
 
]
  }
}

output storageAccountName string = storageAccountName
output storageAccountId string = storage.outputs.storageAccountId

