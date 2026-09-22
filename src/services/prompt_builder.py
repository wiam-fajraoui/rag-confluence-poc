from models.search_result import SearchResult


class PromptBuilder:

    def build_context(
        self,
        search_results: list
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
6. Après chaque affirmation tirée du contexte, ajoute un marqueur de
   citation entre crochets indiquant le numéro du DOCUMENT utilisé,
   par exemple [1] ou [2]. Utilise le numéro du DOCUMENT tel qu'il
   apparaît dans le contexte (DOCUMENT 1, DOCUMENT 2, etc.), jamais
   le nom du fichier. Si une phrase s'appuie sur plusieurs documents,
   indique tous les numéros concernés, par exemple [1][2].
7. Ne génère jamais toi-même de section "Sources" ou "Citations" à
   la fin de ta réponse -- les marqueurs [n] dans le texte suffisent,
   la liste détaillée est construite séparément.

Rédige une réponse claire, concise et professionnelle.
"""

    def build_prompt(
        self,
        question: str,
        search_results: list
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