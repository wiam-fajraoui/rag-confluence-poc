from pathlib import Path

from services.document_loader import DocumentLoader
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
CHROMA_DIR = BASE_DIR / "chroma_data"


# -----------------------------
# Base vectorielle (persistante)
# -----------------------------

vector_store = VectorStore(persist_directory=CHROMA_DIR)

embedding_service = EmbeddingService()


# -----------------------------
# Ingestion (uniquement si la base est vide)
# -----------------------------

if vector_store.is_empty():

    print("Base vectorielle vide : ingestion du corpus...")

    loader = DocumentLoader(DOCS_DIR)
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
        "Base vectorielle déjà peuplée (chroma_data/) : "
        "ingestion sautée.\n"
        "Pour forcer une réingestion complète (ex. après "
        "modification des fichiers docs/*.md), supprimer "
        "le dossier chroma_data/ puis relancer."
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

question = "Comment versionner et déployer une application avec Docker ?"

response = rag_service.ask(question)

print("\nRéponse\n")

print(response.answer)

print("\nSources\n")

for source in response.sources:
    print(f"- {source}")