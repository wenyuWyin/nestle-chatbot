from openai import AzureOpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt


class OpenAIService:
    def __init__(self, endpoint: str, api_key: str, api_version: str):
        self.client = AzureOpenAI(
            azure_endpoint=endpoint, api_key=api_key, api_version=api_version
        )
        self.embedding_deployment = "text-embedding-3-small"
        self.chat_deployment = "gpt-4"

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
    def generate_embedding(self, text: str, dimensions: int = 768) -> list[float]:
        if not text.strip():
            return [0.0] * dimensions

        response = self.client.embeddings.create(
            input=text, model=self.embedding_deployment, dimensions=dimensions
        )
        return response.data[0].embedding

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
    def generate_chat_response(
        self, user_query: str, search_results_context: str, citations: bool
    ) -> str:
        try:
            # Base system prompt
            system_prompt = f"You're a helpful Nestlé recipe assistant. Provide concise answers based on the provided recipes: {search_results_context}"

            # Add citation instructions if enabled

            # Generate the base response
            response = self.client.chat.completions.create(
                model=self.chat_deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query},
                ],
                max_tokens=4096,
                temperature=1.0,
                top_p=1.0,
            )

            print("response is generated from ai")

            # Extract the generated content
            generated_content = response.choices[0].message.content
            print(generated_content)

            # Add formatted citations if enabled

            return generated_content

        except Exception as e:
            print(f"Chat completion failed: {str(e)}")
            return None

