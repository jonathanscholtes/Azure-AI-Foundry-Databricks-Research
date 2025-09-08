param accountName string
param location string
param identityName string
param customSubdomain string


@description('Resource ID of the Azure Storage Account')
param storageAccountResourceId string


@description('the Application Insights instance used for monitoring')
param appInsightsName string

// Extract the storage account name from the resource ID
var storageAccountName = last(split(storageAccountResourceId, '/'))

var aiSearchConnectionName = '${accountName}-connection-AzureAISearch'
var storageConnectionName = '${accountName}-connection-Storage'
var appInsightConnectionName = '${accountName}-connection-AppInsight'

resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing= {
  name: identityName
}


resource appInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: appInsightsName
}

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: accountName
  location: location
  sku: {
    name: 'S0'
  }
  kind: 'AIServices'
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}': {}
    }
  }
  properties: {
    apiProperties: {}
    customSubDomainName: customSubdomain
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    allowProjectManagement: true
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
  }
}



resource appInsightsConnection 'Microsoft.CognitiveServices/accounts/connections@2025-06-01' = {
  parent: account
  name: appInsightConnectionName
  properties: {
    authType: 'ApiKey'
    category: 'AppInsights'
    target: appInsights.id
    useWorkspaceManagedIdentity: false
    isSharedToAll: true
    credentials: {
      key: appInsights.properties.InstrumentationKey
    }
    sharedUserList: []
    peRequirement: 'NotRequired'
    peStatus: 'NotApplicable'
    metadata: {
      ApiType: 'Azure'
      ResourceId: appInsights.id
    }
  }
}


resource storageConnection 'Microsoft.CognitiveServices/accounts/connections@2025-06-01' = {
  parent: account
  name: storageConnectionName
  properties: {
     authType: 'AccountManagedIdentity'
    category: 'AzureStorageAccount'
    target: 'https://${storageAccountName}.blob.core.windows.net/'
    useWorkspaceManagedIdentity: false
    isSharedToAll: true
    credentials: {
    clientId: managedIdentity.properties.clientId
    resourceId: managedIdentity.id
  }
    sharedUserList: []
    peRequirement: 'NotRequired'
    peStatus: 'NotApplicable'
    metadata: {
      ApiType: 'Azure'
      ResourceId: storageAccountResourceId
    }
  }
}


resource roleAssignment 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  name: guid(managedIdentity.id, account.id, 'cognitive-services-openai-contributor')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'a001fd3d-188f-4b5d-821b-7da978bf7442') // Cognitive Services OpenAI Contributor role ID
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
  scope:account
}




resource roleAssignmentUser 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  name: guid(managedIdentity.id, account.id, 'cognitive-services-openai-userr')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd') // Cognitive Services OpenAI User role ID
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
  scope:account
}



output aiAccountID string = account.id
output aiAccountTarget string = account.properties.endpoint
output OpenAIEndPoint string = 'https://${accountName}.openai.azure.com'
output aiAccountName string = accountName
