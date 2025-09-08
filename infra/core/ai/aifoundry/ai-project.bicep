@description('Azure region of the deployment')
param location string

@description('AI project name')
param aiProjectName string

param aiProjectFriendlyName string

@description('AI project description')
param aiProjectDescription string

param accountName string


resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: accountName
}


resource aiProject 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  parent:account
  name: aiProjectName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {

  }
}



output aiProjectName string = aiProject.name
