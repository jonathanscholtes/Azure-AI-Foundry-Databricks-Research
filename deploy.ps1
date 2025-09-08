param (
    [string]$Subscription,
    [string]$Location = "eastus2"

)


# Variables
$projectName = "sales"
$environmentName = "demo"
$timestamp = Get-Date -Format "yyyyMMddHHmmss"

function Get-RandomAlphaNumeric {
    param (
        [int]$Length = 12,
        [string]$Seed
    )

    $base62Chars = "abcdefghijklmnopqrstuvwxyz123456789"

    # Convert the seed string to a hash (e.g., MD5)
    $md5 = [System.Security.Cryptography.MD5]::Create()
    $seedBytes = [System.Text.Encoding]::UTF8.GetBytes($Seed)
    $hashBytes = $md5.ComputeHash($seedBytes)

    # Use bytes from hash to generate characters
    $randomString = ""
    for ($i = 0; $i -lt $Length; $i++) {
        $index = $hashBytes[$i % $hashBytes.Length] % $base62Chars.Length
        $randomString += $base62Chars[$index]
    }

    return $randomString
}

# Example usage: Generate a resource token based on a seed
$resourceToken = Get-RandomAlphaNumeric -Length 12 -Seed $timestamp

# Clear account context and configure Azure CLI settings
az account clear
az config set core.enable_broker_on_windows=false
az config set core.login_experience_v2=off

# Login to Azure
az login 
az account set --subscription $Subscription


$deploymentNameInfra = "deployment-demo-sales-infra-$resourceToken"
$templateFile = "infra/main.bicep"

$deploymentOutput = az deployment sub create `
    --name $deploymentNameInfra `
    --location $Location `
    --template-file $templateFile `
    --parameters `
        environmentName=$environmentName `
        projectName=$projectName `
        resourceToken=$resourceToken `
        location=$Location `
    --query "properties.outputs"


# Parse deployment outputs
$deploymentOutputJsonInfra = $deploymentOutput | ConvertFrom-Json
$managedIdentityName = $deploymentOutputJsonInfra.managedIdentityName.value
$appServicePlanName = $deploymentOutputJsonInfra.appServicePlanName.value
$resourceGroupName = $deploymentOutputJsonInfra.resourceGroupName.value
$storageAccountName = $deploymentOutputJsonInfra.storageAccountName.value
$logAnalyticsWorkspaceName = $deploymentOutputJsonInfra.logAnalyticsWorkspaceName.value
$applicationInsightsName = $deploymentOutputJsonInfra.applicationInsightsName.value
$keyVaultUri = $deploymentOutputJsonInfra.keyVaultUri.value
$OpenAIEndPoint = $deploymentOutputJsonInfra.OpenAIEndPoint.value
$containerRegistryName = $deploymentOutputJsonInfra.containerRegistryName.value


# Step 2: Deploy Apps
$deploymentNameApps = "deployment-demo-sales-$resourceToken"
$appsTemplateFile = "infra/app/main.bicep"
$deploymentOutputApps = az deployment sub create  `
    --name $deploymentNameApps `
    --location $Location `
    --template-file $appsTemplateFile `
    --parameters `
        environmentName=$environmentName `
        projectName=$projectName `
        location=$Location `
        resourceGroupName=$resourceGroupName `
        resourceToken=$resourceToken `
        managedIdentityName=$managedIdentityName `
        logAnalyticsWorkspaceName=$logAnalyticsWorkspaceName `
        appInsightsName=$applicationInsightsName `
        appServicePlanName=$appServicePlanName `
        keyVaultUri=$keyVaultUri `
    --query "properties.outputs"


$deploymentOutputJson = $deploymentOutputApps | ConvertFrom-Json
$apiAppName = $deploymentOutputJson.apiAppName.value


Write-Host "Waiting for App Services before pushing code"

$waitTime = 60  # Total wait time in seconds 60

# Display counter
for ($i = $waitTime; $i -gt 0; $i--) {
    Write-Host "`rWaiting: $i seconds remaining..." -NoNewline
    Start-Sleep -Seconds 1
}

Write-Host "`rWait time completed!" 

Set-Location -Path .\scripts

# Deploy Python FastAPI for OpenAPI and GraphQL
Write-Output "*****************************************"
Write-Output "Deploying Python FastAPI from scripts"
Write-Output "If timeout occurs, rerun the following command from scripts:"
Write-Output ".\deploy_api.ps1 -apiAppName $apiAppName -resourceGroupName $resourceGroupName -pythonAppPath ..\src\api"
& .\deploy_api.ps1 -apiAppName $apiAppName -resourceGroupName $resourceGroupName -pythonAppPath "..\src\api"


Set-Location -Path ..


Write-Host "`n✅ Deployment Complete!"