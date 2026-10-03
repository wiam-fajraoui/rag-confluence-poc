"""
Microservice d'ingestion -- application autonome.

Responsabilite unique : lire le corpus (Confluence ou fichiers
locaux), le decouper, le vectoriser et l'indexer dans la base
vectorielle. Ne repond jamais a une question utilisateur (role du
rag-service).

Lancement local (depuis ingestion-service/src/) :
    uvicorn main:app --port 8001 --reload
"""

from contextlib import asynccontextmanager
from pathlib import Path
from threading import Lock

from dotenv import load_dotenv

# .env propre a ce service : ingestion-service/.env
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from fastapi import FastAPI, HTTPException

from services.ingestion import IngestionPipeline


pipeline = None
last_sync = None
_sync_lock = Lock()


def _do_sync() -> dict:

    global last_sync

    # Empeche deux synchronisations simultanees (ex. deux appels
    # POST /sync rapproches) d'ecrire en meme temps dans l'index.
    if not _sync_lock.acquire(blocking=False):
        raise HTTPException(status_code=409, detail="Une synchronisation est déjà en cours.")

    try:
        last_sync = pipeline.run_sync()
        return last_sync
    finally:
        _sync_lock.release()


@asynccontextmanager
async def lifespan(app: FastAPI):

    global pipeline

    print("Démarrage du service d'ingestion...")
    pipeline = IngestionPipeline()

    # Synchronisation initiale AVANT d'accepter des requetes : tant
    # qu'elle n'est pas terminee, /health ne repond pas -- c'est ce
    # que docker-compose utilise pour ne demarrer le rag-service
    # qu'une fois l'index pret.
    _do_sync()
    print("Service d'ingestion prêt.")

    yield


app = FastAPI(
    title="Ingestion Service — RAG Confluence",
    description="Charge, découpe, vectorise et indexe le corpus documentaire.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", summary="Le service répond-il ?")
def health():

    return {"status": "ok"}


@app.get("/status", summary="État de l'index (consulté par le rag-service)")
def status():

    return {
        "ready": last_sync is not None,
        "data_source": pipeline.data_source,
        "vector_store": pipeline.vector_store_name,
        "storage_name": pipeline.storage_name,
        "last_sync": last_sync,
    }


@app.post("/sync", summary="Déclenche une synchronisation incrémentale")
def sync():

    return _do_sync()
