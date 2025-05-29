from azure.search.documents.indexes.models import (
    SimpleField,
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField,
    SemanticSearch,
)
from ..azure_search_service import AzureSearchService
from ..openai_service import OpenAIService
from .data_prep import prepare_recipe_docs


def create_recipe_index_definition(index_name: str) -> SearchIndex:
    """Define schema for recipe index"""
    fields = [
        SimpleField(name="id", type="Edm.String", key=True),
        SearchField(
            name="title",
            type=SearchFieldDataType.String,
            searchable=True,
            analyzer_name="en.microsoft",
        ),
        SearchField(
            name="description",
            type=SearchFieldDataType.String,
            searchable=True,
            analyzer_name="en.microsoft",
        ),
        # Time fields
        SearchField(
            name="prep_time_min", type=SearchFieldDataType.Int32, filterable=True
        ),
        SearchField(
            name="cook_time_min", type=SearchFieldDataType.Int32, filterable=True
        ),
        SearchField(
            name="total_time_min",
            type=SearchFieldDataType.Int32,
            filterable=True,
            sortable=True,
        ),
        SearchField(name="servings", type=SearchFieldDataType.Int32, filterable=True),
        SearchField(
            name="difficulty", type=SearchFieldDataType.String, filterable=True
        ),
        SearchField(
            name="ingredients",
            type=SearchFieldDataType.Collection(SearchFieldDataType.String),
            searchable=True,
            filterable=True,
            analyzer_name="en.microsoft",
        ),
        SearchField(
            name="instructions",
            type=SearchFieldDataType.Collection(SearchFieldDataType.String),
            searchable=True,
        ),
        SearchField(
            name="tags",
            type=SearchFieldDataType.Collection(SearchFieldDataType.String),
            filterable=True,
            facetable=True,
        ),
        # Vector fields for embeddings
        SearchField(
            name="title_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=768,
            vector_search_profile_name="recipe-vector-config",
        ),
        SearchField(
            name="ingredients_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=768,
            vector_search_profile_name="recipe-vector-config",
        ),
        SearchField(name="url", type=SearchFieldDataType.String),
        SearchField(
            name="scraped_at", type=SearchFieldDataType.DateTimeOffset, sortable=True
        ),
    ]

    vector_search = VectorSearch(
        profiles=[
            VectorSearchProfile(
                name="recipe-vector-config",
                algorithm_configuration_name="recipe-hnsw-config",
            )
        ],
        algorithms=[HnswAlgorithmConfiguration(name="recipe-hnsw-config")],
    )

    semantic_config = SemanticConfiguration(
        name="recipe-semantic-config",
        prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="title"),
            content_fields=[
                SemanticField(field_name="description"),
                SemanticField(field_name="ingredients"),
                SemanticField(field_name="instructions"),
            ],
            keywords_fields=[
                SemanticField(field_name="tags"),
                SemanticField(field_name="ingredients"),
            ],
        ),
    )
    semantic_search = SemanticSearch(configurations=[semantic_config])

    return SearchIndex(
        name=index_name,
        fields=fields,
        vector_search=vector_search,
        semantic_search=semantic_search,
    )


def initialize_recipe_index(
    search_service: AzureSearchService, file_path: str, embedding_service: OpenAIService
) -> None:
    print("=== Azure AI Search Initialization ===")

    # Create indexes
    print("\n1. Creating indexes...")
    index_name = search_service.index_name
    index_schema = create_recipe_index_definition(index_name)
    if not search_service.create_index(index_schema):
        return

    # Upload data
    print("\n2. Uploading recipe data...")
    documents = prepare_recipe_docs(file_path, embedding_service)
    print("Data processing is done successfully")
    search_service.upload_data(documents)

    print("\nInitialization complete!")


def update_recipe_index_data(
    search_service: AzureSearchService, file_path: str, embedding_service: OpenAIService
) -> None:
    print("Updating recipe data...")
    documents = prepare_recipe_docs(file_path, embedding_service)
    search_service.update_data(documents)

    print("\nUpdates complete!")

def recipe_search(search_service: AzureSearchService, openai_client: OpenAIService, query: str, citation: bool = True):
    query_embedding = openai_client.generate_embedding(query)

    print("starting searching")
    search_results = search_service.hybrid_search(query=query,
        query_embedding=query_embedding,
        vector_fields="title_vector,ingredients_vector",
        select=["title", "description", "ingredients", "instructions", "url"])
    
    print("searching is done")
    
    if search_results:
        # Format search results as context
        context = "\n\n".join(
            f"Recipe {i+1}: {result['title']}\n"
            f"Ingredients: {', '.join(result['ingredients'])}\n"
            f"Instructions: {result['instructions']}"
            for i, result in enumerate(search_results))
        
        print("start generate response")
        
        return openai_client.generate_response(user_query=query, context=context, citation=citation)
    
    return "Sorry, I couldn't find matching recipes. Try different keywords."

