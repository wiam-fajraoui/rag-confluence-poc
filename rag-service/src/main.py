"""
Microservice RAG -- application autonome.

Responsabilite unique : repondre aux questions a partir de l'index
deja peuple par l'ingestion-service. N'ingere jamais rien.

Communication avec l'ingestion-service :
- Donnees : les deux lisent/ecrivent le MEME index (contrat :
  meme VECTOR_STORE, meme DATA_SOURCE -> meme nom d'index, meme
  modele d'embedding).
- Controle : appel HTTP GET {INGESTION_SERVICE_URL}/status, pour
  savoir si l'index est pret et verifier que les deux services
  pointent bien vers le meme index.

Lancement local (depuis rag-service/src/) :
    uvicorn main:app --port 8000 --reload
"""

import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv

# .env propre a ce service : rag-service/.env
SERVICE_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(SERVICE_ROOT / ".env")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from connectors.embedding_service import EmbeddingService
from connectors.llm_service_factory import build_llm_service
from connectors.vector_store_factory import build_vector_store, get_vector_store_name
from services.ingestion_client import get_ingestion_status
from services.prompt_builder import PromptBuilder
from services.rag_service import RAGService


DATA_SOURCE = os.getenv("DATA_SOURCE", "local").strip().lower()
STORAGE_NAME = f"chunks_{DATA_SOURCE}"

rag_pipeline = None


def _build_pipeline() -> RAGService:

    search_mode = os.getenv("SEARCH_MODE", "vector").strip().lower()

    if search_mode not in ("vector", "hybrid"):
        raise SystemExit(f"SEARCH_MODE='{search_mode}' invalide (attendu : 'vector' ou 'hybrid').")

    chroma_base = Path(os.getenv("CHROMA_DIR", SERVICE_ROOT / "data"))

    return RAGService(
        embedding_service=EmbeddingService(),
        vector_store=build_vector_store(
            STORAGE_NAME,
            chroma_dir=chroma_base / f"chroma_data_{DATA_SOURCE}",
        ),
        prompt_builder=PromptBuilder(),
        llm_service=build_llm_service(),
        use_hybrid=(search_mode == "hybrid"),
    )


def _is_consistent(ingestion_status: dict):
    """
    True/False si l'ingestion-service est joignable : les deux
    services ciblent-ils le meme backend et le meme index ?
    None s'il est injoignable (impossible de verifier).
    """

    if not ingestion_status.get("reachable"):
        return None

    return (
        ingestion_status.get("vector_store") == get_vector_store_name()
        and ingestion_status.get("storage_name") == STORAGE_NAME
    )


@asynccontextmanager
async def lifespan(app: FastAPI):

    global rag_pipeline

    print("Démarrage du rag-service...")
    rag_pipeline = _build_pipeline()

    status = get_ingestion_status()
    consistent = _is_consistent(status)

    if consistent is None:
        print("ATTENTION : ingestion-service injoignable -- l'index n'est peut-être pas prêt.")
    elif not consistent:
        print("ATTENTION : configuration différente de l'ingestion-service (backend ou index) !")
    else:
        print("ingestion-service joignable, même index : OK.")

    print("Rag-service prêt.")

    yield


app = FastAPI(
    title="RAG Service — Assistant documentaire Confluence",
    description="Répond aux questions avec citations, à partir de l'index alimenté par l'ingestion-service.",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):

    question: str = Field(..., min_length=1, examples=["Comment fonctionne un Deployment Kubernetes ?"])


class CitationOut(BaseModel):

    number: int
    source: str
    excerpt: str


class AskResponse(BaseModel):

    answer: str
    citations: list[CitationOut]


@app.get("/health", summary="État du rag-service et de sa dépendance ingestion-service")
def health():

    ingestion_status = get_ingestion_status()

    return {
        "status": "ok",
        "rag_pipeline_ready": rag_pipeline is not None,
        "ingestion_service": ingestion_status,
        "same_index_as_ingestion": _is_consistent(ingestion_status),
    }


@app.post("/ask", response_model=AskResponse, summary="Pose une question à l'assistant")
def ask(request: AskRequest):

    if rag_pipeline is None:
        raise HTTPException(status_code=503, detail="Service en cours d'initialisation.")

    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="La question ne peut pas être vide.")

    response = rag_pipeline.ask(question)

    return AskResponse(
        answer=response.answer,
        citations=[
            CitationOut(number=c.number, source=c.source, excerpt=c.excerpt)
            for c in response.citations
        ],
    )
