import psycopg2
from psycopg2.extras import execute_values

from models.chunk import Chunk
from models.search_result import SearchResult


class VectorStorePgvector:
    """
    Implementation pgvector du stockage/retrieval vectoriel, avec la
    meme interface que VectorStore (ChromaDB) : add_chunks(), search(),
    is_empty(). Permet de comparer les deux solutions dans le meme
    pipeline, sans modifier rag_service.py ni la logique d'ingestion
    de main.py au-dela du choix du store a instancier.
    """

    def __init__(
        self,
        connection_params: dict,
        embedding_dimension: int = 384,
        table_name: str = "chunks",
    ):

        # La dimension doit correspondre exactement a celle du modele
        # d'embedding utilise (384 pour all-MiniLM-L6-v2, la valeur
        # actuelle du projet). Elle sera differente pour un autre
        # modele (ex. les modeles d'embedding Azure OpenAI).
        self.embedding_dimension = embedding_dimension
        self.table_name = table_name

        self.conn = psycopg2.connect(**connection_params)
        self.conn.autocommit = True

        self._ensure_schema()

    def _ensure_schema(self):

        with self.conn.cursor() as cur:

            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    source TEXT NOT NULL,
                    embedding VECTOR({self.embedding_dimension})
                );
                """
            )

    def is_empty(self) -> bool:

        with self.conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {self.table_name};")
            count = cur.fetchone()[0]

        return count == 0

    def add_chunks(self, chunks: list):

        # Insertion groupee (un seul aller-retour reseau) plutot
        # qu'une boucle d'INSERT individuels -- necessaire pour une
        # comparaison de performance equitable avec ChromaDB et
        # Qdrant, qui recoivent deja leurs chunks en un seul appel
        # (add()/upsert() avec une liste complete).
        values = [
            (
                chunk.id,
                chunk.content,
                chunk.source,
                self._to_vector_literal(chunk.embedding),
            )
            for chunk in chunks
        ]

        with self.conn.cursor() as cur:

            execute_values(
                cur,
                f"""
                INSERT INTO {self.table_name} (id, content, source, embedding)
                VALUES %s
                ON CONFLICT (id) DO UPDATE SET
                    content = EXCLUDED.content,
                    source = EXCLUDED.source,
                    embedding = EXCLUDED.embedding;
                """,
                values,
                template="(%s, %s, %s, %s::vector)",
            )

    def search(self, query_embedding, n_results: int = 3) -> list:

        embedding_literal = self._to_vector_literal(query_embedding)

        with self.conn.cursor() as cur:

            # L'operateur <=> de pgvector calcule une distance
            # cosinus (0 = identique, 2 = oppose), coherente avec le
            # meme principe de "plus petit = plus pertinent" utilise
            # par ChromaDB dans le reste du pipeline.
            cur.execute(
                f"""
                SELECT id, content, source, embedding <=> %s::vector AS distance
                FROM {self.table_name}
                ORDER BY distance
                LIMIT %s;
                """,
                (embedding_literal, n_results),
            )

            rows = cur.fetchall()

        return [
            SearchResult(
                id=row[0],
                content=row[1],
                source=row[2],
                distance=row[3],
            )
            for row in rows
        ]

    @staticmethod
    def _to_vector_literal(embedding) -> str:

        return "[" + ",".join(str(value) for value in embedding) + "]"

    def close(self):

        self.conn.close()