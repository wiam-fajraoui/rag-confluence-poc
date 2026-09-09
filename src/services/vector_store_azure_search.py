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
)
from azure.search.documents.models import VectorizedQuery

from models.chunk import Chunk
from models.search_result import SearchResult


class VectorStoreAzureSearch:
    """
    Implementation Azure AI Search du stockage/retrieval vectoriel,
    avec la meme interface que les 3 autres : add_chunks(), search(),
    is_empty().

    Point d'attention important : Azure AI Search retourne un score
    de similarite (plus haut = plus pertinent) calcule avec la
    formule score = 1 / (1 + distance_cosinus) -- confirmee
    empiriquement en comparant les scores obtenus sur 3 vecteurs de
    test aux distances cosinus deja connues de pgvector/Qdrant sur
    ces memes vecteurs (concordance exacte). On inverse cette formule
    (distance = (1/score) - 1) pour rester compatible avec le seuil
    de filtrage existant et comparable aux deux autres backends.
    """

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

    def search(self, query_embedding, n_results: int = 3) -> list:

        vector_query = VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=n_results,
            fields="embedding",
        )

        results = self.search_client.search(
            vector_queries=[vector_query],
            select=["id", "content", "source"],
            top=n_results,
        )

        search_results = []

        for r in results:

            score = r["@search.score"]

            # Voir la docstring de la classe pour l'explication de
            # cette conversion.
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