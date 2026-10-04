"""
Construction du pipeline RAG a partir de la configuration (.env), et
verification que le rag-service cible le meme index que
l'ingestion-service.

Anciennement dans main.py : deplace ici pour etre partage entre le
demarrage (main.py) et l'endpoint /health (routes/health.py).
"""

import os
from pathlib import Path

from connectors.embedding_service import EmbeddingService
from connectors.llm_service_factory import build_llm_service
from connectors.vector_store_factory import build_vector_store, get_vector_store_name
from services.prompt_builder import PromptBuilder
from services.rag_service import RAGService


# rag-service/ (en local). Dans le conteneur, CHROMA_DIR est fourni
# par docker-compose.yml.
SERVICE_ROOT = Path(__file__).resolve().parents[2]


def get_data_source() -> str:

    return os.getenv("DATA_SOURCE", "local").strip().lower()


def get_storage_name() -> str:

    # CONTRAT partage avec l'ingestion-service, qui calcule le meme
    # nom a partir de DATA_SOURCE.
    return f"chunks_{get_data_source()}"


def build_pipeline() -> RAGService:

    search_mode = os.getenv("SEARCH_MODE", "vector").strip().lower()

    if search_mode not in ("vector", "hybrid"):
        raise SystemExit(f"SEARCH_MODE='{search_mode}' invalide (attendu : 'vector' ou 'hybrid').")

    chroma_base = Path(os.getenv("CHROMA_DIR", SERVICE_ROOT / "data"))

    return RAGService(
        embedding_service=EmbeddingService(),
        vector_store=build_vector_store(
            get_storage_name(),
            chroma_dir=chroma_base / f"chroma_data_{get_data_source()}",
        ),
        prompt_builder=PromptBuilder(),
        llm_service=build_llm_service(),
        use_hybrid=(search_mode == "hybrid"),
    )


def is_same_index(ingestion_status: dict):
    """
    True/False si l'ingestion-service est joignable : les deux
    services ciblent-ils le meme backend et le meme index ?
    None s'il est injoignable (impossible de verifier).
    """

    if not ingestion_status.get("reachable"):
        return None

    return (
        ingestion_status.get("vector_store") == get_vector_store_name()
        and ingestion_status.get("storage_name") == get_storage_name()
    )
