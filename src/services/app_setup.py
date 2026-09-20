"""
Construction du service RAG configure (chargement .env, choix des
backends, ingestion/synchronisation, assemblage final).

Cette logique etait avant ecrite directement dans main.py. Elle est
extraite ici pour etre partagee entre main.py (script en ligne de
commande) et api.py (serveur FastAPI) -- eviter de dupliquer ~200
lignes de configuration dans deux fichiers, qui auraient fini par
diverger l'un de l'autre au fil des evolutions.
"""

import os
import time
from pathlib import Path

from dotenv import load_dotenv

from services.document_loader import DocumentLoader
from services.confluence_loader import ConfluenceLoader
from services.sync_state import SyncStateStore
from services.chunker import Chunker
from services.embedding_service import EmbeddingService
from services.vector_store import VectorStore
from services.vector_store_pgvector import VectorStorePgvector
from services.vector_store_qdrant import VectorStoreQdrant
from services.vector_store_azure_search import VectorStoreAzureSearch
from services.prompt_builder import PromptBuilder
from services.llm_service import LLMService
from services.llm_service_azure_openai import LLMServiceAzureOpenAI
from services.rag_service import RAGService


def build_rag_service(base_dir: Path = None) -> RAGService:
    """
    Charge la configuration, effectue l'ingestion/synchronisation
    necessaire, et retourne un RAGService pret a repondre aux
    questions.
    """

    if base_dir is None:
        # src/services/app_setup.py -> remonte de 2 niveaux pour
        # atteindre la racine du projet (meme convention que
        # l'ancien main.py).
        base_dir = Path(__file__).resolve().parent.parent.parent

    docs_dir = base_dir / "docs"

    load_dotenv(base_dir / ".env")

    data_source = os.getenv("DATA_SOURCE", "local").strip().lower()
    chroma_dir = base_dir / f"chroma_data_{data_source}"
    vector_store_name = os.getenv("VECTOR_STORE", "chromadb").strip().lower()
    storage_name = f"chunks_{data_source}"

    search_mode = os.getenv("SEARCH_MODE", "vector").strip().lower()

    if search_mode not in ("vector", "hybrid"):
        raise SystemExit(
            f"SEARCH_MODE='{search_mode}' invalide dans .env "
            "(valeurs attendues : 'vector' ou 'hybrid')."
        )

    if search_mode == "hybrid" and vector_store_name != "azure_search":
        raise SystemExit(
            "SEARCH_MODE=hybrid n'est disponible qu'avec VECTOR_STORE=azure_search "
            "(seul backend a implementer la recherche hybride)."
        )

    # -----------------------------
    # Base vectorielle
    # -----------------------------

    if vector_store_name == "chromadb":

        vector_store = VectorStore(persist_directory=chroma_dir)

    elif vector_store_name == "pgvector":

        vector_store = VectorStorePgvector(
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

    elif vector_store_name == "qdrant":

        vector_store = VectorStoreQdrant(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", "6333")),
            embedding_dimension=384,
            collection_name=storage_name,
        )

    elif vector_store_name == "azure_search":

        vector_store = VectorStoreAzureSearch(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            api_key=os.getenv("AZURE_SEARCH_API_KEY"),
            embedding_dimension=384,
            index_name=storage_name.replace("_", "-"),
        )

    else:

        raise SystemExit(
            f"VECTOR_STORE='{vector_store_name}' invalide dans .env "
            "(valeurs attendues : 'chromadb', 'pgvector', 'qdrant' ou 'azure_search')."
        )

    embedding_service = EmbeddingService()

    def _get_confluence_space_keys():

        space_keys = [
            key.strip()
            for key in os.getenv("CONFLUENCE_SPACE_KEYS", "").split(",")
            if key.strip()
        ]

        if not space_keys:
            raise SystemExit(
                "DATA_SOURCE=confluence mais CONFLUENCE_SPACE_KEYS "
                "n'est pas defini dans .env (ex: CONFLUENCE_SPACE_KEYS=Infra,DevOps)."
            )

        return space_keys

    def _embed_and_store(documents, chunker):

        chunks = chunker.chunk_documents(documents)

        embedded_chunks = [
            embedding_service.embed_chunk(chunk)
            for chunk in chunks
        ]

        vector_store.add_chunks(embedded_chunks)

        if vector_store_name == "azure_search":
            print("Attente de la fin de l'indexation Azure AI Search...")
            time.sleep(5)

    # -----------------------------
    # Ingestion / synchronisation
    # -----------------------------

    if data_source == "confluence":

        space_keys = _get_confluence_space_keys()

        loader = ConfluenceLoader(
            site_url=os.getenv("CONFLUENCE_SITE_URL"),
            email=os.getenv("CONFLUENCE_EMAIL"),
            api_token=os.getenv("CONFLUENCE_API_TOKEN"),
            space_keys=space_keys,
        )

        sync_state_path = base_dir / f"sync_state_{data_source}.json"
        sync_state = SyncStateStore(sync_state_path)

        print("Vérification des pages Confluence nouvelles ou modifiées...")
        changed_documents = loader.load_changed_documents(sync_state)

        if changed_documents:

            print(f"{len(changed_documents)} page(s) nouvelle(s) ou modifiée(s) : ingestion en cours...")

            chunker = Chunker()
            _embed_and_store(changed_documents, chunker)

            sync_state.save()

            print("Synchronisation terminée.")

        else:

            print("Aucune page modifiée depuis la dernière synchronisation.")

    elif data_source == "local":

        if vector_store.is_empty():

            print(f"Base vectorielle vide (source : {data_source}, moteur : {vector_store_name}) : ingestion du corpus...")

            loader = DocumentLoader(docs_dir)
            documents = loader.load_documents()

            chunker = Chunker()
            _embed_and_store(documents, chunker)

        else:

            print(
                f"Base vectorielle déjà peuplée (source : {data_source}, moteur : {vector_store_name}) : "
                "ingestion sautée."
            )

    else:

        raise SystemExit(
            f"DATA_SOURCE='{data_source}' invalide dans .env "
            "(valeurs attendues : 'local' ou 'confluence')."
        )

    # -----------------------------
    # Services IA
    # -----------------------------

    llm_service_name = os.getenv("LLM_SERVICE", "ollama").strip().lower()

    prompt_builder = PromptBuilder()

    if llm_service_name == "ollama":

        llm_service = LLMService()

    elif llm_service_name == "azure_openai":

        llm_service = LLMServiceAzureOpenAI(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"),
        )

    else:

        raise SystemExit(
            f"LLM_SERVICE='{llm_service_name}' invalide dans .env "
            "(valeurs attendues : 'ollama' ou 'azure_openai')."
        )

    return RAGService(
        embedding_service=embedding_service,
        vector_store=vector_store,
        prompt_builder=prompt_builder,
        llm_service=llm_service,
        use_hybrid=(search_mode == "hybrid"),
    )