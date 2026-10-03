from openai import AzureOpenAI


class LLMServiceAzureOpenAI:
    """
    Implementation Azure OpenAI du service LLM, avec la meme
    interface que LLMService (Ollama) : generate_answer(prompt).
    Permet de basculer entre les deux sans modifier rag_service.py.
    """

    def __init__(
        self,
        endpoint: str,
        api_key: str,
        deployment_name: str = "gpt-4o-mini",
        api_version: str = "2024-10-21",
    ):

        # La version d'API Azure OpenAI evolue regulierement. Si une
        # erreur mentionne une version non supportee, verifier la
        # valeur actuelle recommandee dans la documentation Microsoft
        # et l'ajuster ici.
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        )

        self.deployment_name = deployment_name

    def generate_answer(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
        )

        return response.choices[0].message.content