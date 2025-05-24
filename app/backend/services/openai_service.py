from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from tenacity import retry, wait_random_exponential, stop_after_attempt


class OpenAIService:
    def __init__(self, endpoint: str, api_key: str, api_version: str):
        self.search_client = AzureOpenAI(
            azure_endpoint=endpoint, api_key=api_key, api_version=api_version
        )
        self.embedding_deployment = "text-embedding-3-small"

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
    def generate_embedding(self, text: str, dimensions: int = 768) -> list[float]:
        """
        Generate vector embedding for text using Azure OpenAI.

        Args:
            text: Input text to embed
            dimensions: Output dimensions (1536 for large, 768 for small)

        Returns:
            List of floats representing the embedding
            Zero vector if input is empty
        """
        if not text.strip():
            return [0.0] * dimensions

        response = self.search_client.embeddings.create(
            input=text, model=self.embedding_deployment, dimensions=dimensions
        )
        return response.data[0].embedding

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
    def generate_chat_response(
        self, user_query: str, search_results_context: str, citations: bool
    ) -> str:
        """
        Generate chat completion using GPT-3.5 Turbo.

        Args:
            messages: Conversation history in OpenAI format
            max_tokens: Maximum response length
            temperature: Creativity control (0-2)

        Returns:
            Generated response text or None if failed
        """
        try:
            # # Base system prompt
            # system_prompt = f"You're a helpful Nestlé recipe assistant. Provide concise answers based on the provided recipes: {search_results_context}"

            # # Add citation instructions if enabled
            # if citations:
            #     system_prompt += (
            #         " When referencing recipes, cite them numerically like [1][2] "
            #         "matching their order in the provided context."
            #     )

            # Generate the base response
            response = self.gpt_client.chat.completions.create(
                model=self.chat_deployment,
                # messages=[
                #     {"role": "system", "content": system_prompt},
                #     {"role": "user", "content": user_query},
                # ],
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant.",
                    },
                    {
                        "role": "user",
                        "content": "I am going to Paris, what should I see?",
                    }
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
            if citations:
                # Parse the search results to extract titles and URLs
                citations_list = []
                for i, result in enumerate(search_results_context.split("\n\n")):
                    if "Recipe " in result:
                        title = result.split("Recipe ")[1].split("\n")[0]
                        url = ""
                        if "URL:" in result:
                            url = result.split("URL: ")[1].split("\n")[0]
                        citations_list.append(
                            f"[{i + 1}] {title} ({url})"
                            if url
                            else f"[{i + 1}] {title}"
                        )

                # Append citations if we found any
                if citations_list:
                    generated_content += "\n\nSources:\n" + "\n".join(citations_list)

            return generated_content

        except Exception as e:
            print(f"Chat completion failed: {str(e)}")
            return None

