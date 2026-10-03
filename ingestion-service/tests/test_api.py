import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from fastapi.testclient import TestClient

import main


class FakePipeline:

    data_source = "confluence"
    vector_store_name = "azure_search"
    storage_name = "chunks_confluence"

    def run_sync(self):
        return {"status": "up_to_date", "pages_processed": 0, "chunks_ingested": 0, "finished_at": "2026-01-01T00:00:00"}


@pytest.fixture
def client():
    with patch("main.IngestionPipeline", return_value=FakePipeline()):
        with TestClient(main.app) as test_client:
            yield test_client


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_status_ready_after_startup(client):
    body = client.get("/status").json()
    assert body["ready"] is True
    assert body["data_source"] == "confluence"
    assert body["storage_name"] == "chunks_confluence"


def test_sync_returns_summary(client):
    body = client.post("/sync").json()
    assert body["status"] == "up_to_date"
