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

from models.search_result import SearchResult


class VectorStoreAzureSearch:
    """
    Implementation Azure AI Search du stockage/retrieval vectoriel :
    add_chunks(), search(), is_empty(), delete_pages().

    Chaque fiche porte le champ page_id (identifiant de la page
    d'origine), qui permet de retrouver et supprimer tous les
    fragments d'une page : Azure ne connait que des fiches
    independantes, sans notion de page.

    IMPORTANT : le schema de l'index fait partie du contrat entre
    l'ingestion-service et le rag-service. Ce fichier doit rester
    identique dans les deux services : si le rag-service declarait un
    schema sans page_id, Azure refuserait la mise a jour de l'index
    (un champ existant ne peut pas etre retire).

    Calcul de la distance :
    - mode vectoriel pur (query_text absent) : distance = 1/score - 1
      (score = 1 / (1 + distance_cosinus), confirme empiriquement) ;
    - mode hybride (query_text fourni) : distance = 4 - reranker_score
      (@search.reranker_score, echelle officielle 0 a 4).
    """

    _SEMANTIC_CONFIG_NAME = "chunks-semantic-config"

    # Plafond de fragments recuperes pour UNE page lors d'une
    # suppression : largement au-dessus du nombre de sections d'une
    # page reelle.
    _MAX_CHUNKS_PER_PAGE = 1000

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
            SimpleField(name="page_id", type=SearchFieldDataType.String, filterable=True),
            SearchField(
                name="embedding",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=self.embedding_dimension,
                vector_search_profile_name="chunks-vector-profile",
            ),
        ]

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

        return self.search_client.get_document_count() == 0

    def add_chunks(self, chunks: list):

        # Azure AI Search refuse un lot vide (entre 1 et 32000 actions).
        # Cas reel : une page trop courte peut produire 0 morceau.
        if not chunks:
            return

        documents = [
            {
                "id": self._safe_id(chunk.id),
                "content": chunk.content,
                "source": chunk.source,
                "page_id": getattr(chunk, "page_id", None),
                "embedding": chunk.embedding,
            }
            for chunk in chunks
        ]

        self.search_client.upload_documents(documents=documents)

    def delete_pages(self, page_ids, keep_ids=None) -> int:
        """
        Supprime les fiches des pages donnees, sauf celles dont
        l'identifiant figure dans keep_ids. Retourne le nombre de
        fiches supprimees.

        - Page supprimee dans Confluence : keep_ids vide, toutes ses
          fiches sont supprimees.
        - Page modifiee : keep_ids = identifiants des fragments qui
          viennent d'etre (re)envoyes ; seules les anciennes fiches
          qui n'existent plus (sections retirees) sont supprimees.
          On ne supprime jamais une fiche qu'on vient d'envoyer, ce
          qui evite tout conflit d'ordre entre suppression et envoi.
        """

        keep = {self._safe_id(chunk_id) for chunk_id in (keep_ids or [])}

        to_delete = []

        for page_id in page_ids:

            if not page_id:
                continue

            results = self.search_client.search(
                search_text="*",
                filter=f"page_id eq '{page_id}'",
                select=["id"],
                top=self._MAX_CHUNKS_PER_PAGE,
            )

            to_delete.extend(
                {"id": result["id"]}
                for result in results
                if result["id"] not in keep
            )

        if to_delete:
            self.search_client.delete_documents(documents=to_delete)

        return len(to_delete)

    def search(self, query_embedding, n_results: int = 3, query_text: str = None) -> list:

        vector_query = VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=n_results,
            fields="embedding",
        )

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

            if query_text:
                distance = 4.0 - r["@search.reranker_score"]
            else:
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

        # Azure n'accepte dans les cles que lettres, chiffres, "_", "-", "=".
        return re.sub(r"[^A-Za-z0-9_\-=]", "_", chunk_id)