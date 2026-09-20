"""
API exposant l'assistant RAG Confluence.

Lancement :
    uvicorn api:app --reload

Documentation interactive generee automatiquement, une fois lancee :
    http://127.0.0.1:8000/docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from services.app_setup import build_rag_service


# Instance partagee, construite une seule fois au demarrage du
# serveur (pas a chaque question) -- l'ingestion/synchronisation et
# le chargement du modele d'embedding sont couteux, ils ne doivent
# pas se reproduire a chaque requete HTTP.
rag_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):

    global rag_service

    print("Démarrage de l'API : initialisation du pipeline RAG...")
    rag_service = build_rag_service()
    print("Pipeline RAG prêt.")

    yield

    # Rien a nettoyer explicitement au moment de l'arret pour
    # l'instant (pas de connexion persistante a fermer cote
    # ChromaDB/Azure) -- ce bloc existe pour respecter le protocole
    # lifespan, prevu pour accueillir un futur nettoyage si besoin.


app = FastAPI(
    title="API Assistant RAG Confluence",
    description=(
        "Recherche documentaire sur Confluence, combinant Azure AI "
        "Search (indexation hybride) et Azure OpenAI (génération de "
        "réponse avec citations des sources)."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


class AskRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        description="La question posée à l'assistant, en français.",
        examples=["Comment fonctionne un Deployment Kubernetes ?"],
    )


class AskResponse(BaseModel):

    answer: str = Field(description="La réponse générée par l'assistant.")
    sources: list = Field(description="Les documents Confluence utilisés pour répondre.")


@app.get("/health", summary="Vérifie que l'API et le pipeline RAG sont opérationnels")
def health():

    return {
        "status": "ok",
        "rag_service_ready": rag_service is not None,
    }


@app.post(
    "/ask",
    response_model=AskResponse,
    summary="Pose une question à l'assistant documentaire",
)
def ask(request: AskRequest):

    if rag_service is None:
        raise HTTPException(
            status_code=503,
            detail="Le service n'est pas encore initialisé, réessayez dans un instant.",
        )

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="La question ne peut pas être vide.",
        )

    response = rag_service.ask(question)

    return AskResponse(answer=response.answer, sources=response.sources)