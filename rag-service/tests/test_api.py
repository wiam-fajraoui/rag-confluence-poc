import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from fastapi.testclient import TestClient

import main


class FakeCitation:
    def __init__(self, number, source, excerpt):
        self.number, self.source, self.excerpt = number, source, excerpt


class FakeChatResponse:
    def __init__(self, answer, citations):
        self.answer, self.citations = answer, citations


class FakePipeline:
    def ask(self, question):
        if question == "question hors corpus":
            return FakeChatResponse("Je ne trouve pas cette information dans la documentation.", [])
        return FakeChatResponse(f"Réponse [1]", [FakeCitation(1, "exemple.md", "Extrait.")])


FAKE_STATUS = {"reachable": True, "ready": True, "vector_store": "chromadb", "storage_name": "chunks_local"}


@pytest.fixture
def client():
    with patch("main._build_pipeline", return_value=FakePipeline()), \
         patch("main.get_ingestion_status", return_value=FAKE_STATUS):
        with TestClient(main.app) as test_client:
            yield test_client


def test_health_reports_ingestion_status(client):
    body = client.get("/health").json()
    assert body["rag_pipeline_ready"] is True
    assert body["ingestion_service"]["reachable"] is True


def test_ask_returns_citations(client):
    body = client.post("/ask", json={"question": "Qu'est-ce qu'un Pod ?"}).json()
    assert body["citations"][0]["source"] == "exemple.md"


def test_ask_empty_question_400(client):
    assert client.post("/ask", json={"question": "   "}).status_code == 400


def test_ask_missing_field_422(client):
    assert client.post("/ask", json={}).status_code == 422


def test_ask_hors_corpus_no_citations(client):
    body = client.post("/ask", json={"question": "question hors corpus"}).json()
    assert body["citations"] == []
