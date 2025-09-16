> ⚠️  
> **This project is currently in active development and may contain breaking changes.**  
> Updates and modifications are being made frequently, which may impact stability or functionality. This notice will be removed once development is complete and the project reaches a stable release. 

# Azure AI Foundry Agent Development for Exploring and Reasoning over Databricks 

## Overview  

## 🔧 What You’ll Build

- **Agentic AI with Azure AI Agent Service and Semantic Kernel**  
  Use prebuilt and custom agents to delegate tasks, make decisions, and interact with multiple endpoints - tools. Experiment with orchestration patterns using Semantic Kernel Agent Framework.

- **Integrations with OpenAPI and MCP**  
  Connect your agents to external services, such as Azure Databricks, to perform actions like retrieving live data, triggering workflows, or interacting with apps and systems — leveraging Model Context Protocol (MCP) to define tools once and expose them consistently across scalable, modular architectures.


---


## 🛠️ **Steps**

Follow these key steps to successfully implement and deploy the workshop:

### 1️⃣ [**Setup and Solution Deployment**](docs/deployment.md)  
Step-by-step instructions to deploy **Azure AI Foundry** and all required services for the workshop environment, including:

- **Azure AI Foundry** components: AI Service, AI Hub, Projects, and Compute  
- **Azure Databricks** for agents to send spark queries via tool calling
- **Azure Storage Account** for document storage and data ingestion  
- **Azure Web App** to enable agent interactions via OpenAPI integrations
- **Azure Container Apps**  providing agent tools OpenAPI access

### 3️⃣ [**Hands-On with Agents**](docs/notebooks.md)  
Discover interactive Notebooks and guides that walk you through building intelligent, task-driven agents. These curated resources cover: