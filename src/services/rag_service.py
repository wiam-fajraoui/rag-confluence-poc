from services.embedding_service import EmbeddingService
from services.vector_store import VectorStore
from services.prompt_builder import PromptBuilder
from services.llm_service import LLMService
from models.chat_response import ChatResponse


class RAGService:

    # Seuil de distance ChromaDB au-delà duquel un résultat est considéré
    # comme non pertinent et n'est pas transmis au LLM.
    #
    # Calibré empiriquement sur la baseline de tests :
    #   - chunks réellement pertinents observés : 0.35 - 0.53
    #   - chunks bruités / hors-sujet observés   : 0.95 - 1.35
    # 0.75 laisse une marge confortable des deux côtés, mais reste une
    # valeur de départ à ajuster si de nouveaux tests révèlent des cas
    # pertinents au-delà de ce seuil (ou des cas non pertinents en-deçà).
    #
    # Limite connue (voir learnings-and-approach) : ce seuil n'est
    # directement valide que pour la metrique de distance de ChromaDB.
    # pgvector/Qdrant utilisent une distance cosinus, Azure AI Search
    # une formule differente -- confirme fonctionner correctement en
    # pratique sur nos tests, mais pas garanti pour tout corpus.
    DISTANCE_THRESHOLD = 0.75

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        prompt_builder: PromptBuilder,
        llm_service: LLMService
    ):

        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.prompt_builder = prompt_builder
        self.llm_service = llm_service

    def ask(self, question: str):

        question_embedding = self.embedding_service.generate_embedding(
            question
        )

        # query_text=question transmis en plus du vecteur : necessaire
        # pour que VectorStoreAzureSearch puisse faire une recherche
        # hybride (mots-cles + vecteur) avec classement semantique,
        # plutot qu'une recherche vectorielle pure. Les 3 autres
        # connecteurs (ChromaDB, pgvector, Qdrant) acceptent ce meme
        # parametre mais l'ignorent, pour garder une interface commune.
        search_results = self.vector_store.search(
            question_embedding,
            n_results=3,
        )

        print("\n" + "=" * 70)
        print("SEARCH RESULTS")
        print("=" * 70)

        for i, result in enumerate(search_results, start=1):

            print(f"\nRésultat {i}")

            print(f"Source   : {result.source}")
            print(f"Distance : {result.distance:.4f}")

            print()

            print(result.content)

            print("-" * 70)

        filtered_results = [
            result
            for result in search_results
            if result.distance <= self.DISTANCE_THRESHOLD
        ]

        print(f"\nRésultats retenus (seuil = {self.DISTANCE_THRESHOLD})\n")

        if not filtered_results:
            print("Aucun résultat sous le seuil.")
        else:
            for result in filtered_results:
                print(
                    f"{result.source} ({result.distance:.4f})"
                )

        if not filtered_results:

            print(
                "\nAucun chunk suffisamment pertinent : "
                "le LLM n'est pas sollicité."
            )

            return ChatResponse(
                answer="Je ne trouve pas cette information dans la documentation.",
                sources=[]
            )

        prompt = self.prompt_builder.build_prompt(
            question,
            filtered_results
        )

        print("\n" + "=" * 70)
        print("PROMPT ENVOYÉ AU LLM")
        print("=" * 70)

        print(prompt)

        answer = self.llm_service.generate_answer(
            prompt
        )

        sources = sorted(
            {
                result.source
                for result in filtered_results
            }
        )

        return ChatResponse(
            answer=answer,
            sources=sources
        )