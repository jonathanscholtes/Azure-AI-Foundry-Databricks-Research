
@description('Name of the Azure AI Foundry  instance')
param accountName string


resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: accountName
}



resource gpt4oDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: account
  name: 'gpt-4o'
  sku: {
    capacity: 80
    name: 'GlobalStandard'
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4o'
      version: '2024-11-20'
    }
    versionUpgradeOption: 'OnceCurrentVersionExpired'
    raiPolicyName: 'Microsoft.DefaultV2'
  }

}

resource embeddingDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: account
  name: 'text-embedding'
  sku: {
    capacity: 120
    name: 'Standard'
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'text-embedding-ada-002'
      version: '2'
    }
    versionUpgradeOption: 'OnceCurrentVersionExpired'
    raiPolicyName: 'Microsoft.DefaultV2'
  }
  dependsOn: [gpt4oDeployment]
}
