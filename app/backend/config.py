import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Azure Cognitive Search
    AZURE_SEARCH_SERVICE_NAME = os.getenv("AZURE_SEARCH_SERVICE_NAME")
    AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")
    AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
    AZURE_SEARCH_ADMIN_KEY = os.getenv("AZURE_SEARCH_ADMIN_KEY")
    AZURE_SEARCH_ENDPOINT = f"https://{AZURE_SEARCH_SERVICE_NAME}.search.windows.net/"
        
    # Azure Cosmos DB
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_API_ENDPOINT = os.getenv("OPENAI_API_ENDPOINT")
    OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")

    # Data Filepath
    OUTPUT_FILEPATH = "data/storage/datasets"

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")

    # Enable CORS for all routes
    CORS_ORIGINS = ["http://localhost:3000"]
    CORS_METHODS = ["GET", "POST"]