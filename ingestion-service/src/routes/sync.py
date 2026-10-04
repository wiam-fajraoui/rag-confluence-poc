"""Endpoints liés à la synchronisation du corpus et à l'état de l'index."""

from fastapi import APIRouter, HTTPException, Request

from services.sync_coordinator import SyncAlreadyRunning

router = APIRouter(tags=["Synchronisation"])


@router.get("/status", summary="État de l'index (consulté par le rag-service)")
def status(request: Request):

    coordinator = request.app.state.sync_coordinator
    pipeline = coordinator.pipeline

    return {
        "ready": coordinator.last_sync is not None,
        "data_source": pipeline.data_source,
        "vector_store": pipeline.vector_store_name,
        "storage_name": pipeline.storage_name,
        "last_sync": coordinator.last_sync,
    }


@router.post("/sync", summary="Déclenche une synchronisation incrémentale")
def sync(request: Request):

    try:
        return request.app.state.sync_coordinator.run()

    except SyncAlreadyRunning:
        raise HTTPException(status_code=409, detail="Une synchronisation est déjà en cours.")
