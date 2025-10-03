## 🚀 Explore Sample Notebooks

These notebooks demonstrate building intelligent agents to talk with and analyize the data tables deployed to Azure Databricks, integrates uing OpenAPI, MCP and local tool calling. The agents demonstrated are developed with **Azure AI Foundry**, **Azure AI Agent Service** and an advanced reasoning agent-to-agent orchestration is demonstrated using **Semantic Kenrel Orchestration Framework**.

---

## 📥 Download Workshop Notebooks

Once your environment is up and running, you can download the sample notebooks directly from the GitHub repository using the following commands:

```bash
curl -L https://github.com/jonathanscholtes/Azure-AI-Foundry-Databricks-Research/archive/refs/heads/main.zip -o workshop.zip
unzip workshop.zip
mv Azure-AI-Foundry-Databricks-Research-main/src/Notebooks ./Notebooks
rm -rf Azure-AI-Foundry-Databricks-Research-main workshop.zip
```

This approach downloads only the relevant [src/Notebooks](../src/Notebooks) directory, keeping your workspace clean and lightweight.

---


### ⚙️ Configure Your Environment

To connect your notebooks to your Azure AI resources, create a .env file with your specific service credentials.

#### Steps:

1. Copy `sample.env` to a new file named `.env`
2. Replace the placeholder values with your Azure resource info:

```
# Azure AI Project
PROJECT_ENDPOINT=''
AI_INFERENCE_ENDPOINT='https://[Azure AI Foundry Project].cognitiveservices.azure.com/'
AZURE_OPENAI_ENDPOINT='Endpoint from deployed Azure AI Service or Azure OpenAI Service'
AZURE_OPENAI_API_KEY='Key from deployed Azure AI Service or Azure OpenAI Service'
AZURE_OPENAI_CHAT_MODEL='gpt-4o'
AZURE_OPENAI_API_VERSION='2025-01-01-preview'

# Chat History Store
COSMOSDB_ENDPOINT=''
COSMOSDB_KEY=''
COSMOSDB_DATABASE='chatdatabase'
COSMOSDB_HISTORY_CONTAINER='chathistory'

# Tracing with Azure AI Foundry 
AZURE_INSIGHT_CONNECTION_STRING=''

SEMANTICKERNEL_EXPERIMENTAL_GENAI_ENABLE_OTEL_DIAGNOSTICS_SENSITIVE=true


# API Endpoints
OPENAPI_URL=' https://api-sales-demo-[random].azurewebsites.net/openapi.json'

# MCP Servers
MCP_SERVER_URL='https://ca-mcp-sales-demo-[random].azurecontainerapps.io/mcp'
MCP_SERVER_LABEL='SalesAnalysis'

# Databricks
DATABRICKS_SERVER='The base URL of your Databricks workspace.'
DATABRICKS_HTTP_PATH='The HTTP path to your Databricks SQL warehouse or cluster.'
DATABRICKS_TOKEN='Your personal access token for authenticating with Databricks.'

```
<br/>

3. Create an Environment for Notebooks:

Navigate to the Notebook directory src/Notebooks and follow these steps:

- Create a Python Virtual Environment

```bash
python -m venv venv
```

- Activate the Virtual Environment and Install Dependencies:

```bash
venv\Scripts\activate # On macOS/Linux, use `source venv/bin/activate`
python -m pip install -r requirements.txt
```

--- 

### 📓 Notebooks

### Azure AI Agent Service  

