"""
Pipeline d'ingestion : chargement -> decoupage -> embeddings ->
indexation. Les objets couteux (modele d'embedding, connexion a la
base vectorielle) sont crees une seule fois, puis reutilises a
chaque synchronisation.
"""

import os
import time
from datetime import datetime, timezone
from pathlib import Path

from connectors.embedding_service import EmbeddingService
from connectors.vector_store_factory import build_vector_store, get_vector_store_name
from services.chunker import Chunker
from services.confluence_loader import ConfluenceLoader
from services.document_loader import DocumentLoader
from services.sync_state import SyncStateStore


# ingestion-service/ (en local). Dans le conteneur, DATA_DIR et
# DOCS_DIR sont fournis par le Dockerfile.
SERVICE_ROOT = Path(__file__).resolve().parents[2]


class IngestionPipeline:

    def __init__(self):

        self.data_source = os.getenv("DATA_SOURCE", "local").strip().lower()

        if self.data_source not in ("local", "confluence"):
            raise SystemExit(
                f"DATA_SOURCE='{self.data_source}' invalide (attendu : 'local' ou 'confluence')."
            )

        self.vector_store_name = get_vector_store_name()

        # Nom de l'espace de stockage : CONTRAT partage avec le
        # rag-service, qui le recalcule de la meme facon a partir de
        # DATA_SOURCE pour lire le meme index.
        self.storage_name = f"chunks_{self.data_source}"

        self.data_dir = Path(os.getenv("DATA_DIR", SERVICE_ROOT / "data"))
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.docs_dir = Path(os.getenv("DOCS_DIR", SERVICE_ROOT / "docs"))

        chroma_base = Path(os.getenv("CHROMA_DIR", self.data_dir))

        self.vector_store = build_vector_store(
            self.storage_name,
            chroma_dir=chroma_base / f"chroma_data_{self.data_source}",
        )

        self.embedding_service = EmbeddingService()
        self.chunker = Chunker()

    def run_sync(self) -> dict:

        if self.data_source == "confluence":
            summary = self._sync_confluence()
        else:
            summary = self._sync_local()

        summary["finished_at"] = datetime.now(timezone.utc).isoformat()

        return summary

    def _sync_confluence(self) -> dict:

        space_keys = [
            key.strip()
            for key in os.getenv("CONFLUENCE_SPACE_KEYS", "").split(",")
            if key.strip()
        ]

        if not space_keys:
            raise SystemExit("CONFLUENCE_SPACE_KEYS doit être défini (ex: Infra,DevOps).")

        loader = ConfluenceLoader(
            site_url=os.getenv("CONFLUENCE_SITE_URL"),
            email=os.getenv("CONFLUENCE_EMAIL"),
            api_token=os.getenv("CONFLUENCE_API_TOKEN"),
            space_keys=space_keys,
        )

        sync_state = SyncStateStore(self.data_dir / f"sync_state_{self.data_source}.json")

        print("Vérification des pages Confluence nouvelles ou modifiées...")
        documents = loader.load_changed_documents(sync_state)

        if not documents:
            print("Aucune page modifiée depuis la dernière synchronisation.")
            return {"status": "up_to_date", "pages_processed": 0, "chunks_ingested": 0}

        print(f"{len(documents)} page(s) nouvelle(s) ou modifiée(s) : ingestion en cours...")
        n_chunks = self._index(documents)

        # Sauvegarde APRES l'indexation reussie : une page n'est
        # jamais marquee synchronisee si l'indexation a echoue.
        sync_state.save()

        return {"status": "synced", "pages_processed": len(documents), "chunks_ingested": n_chunks}

    def _sync_local(self) -> dict:

        if not self.vector_store.is_empty():
            print("Base vectorielle déjà peuplée : ingestion sautée.")
            return {"status": "already_populated", "pages_processed": 0, "chunks_ingested": 0}

        documents = DocumentLoader(self.docs_dir).load_documents()
        n_chunks = self._index(documents)

        return {"status": "ingested", "pages_processed": len(documents), "chunks_ingested": n_chunks}

    def _index(self, documents) -> int:

        chunks = self.chunker.chunk_documents(documents)

        embedded_chunks = [self.embedding_service.embed_chunk(chunk) for chunk in chunks]

        self.vector_store.add_chunks(embedded_chunks)

        if self.vector_store_name == "azure_search":
            # Indexation asynchrone cote Azure (constat fait lors du benchmark).
            time.sleep(5)

        print(f"{len(chunks)} chunks indexés.")

        return len(chunks)
