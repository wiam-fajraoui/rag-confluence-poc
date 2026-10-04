"""
Microservice d'ingestion -- point d'entree.

Ce fichier ne fait qu'assembler l'application : chargement de la
configuration, demarrage (synchronisation initiale) et inclusion des
routes. Les endpoints eux-memes sont declares dans routes/.

Lancement local (depuis ingestion-service/src/) :
    uvicorn main:app --port 8001 --reload
"""

from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv

# .env propre a ce service : ingestion-service/.env
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from fastapi import FastAPI

from routes import health, sync
from services.ingestion import IngestionPipeline
from services.sync_coordinator import SyncCoordinator


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Démarrage du service d'ingestion...")

    # Rangé dans app.state : les routes y accedent via request.app.state,
    # sans importer main.py (ce qui creerait un import circulaire).
    coordinator = SyncCoordinator(IngestionPipeline())
    app.state.sync_coordinator = coordinator

    # Synchronisation initiale AVANT d'accepter des requetes : tant
    # qu'elle n'est pas terminee, /health ne repond pas -- c'est ce
    # que docker-compose utilise pour ne demarrer le rag-service
    # qu'une fois l'index pret.
    coordinator.run()

    print("Service d'ingestion prêt.")

    yield


app = FastAPI(
    title="Ingestion Service — RAG Confluence",
    description="Charge, découpe, vectorise et indexe le corpus documentaire.",
    version="1.1.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(sync.router)
