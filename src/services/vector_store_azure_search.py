import re

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    HnswParameters,
    VectorSearchProfile,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField,
    SemanticSearch,
)
from azure.search.documents.models import VectorizedQuery

from models.chunk import Chunk
from models.search_result import SearchResult


class VectorStoreAzureSearch:
    """
    Implementation Azure AI Search du stockage/retrieval vectoriel,
    avec la meme interface que les 3 autres : add_chunks(), search(),
    is_empty().

    Effectue une recherche hybride (mots-cles + vecteur) avec
    classement semantique, confirmee fonctionnelle sur le niveau
    Gratuit (voir test_azure_search_hybrid_semantic.py). L'ordre des
    resultats retournes par Azure beneficie donc du reclassement
    semantique.

    Point d'attention important sur la distance retournee : le champ
    "distance" de chaque SearchResult reste calcule a partir du score
    de similarite brut (@search.score), pas du score de reclassement
    semantique (@search.reranker_score). Raison : @search.score suit
    la formule score = 1 / (1 + distance_cosinus) -- confirmee
    empiriquement et compatible avec le seuil de filtrage existant
    (DISTANCE_THRESHOLD = 0.75) et les distances de pgvector/Qdrant.
    @search.reranker_score suit une toute autre echelle (0 a environ
    4, observe empiriquement) et casserait cette comparabilite. On
    profite donc du meilleur classement semantique sans perdre la
    coherence du seuil de filtrage deja calibre.

    Nom de la configuration semantique sur l'index :
    "chunks-semantic-config".
    """

    _SEMANTIC_CONFIG_NAME = "chunks-semantic-config"

    def __init__(
        self,
        endpoint: str,
        api_key: str,
        embedding_dimension: int = 384,
        index_name: str = "chunks",
    ):

        self.index_name = index_name
        self.embedding_dimension = embedding_dimension

        credential = AzureKeyCredential(api_key)

        self.index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
        self.search_client = SearchClient(
            endpoint=endpoint, index_name=index_name, credential=credential
        )

        self._ensure_index()

    def _ensure_index(self):

        fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SearchableField(name="content", type=SearchFieldDataType.String),
            SearchableField(name="source", type=SearchFieldDataType.String, filterable=True),
            SearchField(
                name="embedding",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=self.embedding_dimension,
                vector_search_profile_name="chunks-vector-profile",
            ),
        ]

        # Metrique cosinus, coherente avec pgvector et Qdrant, pour
        # garder les distances comparables entre les 3 backends.
        vector_search = VectorSearch(
            algorithms=[
                HnswAlgorithmConfiguration(
                    name="chunks-hnsw-config",
                    parameters=HnswParameters(metric="cosine"),
                )
            ],
            profiles=[
                VectorSearchProfile(
                    name="chunks-vector-profile",
                    algorithm_configuration_name="chunks-hnsw-config",
                )
            ],
        )

        index = SearchIndex(
            name=self.index_name,
            fields=fields,
            vector_search=vector_search,
            semantic_search=SemanticSearch(
                configurations=[
                    SemanticConfiguration(
                        name=self._SEMANTIC_CONFIG_NAME,
                        prioritized_fields=SemanticPrioritizedFields(
                            content_fields=[SemanticField(field_name="content")],
                        ),
                    )
                ]
            ),
        )

        self.index_client.create_or_update_index(index)

    def is_empty(self) -> bool:

        count = self.search_client.get_document_count()
        return count == 0

    def add_chunks(self, chunks: list):

        documents = [
            {
                "id": self._safe_id(chunk.id),
                "content": chunk.content,
                "source": chunk.source,
                "embedding": chunk.embedding,
            }
            for chunk in chunks
        ]

        self.search_client.upload_documents(documents=documents)

    def search(self, query_embedding, n_results: int = 3, query_text: str = None) -> list:

        vector_query = VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=n_results,
            fields="embedding",
        )

        # Recherche hybride (mots-cles + vecteur) avec classement
        # semantique quand le texte de la question est fourni ;
        # recherche vectorielle pure en repli sinon (comportement
        # d'origine, garde par securite si query_text n'est pas
        # transmis par l'appelant).
        if query_text:

            results = self.search_client.search(
                search_text=query_text,
                vector_queries=[vector_query],
                query_type="semantic",
                semantic_configuration_name=self._SEMANTIC_CONFIG_NAME,
                select=["id", "content", "source"],
                top=n_results,
            )

        else:

            results = self.search_client.search(
                vector_queries=[vector_query],
                select=["id", "content", "source"],
                top=n_results,
            )

        search_results = []

        for r in results:

            # On utilise volontairement @search.score (pas
            # @search.reranker_score) pour le calcul de la distance
            # -- voir la docstring de la classe pour l'explication.
            score = r["@search.score"]

            distance = (1 / score) - 1 if score > 0 else float("inf")

            search_results.append(
                SearchResult(
                    id=r["id"],
                    content=r["content"],
                    source=r["source"],
                    distance=distance,
                )
            )

        return search_results

    @staticmethod
    def _safe_id(chunk_id: str) -> str:

        # Les cles de document Azure AI Search n'acceptent que
        # lettres, chiffres, tiret, underscore et signe egal -- pas
        # d'espaces ni d'accents (possibles dans nos ids de pages
        # Confluence, ex. "Kubernetes Deployment_1").
        return re.sub(r"[^A-Za-z0-9_\-=]", "_", chunk_id)