> ⚠️  
> **This project is currently in active development and may contain breaking changes.**  
> Updates and modifications are being made frequently, which may impact stability or functionality. This notice will be removed once development is complete and the project reaches a stable release. 

# Azure AI Foundry Agent Development for Exploring and Reasoning over Databricks 


## Overview  

This project demonstrates how to explore and reason over structured data (Databricks) using the **Azure AI Foundry Agent Service** and the **Semantic Kernel Agentic Framework**.  

It includes:  
- Python function tool calling  
- OpenAPI endpoints hosted on Azure App Service  
- Dynamic tool resolution with the **Model Context Protocol (MCP)**, deployed as an HTTP-Streamable remote server on Azure Container Apps  

The solution also highlights **observability** by leveraging **Azure AI Foundry Tracability and Evaluation SDKs** for deeper insights into agent behavior. Additionally, it demonstrates **agent orchestration** with the **Semantic Kernel Orchestration Framework**, enabling advanced reasoning steps for data exploration.  

## Key Features  

- **Agentic AI with Azure AI Agent Service and Semantic Kernel**  
  Build and experiment with prebuilt or custom agents that can delegate tasks, make decisions, and interact with multiple endpoints (tools). Explore orchestration patterns using the Semantic Kernel framework.  

- **Integration with OpenAPI and MCP**  
  Extend agents to external services, such as Azure Databricks, to perform actions like retrieving live data, triggering workflows, or interacting with apps and systems. MCP enables defining tools once and exposing them consistently across scalable, modular architectures.  



![design](/media/design.png)

---



## 🛠️ **Core Steps for Solution Implementation**

Follow these key steps to successfully deploy and configure the solution:

### 1️⃣ [**Deploy the Solution**](docs/deployment.md)
-  Instructions for deploying solution, including prerequisites, configuration steps.   

---


## ♻️ **Clean-Up**

After completing the workshop and testing, ensure you delete any unused Azure resources or remove the entire Resource Group to avoid additional charges.

---

## 📜 License  
This project is licensed under the [MIT License](LICENSE.md), granting permission for commercial and non-commercial use with proper attribution.

---

## Disclaimer  
This workshop and demo application are intended for educational and demonstration purposes. It is provided "as-is" without any warranties, and users assume all responsibility for its use.