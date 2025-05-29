import pathlib
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from services.azure_search_service import AzureSearchService
from services.openai_service import OpenAIService
from data.run_scrape import main as run_scrape
from services.utils.recipe_search_util import (
    initialize_recipe_index,
    update_recipe_index_data,
    recipe_search,
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configuration
    azure_search_endpoint = app.config["AZURE_SEARCH_ENDPOINT"]
    azure_search_index_name = app.config["AZURE_SEARCH_INDEX_NAME"]
    azure_search_admin_key = app.config["AZURE_SEARCH_ADMIN_KEY"]
    azure_search_query_key = app.config["AZURE_SEARCH_API_KEY"]

    openai_api_key = app.config["OPENAI_API_KEY"]
    openai_api_endpoint = app.config["OPENAI_API_ENDPOINT"]
    openai_api_version = app.config["OPENAI_API_VERSION"]

    # JSON file path
    recipe_filepath = pathlib.Path(app.config["OUTPUT_FILEPATH"]) / "recipes.json"

    # Initialize services
    print("starting initializing")
    search_service = AzureSearchService(
        endpoint=azure_search_endpoint,
        index_name=azure_search_index_name,
        admin_key=azure_search_admin_key,
        query_key=azure_search_query_key,
    )
    print("Azure Search Client created successfully")
    embedding_service = OpenAIService(
        endpoint=openai_api_endpoint,
        api_key=openai_api_key,
        api_version=openai_api_version,
    )
    print("Azure OpenAI Client created successfully")

    # Rescrape the data
    run_scrape()
    print("Data scraping is done successfully")
    # initialize_recipe_index(
    #     search_service=search_service,
    #     file_path=recipe_filepath,
    #     embedding_service=embedding_service,
    # )
    update_recipe_index_data(
        search_service=search_service,
        file_path=recipe_filepath,
        embedding_service=embedding_service,
    )

    # Enable CORS
    CORS(app, origins=app.config["CORS_ORIGINS"], methods=app.config["CORS_METHODS"])

    # Register routes
    @app.route("/api/chat", methods=["POST"])
    def chat():
        try:
            data = request.get_json()
            print(f"This is a test response to: {data['message']}")

            response = recipe_search(
                search_service=search_service,
                openai_client=embedding_service,
                query=data["message"],
                citation=False,
            )

            print(response)

            return {"response": response}

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app
