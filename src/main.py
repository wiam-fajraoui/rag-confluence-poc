import os
import time
from pathlib import Path

from dotenv import load_dotenv

from services.document_loader import DocumentLoader
from services.confluence_loader import ConfluenceLoader
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

# DATA_SOURCE choisit la source des documents : "local" (fichiers
# docs/*.md) ou "confluence" (API REST Confluence). Definie dans le
# fichier .env, avec "local" comme valeur par defaut pour ne rien
# casser si la variable n'est pas encore configuree.
DATA_SOURCE = os.getenv("DATA_SOURCE", "local").strip().lower()

# Une base vectorielle persistante distincte par source : basculer
# de DATA_SOURCE ne declenche pas de reingestion (voir la correction
# "ingestion uniquement si la base est vide" plus bas) si les deux
# sources partageaient le meme dossier -- ce qui empecherait de les
# comparer proprement. Chaque source a donc son propre dossier.
CHROMA_DIR = BASE_DIR / f"chroma_data_{DATA_SOURCE}"

# VECTOR_STORE choisit le moteur de recherche vectorielle : "chromadb"
# (par defaut, comportement inchange), "pgvector", "qdrant" ou
# "azure_search". Comme pour DATA_SOURCE, un identifiant de stockage
# (table/collection/index) distinct par DATA_SOURCE evite de melanger
# des donnees issues de sources differentes dans un meme espace de
# stockage.
VECTOR_STORE = os.getenv("VECTOR_STORE", "chromadb").strip().lower()
STORAGE_NAME = f"chunks_{DATA_SOURCE}"


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


# -----------------------------
# Ingestion (uniquement si la base est vide)
# -----------------------------

if vector_store.is_empty():

    print(f"Base vectorielle vide (source : {DATA_SOURCE}, moteur : {VECTOR_STORE}) : ingestion du corpus...")

    if DATA_SOURCE == "confluence":

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

        loader = ConfluenceLoader(
            site_url=os.getenv("CONFLUENCE_SITE_URL"),
            email=os.getenv("CONFLUENCE_EMAIL"),
            api_token=os.getenv("CONFLUENCE_API_TOKEN"),
            space_keys=space_keys,
        )

    elif DATA_SOURCE == "local":

        loader = DocumentLoader(DOCS_DIR)

    else:

        raise SystemExit(
            f"DATA_SOURCE='{DATA_SOURCE}' invalide dans .env "
            "(valeurs attendues : 'local' ou 'confluence')."
        )

    documents = loader.load_documents()

    chunker = Chunker()
    chunks = chunker.chunk_documents(documents)

    embedded_chunks = [
        embedding_service.embed_chunk(chunk)
        for chunk in chunks
    ]

    vector_store.add_chunks(embedded_chunks)

    if VECTOR_STORE == "azure_search":
        # Azure AI Search indexe de facon asynchrone : sans cette
        # pause, une recherche lancee juste apres l'ingestion peut
        # ne retourner aucun resultat, l'indexation n'etant pas
        # encore terminee (meme constat fait dans
        # benchmark_vector_stores.py).
        print("Attente de la fin de l'indexation Azure AI Search...")
        time.sleep(5)

else:

    print(
        f"Base vectorielle déjà peuplée (source : {DATA_SOURCE}, moteur : {VECTOR_STORE}) : "
        "ingestion sautée.\n"
        "Pour forcer une réingestion complète (ex. après "
        "modification du corpus) : supprimer le dossier "
        f"{CHROMA_DIR.name}/ (ChromaDB), ou vider/supprimer la "
        f"table/collection/index '{STORAGE_NAME}' correspondante "
        "(pgvector/Qdrant/Azure AI Search), puis relancer."
    )


# -----------------------------
# Services IA
# -----------------------------

# LLM_SERVICE choisit le moteur de generation : "ollama" (par
# defaut, comportement inchange) ou "azure_openai".
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
    llm_service=llm_service
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