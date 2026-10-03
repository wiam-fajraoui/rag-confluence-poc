"""
Client HTTP vers l'ingestion-service -- meme principe que le front
qui appelle le rag-service : on ne connait l'autre service que par
son URL.
"""

import os

import requests


def get_ingestion_status(timeout: float = 3.0) -> dict:

    base_url = os.getenv("INGESTION_SERVICE_URL", "http://localhost:8001").rstrip("/")

    try:
        response = requests.get(f"{base_url}/status", timeout=timeout)
        response.raise_for_status()
        return {"reachable": True, **response.json()}

    except requests.RequestException as error:
        # Le rag-service reste utilisable meme si l'ingestion est
        # arretee : l'index existant reste interrogeable.
        return {"reachable": False, "error": str(error)}
