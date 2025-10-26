# VoiceRAG: Voice-Enabled RAG Application with Azure AI Search and GPT-4o Realtime API

This repository demonstrates how to implement Retrieval Augmented Generation (RAG) in applications with a voice interface, powered by the GPT-4o realtime API for audio. Learn more about this pattern in our [detailed blog post](https://aka.ms/voicerag), and watch the [demo video](https://youtu.be/vXJka8xZ9Ko) to see it in action.

## Table of Contents
* [Features](#features)
* [Architecture Overview](#architecture-diagram)
* [Getting Started](#getting-started)
* [Deploying the App](#deploying-the-app)
* [Local Development](#development-server)
* [Cost Management](#costs)
* [Security](#security)

## Features

* **Voice interface**: The app uses the browser's microphone to capture voice input, and sends it to the backend where it is processed by the Azure OpenAI GPT-4o Realtime API.
* **RAG (Retrieval Augmented Generation)**: The app uses the Azure AI Search service to answer questions about a knowledge base, and sends the retrieved documents to the GPT-4o Realtime API to generate a response.
* **Audio output**: The app plays the response from the GPT-4o Realtime API as audio, using the browser's audio capabilities.
* **Citations**: The app shows the search results that were used to generate the response.

### Architecture Diagram

The `RTClient` in the frontend receives the audio input, sends that to the Python backend which uses an `RTMiddleTier` object to interface with the Azure OpenAI real-time API, and includes a tool for searching Azure AI Search.

![Diagram of real-time RAG pattern](resources/RTMTPattern.png)

This repository includes infrastructure as code and containerization support to deploy the app to various Azure container platforms:
- Azure Container Apps (default deployment)
- Azure Kubernetes Service (AKS)
- Azure App Service for Containers

The application can also be run locally as long as Azure AI Search and Azure OpenAI services are configured.

## Getting Started

To run this application locally, you'll need to install the following prerequisites:

### Prerequisites

* [Azure Developer CLI](https://aka.ms/azure-dev/install)
* [Node.js](https://nodejs.org/)
* [Python >=3.11](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)
* [PowerShell](https://learn.microsoft.com/powershell/scripting/install/installing-powershell) (Windows users only)

**Important Notes:**
- Ensure Python and pip are in your system PATH
- On Windows, verify Python installation by running `python --version`
- On Ubuntu, you may need to run: `sudo apt install python-is-python3`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DomGiorda/azure-realtime-openai
   cd azure-realtime-openai
   ```

2. Continue to [Deploying the App](#deploying-the-app) section.

## Deploying the app

You can deploy this application to different Azure container platforms. By default, the `azd up` command will deploy to Azure Container Apps.

### Default Deployment

1. Login to your Azure account:

    ```shell
    azd auth login
    ```

    For GitHub Codespaces users, if the previous command fails, try:

   ```shell
    azd auth login --use-device-code
    ```

1. Create a new azd environment:

    ```shell
    azd env new
    ```

    Enter a name that will be used for the resource group.
    This will create a new folder in the `.azure` folder, and set it as the active environment for any calls to `azd` going forward.

1. (Optional) This is the point where you can customize the deployment by setting azd environment variables, in order to [use existing services](resources/existing_services.md) or [customize the voice choice](resources/customizing_deploy.md).

1. Run this single command to provision the resources, deploy the code, and setup integrated vectorization for the sample data:

   ```shell
   azd up
   ````

   * **Important**: Beware that the resources created by this command will incur immediate costs, primarily from the AI Search resource. These resources may accrue costs even if you interrupt the command before it is fully executed. You can run `azd down` or delete the resources manually to avoid unnecessary spending.
   * You will be prompted to select two locations, one for the majority of resources and one for the OpenAI resource, which is currently a short list. That location list is based on the [OpenAI model availability table](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#global-standard-model-availability) and may become outdated as availability changes.

## local development

You can run the application locally using Docker Compose.

### Environment Setup

1. Configure environment variables by creating a `.env` file in the root of the project with the following content:

   ```env
      AZURE_CLIENT_ID=
      AZURE_CLIENT_SECRET=
      AZURE_TENANT_ID=
      AZURE_OPENAI_ENDPOINT=
      AZURE_SEARCH_ENDPOINT=
      AZURE_OPENAI_REALTIME_DEPLOYMENT=gpt-4o-realtime-preview
      AZURE_OPENAI_REALTIME_VOICE_CHOICE=alloy
      AZURE_SEARCH_CONTENT_FIELD=chunk
      AZURE_SEARCH_EMBEDDING_FIELD=text-vector    
      AZURE_SEARCH_IDENTIFIER_FIELD=ID
      AZURE_SEARCH_INDEX=voicerag-intvect
      AZURE_SEARCH_SEMANTIC_CONFIGURATION=default
      AZURE_SEARCH_TITLE_FIELD=title
      AZURE_SEARCH_USE_VECTOR_QUERY=True
      RUNNING_IN_PRODUCTION=false
      OPENAI_API_VERSION=
   ```

   Note: For Entra ID authentication, omit the API keys to use your local user credentials or managed identity.

### Starting the Application with Docker Compose

1. Launch the application using Docker Compose:

   ```bash
   docker-compose -f integrations/compose.yaml up --build
   ```

2. Access the application at [http://localhost:8765](http://localhost:8765)

## Cost Management

The application uses several Azure services with varying costs. Use the [Azure pricing calculator](https://azure.com/e/a87a169b256e43c089015fda8182ca87) to estimate costs based on your expected usage.

### Services Used
* **Azure Container Apps**: Consumption plan (1 CPU, 2.0 GB RAM) - [Pricing](https://azure.microsoft.com/pricing/details/container-apps/)
* **Azure OpenAI**: Standard tier (gpt-4o-realtime, text-embedding-3-large) - [Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)
* **Azure AI Search**: Standard tier, 1 replica - [Pricing](https://azure.microsoft.com/pricing/details/search/)
* **Azure Blob Storage**: Standard tier with ZRS - [Pricing](https://azure.microsoft.com/pricing/details/storage/blobs/)
* **Azure Monitor**: Pay-as-you-go - [Pricing](https://azure.microsoft.com/pricing/details/monitor/)

⚠️ **Cost Management Tips:**
- Consider free SKUs for development/testing (with limitations)
- Delete unused resources via Portal or `azd down`
- Monitor usage regularly

## Security

The application implements security best practices:

1. **Managed Identity**: Uses [Azure Managed Identity](https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview) for secure credential management
2. **Secret Management**: Enable [GitHub secret scanning](https://docs.github.com/code-security/secret-scanning/about-secret-scanning) in your repositories

## Additional Notes

>Sample data: The PDF documents used in this demo contain information generated using a language model (Azure OpenAI Service). The information contained in these documents is only for demonstration purposes and does not reflect the opinions or beliefs of Microsoft. Microsoft makes no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability or availability with respect to the information contained in this document. All rights reserved to Microsoft.

## Resources

* [Blog post: VoiceRAG](https://aka.ms/voicerag)
* [Demo video: VoiceRAG](https://youtu.be/vXJka8xZ9Ko)
* [Azure OpenAI Realtime Documentation](https://github.com/Azure-Samples/aoai-realtime-audio-sdk/)