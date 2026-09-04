from models.search_result import SearchResult


class PromptBuilder:

    def build_context(
        self,
        search_results: list[SearchResult]
    ) -> str:

        context = ""

        for index, result in enumerate(search_results, start=1):

            context += f"""
==============================
DOCUMENT {index}

Nom : {result.source}

Contenu :

{result.content}

"""

        return context

    def build_system_prompt(self) -> str:

        return """
Tu es un assistant documentaire.

Le contexte fourni est ta seule source de vérité.

Tu dois respecter STRICTEMENT les règles suivantes :

1. Réponds uniquement avec les informations présentes dans le contexte.
2. N'utilise jamais tes connaissances personnelles.
3. N'invente jamais une commande, un exemple ou une explication.
4. Si une information manque dans le contexte, indique simplement :
   "Je ne trouve pas cette information dans la documentation."
5. Chaque phrase de ta réponse doit être justifiée par le contexte.
6. Ne mentionne jamais les noms des documents.
7. Ne génère jamais une section "Sources".

Rédige une réponse claire, concise et professionnelle.
"""

    def build_prompt(
        self,
        question: str,
        search_results: list[SearchResult]
    ) -> str:

        system_prompt = self.build_system_prompt()

        context = self.build_context(search_results)

        prompt = f"""
{system_prompt}

Contexte :

{context}

Question :

{question}

Réponse :
"""

        return prompt