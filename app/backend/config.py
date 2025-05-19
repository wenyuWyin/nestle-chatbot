import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Azure Cognitive Search
    AZURE_SEARCH_SERVICE_NAME = os.getenv("AZURE_SEARCH_SERVICE")
    # AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")
    AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
    AZURE_SEARCH_ADMIN_KEY = os.getenv("AZURE_SEARCH_ADMIN_KEY")
    
    # Azure Cosmos DB
    COSMOS_ACCOUNT = os.getenv("AZURE_COSMOSDB_ACCOUNT")
    COSMOS_DATABASE = os.getenv("AZURE_COSMOSDB_DATABASE")
    COSMOS_CONTAINER = os.getenv("AZURE_COSMOSDB_CONTAINER")
    COSMOS_KEY = os.getenv("AZURE_COSMOSDB_KEY")
    COSMOS_URI = f"https://{COSMOS_ACCOUNT}.documents.azure.com:443/"
    
    # Azure Blob Storage
    BLOB_ACCOUNT = os.getenv("AZURE_BLOB_ACCOUNT")
    BLOB_CONTAINER = os.getenv("AZURE_BLOB_CONTAINER")
    BLOB_ACCOUNT_KEY = os.getenv("AZURE_BLOB_ACCOUNT_KEY")
    BLOB_CONNECTION_STRING = f"DefaultEndpointsProtocol=https;AccountName={BLOB_ACCOUNT};AccountKey={BLOB_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE", "azure")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
    OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", "2023-05-15")
    OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
    
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")

    # Enable CORS for all routes
    CORS_ORIGINS = ["http://localhost:3000"]  # Your React frontend URL
    CORS_METHODS = ["GET", "POST"]