The [Azure AI Agent Service](https://learn.microsoft.com/en-us/azure/ai-services/agents/overview) is a **fully managed agent orchestration platform** that enables developers to build and deploy intelligent agents powered by OpenAI models—without needing to manage infrastructure, model endpoints, or tool execution environments.

It simplifies the creation of **context-aware, tool-using agents** by offering first-class support for OpenAPI, Azure AI Search, function calling, and structured memory.

1. **Agent with OpenAPI Tooling**  
   *Notebook: `01_azure_ai_agent-openapi`*  
   This notebook demonstrates how to create and deploy an Azure AI Agent that connects to an external system via an **OpenAPI 3.0 tool definition**. 

   🔗 [Azure AI Agent Service with OpenAPI Specified Tools](https://learn.microsoft.com/en-us/azure/ai-services/agents/how-to/tools/openapi-spec?tabs=python&pivots=overview)

<br/>

2. **Agent with MCP Integration**  
   *Notebook: `02_azure_ai_agent-mcp`*  
   This notebook shows how to build and run an Azure AI Agent that connects to an external system using the **Model Context Protocol (MCP)**.  

   🔗 [How to use the Model Context Protocol tool](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/model-context-protocol-samples)

<br/>

### Semantic Kernel Agents  

This section demonstrates how to build AI agents with the [Semantic Kernel Agent Framework](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/?pivots=programming-language-python).  
Semantic Kernel is a lightweight SDK for integrating AI into applications, offering built-in support for function calling, memory, planners, and plugins. These features make it easy to embed agentic patterns into any app with flexibility and control.  

The included notebooks, powered by **Azure AI Foundry**, show agents that interact with and analyze data from Azure Databricks using a combination of OpenAPI and MCP reasoning models.  


3. **Agent Plugins with Function Calling**  
   *Notebook: `03_semantic-kernel-azure-ai-agent-plugin`*  
   This notebook demonstrates how to use Semantic Kernel Plugins to enable agents to perform complex tasks through function calling. It shows how to register and invoke custom plugins that extend the agent’s capabilities, allowing integration with APIs, tools, or business logic.

   🔗 [Configuring Agents with Semantic Kernel Plugins](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-functions?pivots=programming-language-python)

 
<br/>

4. **Remote Integration with Semantic Kernel (OpenAPI)**  
   *Notebook: `semantic-kernel_04-azure-ai-mcp-agent`*  
   This notebook demonstrates how to connect to a remote OpenAPI server using Semantic Kernel’s `OpenAPIFunctionExecutionParameters`.  

   🔗 [Learn more: Adding OpenAPI plugins](https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/adding-openapi-plugins)  

<br/>

5. **Remote Integration with Semantic Kernel (MCP)**  
   *Notebook: `05_semantic-kernel-azure-ai-mcp-agent`*  
   This notebook demonstrates how to connect to a remote MCP server using Semantic Kernel’s `MCPStreamableHttpPlugin`. The **Model Context Protocol (MCP)** enables scalable, modular tool integration across distributed systems.  

   In addition, it showcases:  
   - **Azure AI Foundry Observability**: tracing prompts and responses  
   - **Evaluation SDK**: scoring agents on fluency, coherence, and groundedness  
   - **Azure Cosmos DB**: maintaining and storing conversation history  

<br/>


6. **Advanced Agent Orchestration: Analyzing Data**  
   *Notebook: `06_semantic-kernel-azure-ai-seq-agent_local`*  
   This notebook demonstrates a sequential multi-agent pattern with two specialized agents:  
   - **SalesDataAgent** — retrieves relevant data from Azure Databricks in response to user queries  
   - **DataAnalysisAgent** — a reasoning agent that builds on the retrieved results to provide deeper insights  

   🔗 [Learn more: Sequential Orchestration](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/sequential?pivots=programming-language-python)  

<br/>

7. **Advanced Agent Orchestration: Analyzing Data with MCP**  
   *Notebook: `07_semantic-kernel-azure-ai-seq-agent`*  
   This notebook demonstrates a sequential multi-agent pattern with two specialized agents, enhanced with tool calling through the **Model Context Protocol (MCP)**.  

<br/>  

8. **Advanced Agent Orchestration: Analyzing Data with Identity**  
   *Notebook: `08_semantic-kernel-azure-ai-seq-agent_local_identity`*  
   This notebook demonstrates a sequential multi-agent pattern with two specialized agents, while also showing how to connect to **Azure AI Foundry** using user credentials via `DefaultCredentials`.  
