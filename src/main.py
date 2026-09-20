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


# -----------------------------
# Configuration
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"

load_dotenv(BASE_DIR / ".env")

DATA_SOURCE = os.getenv("DATA_SOURCE", "local").strip().lower()

CHROMA_DIR = BASE_DIR / f"chroma_data_{DATA_SOURCE}"

VECTOR_STORE = os.getenv("VECTOR_STORE", "chromadb").strip().lower()
STORAGE_NAME = f"chunks_{DATA_SOURCE}"

# SEARCH_MODE choisit le mode de recherche : "vector" (par defaut,
# recherche vectorielle pure, comportement historique) ou "hybrid"
# (mots-cles + vecteur + classement semantique -- disponible
# uniquement avec VECTOR_STORE=azure_search). Voir rag_service.py
# pour le detail des deux seuils de distance associes, et la mise en
# garde sur DISTANCE_THRESHOLD_HYBRID, pas encore calibre.
SEARCH_MODE = os.getenv("SEARCH_MODE", "vector").strip().lower()

if SEARCH_MODE not in ("vector", "hybrid"):
    raise SystemExit(
        f"SEARCH_MODE='{SEARCH_MODE}' invalide dans .env "
        "(valeurs attendues : 'vector' ou 'hybrid')."
    )

if SEARCH_MODE == "hybrid" and VECTOR_STORE != "azure_search":
    raise SystemExit(
        "SEARCH_MODE=hybrid n'est disponible qu'avec VECTOR_STORE=azure_search "
        "(seul backend a implementer la recherche hybride)."
    )


# -----------------------------
# Base vectorielle (persistante)
# -----------------------------

if VECTOR_STORE == "chromadb":

    vector_store = VectorStore(persist_directory=CHROMA_DIR)

elif VECTOR_STORE == "pgvector":

    vector_store = VectorStorePgvector(
        connection_params={
            "host": os.getenv("PGVECTOR_HOST", "localhost"),
            "port": int(os.getenv("PGVECTOR_PORT", "5432")),
            "dbname": os.getenv("PGVECTOR_DB", "rag_pgvector"),
            "user": os.getenv("PGVECTOR_USER", "postgres"),
            "password": os.getenv("PGVECTOR_PASSWORD"),
        },
        embedding_dimension=384,
        table_name=STORAGE_NAME,
    )

elif VECTOR_STORE == "qdrant":

    vector_store = VectorStoreQdrant(
        host=os.getenv("QDRANT_HOST", "localhost"),
        port=int(os.getenv("QDRANT_PORT", "6333")),
        embedding_dimension=384,
        collection_name=STORAGE_NAME,
    )

elif VECTOR_STORE == "azure_search":

    vector_store = VectorStoreAzureSearch(
        endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
        api_key=os.getenv("AZURE_SEARCH_API_KEY"),
        embedding_dimension=384,
        index_name=STORAGE_NAME.replace("_", "-"),  # Azure n'autorise pas "_" dans les noms d'index
    )

else:

    raise SystemExit(
        f"VECTOR_STORE='{VECTOR_STORE}' invalide dans .env "
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


def _embed_and_store(documents, chunker, embedding_service, vector_store):

    chunks = chunker.chunk_documents(documents)

    embedded_chunks = [
        embedding_service.embed_chunk(chunk)
        for chunk in chunks
    ]

    vector_store.add_chunks(embedded_chunks)

    if VECTOR_STORE == "azure_search":
        print("Attente de la fin de l'indexation Azure AI Search...")
        time.sleep(5)


# -----------------------------
# Ingestion / synchronisation
# -----------------------------

if DATA_SOURCE == "confluence":

    # Pour Confluence, on ne se contente plus de verifier si la base
    # est vide : on interroge systematiquement l'API pour detecter
    # les pages nouvelles ou modifiees depuis la derniere execution
    # (synchronisation incrementale). Le premier lancement (fichier
    # de suivi absent) traite naturellement toutes les pages comme
    # "nouvelles", sans logique separee a maintenir.

    space_keys = _get_confluence_space_keys()

    loader = ConfluenceLoader(
        site_url=os.getenv("CONFLUENCE_SITE_URL"),
        email=os.getenv("CONFLUENCE_EMAIL"),
        api_token=os.getenv("CONFLUENCE_API_TOKEN"),
        space_keys=space_keys,
    )

    sync_state_path = BASE_DIR / f"sync_state_{DATA_SOURCE}.json"
    sync_state = SyncStateStore(sync_state_path)

    print("Vérification des pages Confluence nouvelles ou modifiées...")
    changed_documents = loader.load_changed_documents(sync_state)

    if changed_documents:

        print(f"{len(changed_documents)} page(s) nouvelle(s) ou modifiée(s) : ingestion en cours...")

        chunker = Chunker()
        _embed_and_store(changed_documents, chunker, embedding_service, vector_store)

        # Sauvegarde de l'etat seulement apres succes de l'ingestion,
        # pour ne pas marquer une page comme synchronisee si
        # l'embedding ou l'indexation a echoue en cours de route.
        sync_state.save()

        print("Synchronisation terminée.")

    else:

        print("Aucune page modifiée depuis la dernière synchronisation.")

elif DATA_SOURCE == "local":

    # Pas de synchronisation incrementale pour les fichiers locaux
    # (non demande par la roadmap, qui ne le prevoit que pour
    # Confluence) -- comportement inchange : ingestion complete
    # uniquement si la base est vide.

    if vector_store.is_empty():

        print(f"Base vectorielle vide (source : {DATA_SOURCE}, moteur : {VECTOR_STORE}) : ingestion du corpus...")

        loader = DocumentLoader(DOCS_DIR)
        documents = loader.load_documents()

        chunker = Chunker()
        _embed_and_store(documents, chunker, embedding_service, vector_store)

    else:

        print(
            f"Base vectorielle déjà peuplée (source : {DATA_SOURCE}, moteur : {VECTOR_STORE}) : "
            "ingestion sautée.\n"
            "Pour forcer une réingestion complète, supprimer le dossier "
            f"{CHROMA_DIR.name}/ (ChromaDB) ou vider la table/collection/index "
            f"'{STORAGE_NAME}' correspondante, puis relancer."
        )

else:

    raise SystemExit(
        f"DATA_SOURCE='{DATA_SOURCE}' invalide dans .env "
        "(valeurs attendues : 'local' ou 'confluence')."
    )


# -----------------------------
# Services IA
# -----------------------------

LLM_SERVICE = os.getenv("LLM_SERVICE", "ollama").strip().lower()

prompt_builder = PromptBuilder()

if LLM_SERVICE == "ollama":

    llm_service = LLMService()

elif LLM_SERVICE == "azure_openai":

    llm_service = LLMServiceAzureOpenAI(
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"),
    )

else:

    raise SystemExit(
        f"LLM_SERVICE='{LLM_SERVICE}' invalide dans .env "
        "(valeurs attendues : 'ollama' ou 'azure_openai')."
    )


# -----------------------------
# Service RAG
# -----------------------------

rag_service = RAGService(
    embedding_service=embedding_service,
    vector_store=vector_store,
    prompt_builder=prompt_builder,
    llm_service=llm_service,
    use_hybrid=(SEARCH_MODE == "hybrid"),
)


# -----------------------------
# Chat
# -----------------------------

question = "Comment un pipeline CI/CD peut-il automatiser l'exécution de Terraform ?"

response = rag_service.ask(question)

print("\nRéponse\n")

print(response.answer)

print("\nSources\n")

for source in response.sources:
    print(f"- {source}")