"""
Microservice RAG -- point d'entree.

Ce fichier ne fait qu'assembler l'application : chargement de la
configuration, demarrage (construction du pipeline, verification de
l'ingestion-service), CORS et inclusion des routes. Les endpoints
sont declares dans routes/, les formats de requete/reponse dans
schemas/.

Lancement local (depuis rag-service/src/) :
    uvicorn main:app --port 8000 --reload
"""

import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv

# .env propre a ce service : rag-service/.env
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import ask, health
from services.ingestion_client import get_ingestion_status
from services.pipeline import build_pipeline, is_same_index


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Démarrage du rag-service...")

    # Rangé dans app.state : les routes y accedent via request.app.state.
    app.state.rag_pipeline = build_pipeline()

    consistent = is_same_index(get_ingestion_status())

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
    version="2.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(ask.router)
