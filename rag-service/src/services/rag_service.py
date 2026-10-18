import re

from connectors.embedding_service import EmbeddingService
from connectors.vector_store import VectorStore
from connectors.llm_service import LLMService
from services.prompt_builder import PromptBuilder
from models.chat_response import ChatResponse
from models.citation import Citation


# Longueur maximale de l'extrait affiche pour chaque citation, pour
# rester lisible dans l'interface (pas le chunk entier).
_EXCERPT_MAX_LENGTH = 160

# Au-dela de ce nombre de sources distinctes retenues, la reponse
# agrege plusieurs sujets (ex. "Quelles sont les bonnes pratiques ?") :
# on precise qu'elle n'est pas exhaustive, car le top-k limite le
# nombre de documents consultes. Fait dans le code plutot que dans le
# prompt : le LLM appliquait cette consigne de facon irreguliere
# (ignoree, puis ajoutee a tort sur une question de comparaison).
_MIN_SOURCES_FOR_PARTIAL_NOTE = 3
_PARTIAL_NOTE = "D'après les documents les plus pertinents trouvés (liste non exhaustive) :\n\n"

# Diversite des sources : on recupere plus de candidats que necessaire,
# puis on garde au plus _MAX_CHUNKS_PER_SOURCE fragments par page dans
# les _N_RESULTS retenus. Sans cette limite, une page riche (ex.
# Ansible.md, 5 fragments sur 5) peut occuper tout le contexte et
# evincer la seconde page d'une question de comparaison.
_N_CANDIDATES = 10
_N_RESULTS = 5
_MAX_CHUNKS_PER_SOURCE = 3


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

    # Seuil pour le mode HYBRIDE (distance = 4.0 - reranker_score).
    #
    # Recalibre sur 5 questions et 19 resultats observes en usage reel :
    #   - passages pertinents (definitions, reponses directes) : 0.53 - 1.88
    #   - passages hors sujet                                   : 2.16 - 2.40
    # Le seuil initial de 1.75 (calibre sur 3 questions seulement)
    # rejetait des definitions indispensables aux questions de
    # comparaison (Ansible 1.77, Prometheus 1.87, Kubernetes 1.88).
    # 2.0 les inclut toutes et garde une marge de 0.16 avant le
    # premier passage hors sujet.
    DISTANCE_THRESHOLD_HYBRID = 2.0

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

        candidates = self.vector_store.search(
            question_embedding,
            n_results=_N_CANDIDATES,
            query_text=question if self.use_hybrid else None,
        )

        search_results = self._diversify(candidates)

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

        # Sources reellement utilisees (citees) par la reponse, et non
        # simplement retenues par la recherche : une question precise
        # peut retenir plusieurs pages proches mais n'en citer qu'une.
        # Pas de mention sur un refus : _extract_citations renvoie alors
        # une liste vide.
        distinct_sources = {citation.source for citation in citations}

        if citations and len(distinct_sources) >= _MIN_SOURCES_FOR_PARTIAL_NOTE:
            print(
                f"\n{len(distinct_sources)} sources distinctes citees : "
                "mention 'liste non exhaustive' ajoutee."
            )
            answer = _PARTIAL_NOTE + answer

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
        
        # Refus explicite sans aucun marqueur : le LLM n'a rien utilise
        # du contexte. Le repli afficherait des sources qui n'ont pas
        # servi a la reponse -> aucune citation.
        if "ne trouve pas cette information" in answer.lower():
            return []

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
    def _diversify(candidates: list) -> list:
        """
        Garde les candidats dans leur ordre de pertinence, en limitant
        le nombre de fragments par source, jusqu'a _N_RESULTS.
        """

        selected = []
        per_source = {}

        for result in candidates:

            if per_source.get(result.source, 0) >= _MAX_CHUNKS_PER_SOURCE:
                continue

            per_source[result.source] = per_source.get(result.source, 0) + 1
            selected.append(result)

            if len(selected) == _N_RESULTS:
                break

        return selected

    @staticmethod
    def _make_excerpt(content: str) -> str:

        flattened = " ".join(content.split())

        if len(flattened) <= _EXCERPT_MAX_LENGTH:
            return flattened

        truncated = flattened[:_EXCERPT_MAX_LENGTH].rsplit(" ", 1)[0]

        return truncated + "…"