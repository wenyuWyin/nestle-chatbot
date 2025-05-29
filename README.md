# Nestlé Chatbot

This repository contains an implementation of an AI-based chatbot for the Made With Nestlé website, focusing on recipe data integration with Azure AI Search.

## Implemented Features

- Web scraping of recipe data from Made With Nestlé website
- Azure AI Search integration for vector storage and retrieval
- Flask backend API
- React frontend interface
- Basic chat endpoint for recipe queries

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js
- Azure account with:
  - AI Search service
  - OpenAI service

### Backend Setup

1. Create a `.env` file based on `.env.example` with your Azure credentials
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask server:
    ```bash
    python main.py
    ```

### Frontend Setup
1. Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2. Install dependencies:
    ```bash
    npm install
    ```
3. Start the development server:
    ```bash
    npm start
    ```

## Project Structure
```
backend/              # Flask application with Azure Search integration
  services/           # Azure and OpenAI service wrappers
  data/               # Web scraping functionality
frontend/             # React chatbot interface
config.py             # Configuration settings
```

## Limitations
- Currently only processes recipe data (not full website content)
- Lacks generative AI responses (only vector search implemented)
- Not deployed to Azure (local development only)

## Future Enhancements
- Integrate OpenAI GPT model for generative responses
  - Use paid gpt-3.5-turbo or gpt-4 to generate dynamic responses from retrieved Azure Search content
- Implement GraphRAG module with Cosmos DB
  - Schema Design
    ```mermaid
    graph TD
    A[Category] --> B[Brand]
    B --> C[Product]
    C --> D[Ingredients]
    C --> E[Nutrition_Info]
    ```
- Deploy to Azure App Service
  - Containerize Flask with Docker
  - Deploy to Azure App Service with CI/CD
- Expand scraping to full website content
