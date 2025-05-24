import json
import uuid
import re
from ..openai_service import OpenAIService


def load_json_data(file_path: str) -> any:
    """Load data from JSON file"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {str(e)}")
        return None
    

def parse_servings(servings_str: str) -> int:
    """Extracts the numeric portion from servings string"""
    if not servings_str:
        return 1
    
    try:
        servings = int(servings_str)
    except Exception as e:
        print(f"Unexpected data: {e}")
        match = re.search(r"(\d+[,.]?\d*)", servings_str)
        servings = int(match.group(1)) if match else 0
    
    return servings


def prepare_recipe_docs(file_path: str, embedding_service: OpenAIService) -> list[dict]:
    """Prepare recipe documents for Azure AI Search"""

    def convert_time_to_int(time: str) -> int:
        return int(time.replace("mins", "").strip())

    documents = []

    recipes = load_json_data(file_path)
    print("Processing and cleaning data...")
    for recipe in recipes:
        # Basic cleaning
        doc = {
            "id": str(uuid.uuid4()),
            "title": recipe["title"],
            "description": recipe["description"] if recipe["description"] else "",
            "prep_time_min": convert_time_to_int(recipe["prep_time"])
            if recipe["prep_time"]
            else 0,
            "cook_time_min": convert_time_to_int(recipe["cook_time"])
            if recipe["cook_time"]
            else 0,
            "total_time_min": convert_time_to_int(recipe["total_time"])
            if recipe["total_time"]
            else 0,
            "servings": parse_servings(recipe["servings"]),
            "difficulty": recipe["difficulty"] if recipe["difficulty"] else "",
            "ingredients": list(set(recipe["ingredients"])),  # Deduplicate
            "instructions": recipe["instructions"],
            "tags": recipe["tags"],
        }

        # Generate embeddings
        doc["title_vector"] = embedding_service.generate_embedding(recipe["title"])
        doc["ingredients_vector"] = embedding_service.generate_embedding(
            " ".join(recipe["ingredients"])
        )

        documents.append(doc)

    return documents
