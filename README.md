> ⚠️  
> **This project is currently in active development and may contain breaking changes.**  
> Updates and modifications are being made frequently, which may impact stability or functionality. This notice will be removed once development is complete and the project reaches a stable release. 

# Azure AI Foundry Agent Development for Exploring and Reasoning over Databricks 

## Overview  


- **Agentic AI with Azure AI Agent Service and Semantic Kernel**  
  Use prebuilt and custom agents to delegate tasks, make decisions, and interact with multiple endpoints - tools. Experiment with orchestration patterns using Semantic Kernel Agent Framework.

- **Integrations with OpenAPI and MCP**  
  Connect your agents to external services, such as Azure Databricks, to perform actions like retrieving live data, triggering workflows, or interacting with apps and systems — leveraging Model Context Protocol (MCP) to define tools once and expose them consistently across scalable, modular architectures.



![design](/media/design.png)

---



## 🛠️ **Steps**

Follow these key steps to successfully implement and deploy the workshop:

### 1️⃣ [**Setup and Solution Deployment**](docs/deployment.md)  
Step-by-step instructions to deploy **Azure AI Foundry** and all required services for the workshop environment, including:

- **Azure AI Foundry** components: AI Service, AI Hub, Projects, and Compute  
- **Azure Databricks** for agents to send spark queries via tool calling
- **Azure Storage Account** for document storage and data ingestion  
- **Azure Web App** to enable agent interactions via OpenAPI integrations
- **Azure Container Apps**  hosting of remote MCP server for agent dynamic tool calling

---


## ♻️ **Clean-Up**

After completing the workshop and testing, ensure you delete any unused Azure resources or remove the entire Resource Group to avoid additional charges.

---

## 📜 License  
This project is licensed under the [MIT License](LICENSE.md), granting permission for commercial and non-commercial use with proper attribution.

---

## Disclaimer  
This workshop and demo application are intended for educational and demonstration purposes. It is provided "as-is" without any warranties, and users assume all responsibility for its use.