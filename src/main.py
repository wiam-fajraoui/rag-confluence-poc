import os
from pathlib import Path

from dotenv import load_dotenv

from services.document_loader import DocumentLoader
from services.confluence_loader import ConfluenceLoader
from services.chunker import Chunker
from services.embedding_service import EmbeddingService
from services.vector_store import VectorStore
from services.prompt_builder import PromptBuilder
from services.llm_service import LLMService
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


# -----------------------------
# Base vectorielle (persistante)
# -----------------------------

vector_store = VectorStore(persist_directory=CHROMA_DIR)

embedding_service = EmbeddingService()


# -----------------------------
# Ingestion (uniquement si la base est vide)
# -----------------------------

if vector_store.is_empty():

    print(f"Base vectorielle vide (source : {DATA_SOURCE}) : ingestion du corpus...")

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

else:

    print(
        f"Base vectorielle déjà peuplée ({CHROMA_DIR.name}/) : "
        "ingestion sautée.\n"
        "Pour forcer une réingestion complète (ex. après "
        "modification du corpus), supprimer ce dossier puis relancer."
    )


# -----------------------------
# Services IA
# -----------------------------

prompt_builder = PromptBuilder()
llm_service = LLMService()


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