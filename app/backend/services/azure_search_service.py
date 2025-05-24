from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex
from azure.search.documents.models import VectorizedQuery


class AzureSearchService:
    def __init__(
        self,
        endpoint: str,
        index_name: str,
        admin_key: str,
        query_key: str,
    ):
        self.endpoint = endpoint
        self.index_name = index_name
        self.admin_key = admin_key
        self.query_key = query_key

    @property
    def index_client(self) -> SearchIndexClient:
        """For index creation/deletion (admin only)"""
        return SearchIndexClient(
            endpoint=self.endpoint, credential=AzureKeyCredential(self.admin_key)
        )

    def get_data_client(self, admin_operations: bool = False) -> SearchClient:
        """For document operations and queries"""
        credential = (
            AzureKeyCredential(self.admin_key)
            if admin_operations
            else AzureKeyCredential(self.query_key)
        )

        return SearchClient(
            endpoint=self.endpoint, index_name=self.index_name, credential=credential
        )

    def create_index(self, index_schema: SearchIndex) -> bool:
        """Create index if doesn't exist"""
        client = self.index_client
        existing_indexes = list(client.list_index_names())

        if self.index_name not in existing_indexes:
            try:
                client.create_index(index_schema)
                print(f"Created index: {self.index_name}")
            except Exception as e:
                print(f"Failed to create recipe index: {str(e)}")
                return False
        else:
            print(f"Index {self.index_name} already exists")

        return True

    def upload_data(self, documents: any) -> None:
        """Upload data to the index"""
        if (
            self.index_client.get_index_statistics(self.index_name)["document_count"]
            > 0
        ):
            print(f"Index {self.index_name} already contains data")
            return

        # Upload to index
        client = self.get_data_client(admin_operations=True)
        try:
            result = client.upload_documents(documents=documents)
            print(
                f"Uploaded {len(documents)} data. Success: {len([r for r in result if r.succeeded])}"
            )
        except Exception as e:
            print(f"Failed to upload: {str(e)}")

    def update_data(self, documents: any) -> None:
        """Update data to the index"""
        client = self.get_data_client(admin_operations=True)
        # Delete all existing data
        all_ids = [{"id": doc["id"]} for doc in client.search(search_text="*")]
        if all_ids:
            client.delete_documents(documents=all_ids)

        # Upload new data
        self.upload_data(documents=documents)

    def hybrid_search(self, query: str, query_embedding: str, vector_fields: list[str], select: list[str], top_k: int = 3):
        """Perform hybrid (text + vector) search"""
        # Generate query embedding
        client = self.get_data_client()

        vector_query = VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=top_k,
            fields=vector_fields
        )
        results = client.search(
            search_text=query,
            vector_queries=[vector_query],
            top=top_k,
            select=select,
        )
        return [dict(result) for result in results]
