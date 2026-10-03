"""
Choix du connecteur de base vectorielle via VECTOR_STORE.

Imports differes (a l'interieur de chaque branche) : seul le client
du backend reellement utilise est charge au demarrage.
"""

import os


def get_vector_store_name() -> str:

    return os.getenv("VECTOR_STORE", "chromadb").strip().lower()


def build_vector_store(storage_name: str, chroma_dir=None):

    name = get_vector_store_name()

    if name == "chromadb":
        from connectors.vector_store import VectorStore
        return VectorStore(persist_directory=chroma_dir)

    if name == "pgvector":
        from connectors.vector_store_pgvector import VectorStorePgvector
        return VectorStorePgvector(
            connection_params={
                "host": os.getenv("PGVECTOR_HOST", "localhost"),
                "port": int(os.getenv("PGVECTOR_PORT", "5432")),
                "dbname": os.getenv("PGVECTOR_DB", "rag_pgvector"),
                "user": os.getenv("PGVECTOR_USER", "postgres"),
                "password": os.getenv("PGVECTOR_PASSWORD"),
            },
            embedding_dimension=384,
            table_name=storage_name,
        )

    if name == "qdrant":
        from connectors.vector_store_qdrant import VectorStoreQdrant
        return VectorStoreQdrant(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", "6333")),
            embedding_dimension=384,
            collection_name=storage_name,
        )

    if name == "azure_search":
        from connectors.vector_store_azure_search import VectorStoreAzureSearch
        return VectorStoreAzureSearch(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            api_key=os.getenv("AZURE_SEARCH_API_KEY"),
            embedding_dimension=384,
            index_name=storage_name.replace("_", "-"),
        )

    raise SystemExit(
        f"VECTOR_STORE='{name}' invalide (attendu : chromadb, pgvector, qdrant, azure_search)."
    )
