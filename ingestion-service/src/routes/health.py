"""Endpoint de supervision du service."""

from fastapi import APIRouter

router = APIRouter(tags=["Supervision"])


@router.get("/health", summary="Le service répond-il ?")
def health():

    return {"status": "ok"}
