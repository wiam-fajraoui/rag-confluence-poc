from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from models.chunk import Chunk
from models.search_result import SearchResult


class VectorStoreQdrant:
    """
    Implementation Qdrant du stockage/retrieval vectoriel, avec la
    meme interface que VectorStore (ChromaDB) et VectorStorePgvector :
    add_chunks(), search(), is_empty().

    Point d'attention important : Qdrant retourne nativement un score
    de similarite cosinus (plus haut = plus pertinent, proche de 1),
    alors que le reste du pipeline (rag_service.py, seuil de
    filtrage DISTANCE_THRESHOLD) raisonne en distance (plus bas =
    plus pertinent). On convertit donc systematiquement le score en
    distance cosinus (distance = 1 - score) avant de construire les
    SearchResult, pour que le seuil de filtrage existant reste valide
    sans modification et que les resultats restent comparables a
    ceux de pgvector (qui utilise la meme metrique cosinus).
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        embedding_dimension: int = 384,
        collection_name: str = "chunks",
    ):

        self.collection_name = collection_name
        self.embedding_dimension = embedding_dimension

        self.client = QdrantClient(host=host, port=port)

        self._ensure_collection()

    def _ensure_collection(self):

        if not self.client.collection_exists(self.collection_name):

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dimension,
                    distance=Distance.COSINE,
                ),
            )

    def is_empty(self) -> bool:

        info = self.client.get_collection(self.collection_name)
        return info.points_count == 0

    def add_chunks(self, chunks: list):

        points = [
            PointStruct(
                id=self._to_point_id(chunk.id),
                vector=chunk.embedding,
                payload={
                    "chunk_id": chunk.id,
                    "content": chunk.content,
                    "source": chunk.source,
                },
            )
            for chunk in chunks
        ]

        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query_embedding, n_results: int = 3, query_text: str = None) -> list:

        # query_text n'est pas utilise par Qdrant dans cette
        # implementation (pas de recherche hybride ici) -- present
        # uniquement pour garder la meme signature que les 4
        # connecteurs.

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=n_results,
        ).points

        return [
            SearchResult(
                id=point.payload["chunk_id"],
                content=point.payload["content"],
                source=point.payload["source"],
                distance=1 - point.score,
            )
            for point in results
        ]

    @staticmethod
    def _to_point_id(chunk_id: str) -> int:

        import hashlib

        digest = hashlib.sha256(chunk_id.encode("utf-8")).hexdigest()
        return int(digest[:16], 16)