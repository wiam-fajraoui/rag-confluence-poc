"""Endpoint de supervision du service et de sa dépendance ingestion-service."""

from fastapi import APIRouter, Request

from services.ingestion_client import get_ingestion_status
from services.pipeline import is_same_index

router = APIRouter(tags=["Supervision"])


@router.get("/health", summary="État du rag-service et de sa dépendance ingestion-service")
def health(request: Request):

    ingestion_status = get_ingestion_status()

    return {
        "status": "ok",
        "rag_pipeline_ready": getattr(request.app.state, "rag_pipeline", None) is not None,
        "ingestion_service": ingestion_status,
        "same_index_as_ingestion": is_same_index(ingestion_status),
    }
