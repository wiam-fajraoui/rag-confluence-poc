import re

from connectors.embedding_service import EmbeddingService  
from connectors.vector_store import VectorStore            
from services.prompt_builder import PromptBuilder
from connectors.llm_service import LLMService              
from models.citation import Citation


# Longueur maximale de l'extrait affiche pour chaque citation, pour
# rester lisible dans l'interface (pas le chunk entier).
_EXCERPT_MAX_LENGTH = 160


class RAGService:

    # Seuil de distance au-delà duquel un résultat est considéré
    # comme non pertinent et n'est pas transmis au LLM -- pour le
    # mode de recherche VECTORIEL (par défaut).
    #
    # Calibré empiriquement sur la baseline de tests :
    #   - chunks réellement pertinents observés : 0.35 - 0.53
    #   - chunks bruités / hors-sujet observés   : 0.95 - 1.35
    # 0.75 laisse une marge confortable des deux côtés.
    #
    # Limite connue : ce seuil n'est directement valide que pour la
    # metrique de distance "vectorielle pure". pgvector/Qdrant
    # utilisent une distance cosinus, Azure AI Search une formule
    # differente -- confirme fonctionner correctement en pratique sur
    # nos tests, mais pas garanti pour tout corpus.
    DISTANCE_THRESHOLD_VECTOR = 0.75

    # Seuil pour le mode HYBRIDE (mots-cles + vecteur + classement
    # semantique, disponible uniquement avec Azure AI Search).
    #
    # Calibre empiriquement sur la distance derivee de
    # @search.reranker_score (voir vector_store_azure_search.py pour
    # le detail du calcul : distance = 4.0 - reranker_score) :
    #   - cas pertinents observes   : 0.53 - 1.52
    #   - cas hors-sujet observes   : 2.16 - 2.28
    # 1.75 se situe entre les deux. Limite connue (voir dossier
    # d'architecture) : un cas reel observe en usage (distance 1.87)
    # est tombe dans la zone grise jamais couverte par la
    # calibration -- seuil a affiner avec un echantillon plus large.
    DISTANCE_THRESHOLD_HYBRID = 1.75

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        prompt_builder: PromptBuilder,
        llm_service: LLMService,
        use_hybrid: bool = False,
    ):

        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.prompt_builder = prompt_builder
        self.llm_service = llm_service
        self.use_hybrid = use_hybrid

    @property
    def distance_threshold(self):

        return (
            self.DISTANCE_THRESHOLD_HYBRID
            if self.use_hybrid
            else self.DISTANCE_THRESHOLD_VECTOR
        )

    def ask(self, question: str):

        question_embedding = self.embedding_service.generate_embedding(
            question
        )

        search_results = self.vector_store.search(
            question_embedding,
            n_results=3,
            query_text=question if self.use_hybrid else None,
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
            if result.distance <= self.distance_threshold
        ]

        print(f"\nRésultats retenus (seuil = {self.distance_threshold})\n")

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
                citations=[]
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

        citations = self._extract_citations(answer, filtered_results)

        return ChatResponse(
            answer=answer,
            citations=citations
        )

    def _extract_citations(self, answer: str, filtered_results: list) -> list:
        """
        Extrait les citations numerotees [n] reellement inserees par
        le LLM dans sa reponse, et les relie aux chunks correspondants
        (DOCUMENT n dans le prompt = filtered_results[n-1]).

        Repli si le LLM n'a insere aucun marqueur (peut arriver, le
        respect de cette consigne n'est pas garanti a 100% -- voir
        note de calibration dans le dossier d'architecture) : on
        liste alors les sources uniques de filtered_results, sans
        marqueur precis, plutot que de ne rien attribuer du tout.
        """

        cited_numbers = sorted(
            {
                int(match)
                for match in re.findall(r"\[(\d+)\]", answer)
            }
        )

        citations = []

        for number in cited_numbers:

            index = number - 1

            if 0 <= index < len(filtered_results):

                result = filtered_results[index]

                citations.append(
                    Citation(
                        number=number,
                        source=result.source,
                        excerpt=self._make_excerpt(result.content),
                    )
                )

        if citations:
            return citations

        # Repli : aucun marqueur valide trouve dans la reponse.
        seen_sources = set()
        fallback_citations = []

        for i, result in enumerate(filtered_results, start=1):

            if result.source in seen_sources:
                continue

            seen_sources.add(result.source)

            fallback_citations.append(
                Citation(
                    number=i,
                    source=result.source,
                    excerpt=self._make_excerpt(result.content),
                )
            )

        return fallback_citations

    @staticmethod
    def _make_excerpt(content: str) -> str:

        flattened = " ".join(content.split())

        if len(flattened) <= _EXCERPT_MAX_LENGTH:
            return flattened

        truncated = flattened[:_EXCERPT_MAX_LENGTH].rsplit(" ", 1)[0]

        return truncated + "…"