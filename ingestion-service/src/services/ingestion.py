"""
Pipeline d'ingestion : chargement -> decoupage -> embeddings ->
indexation -> nettoyage des fiches obsoletes.

Les objets couteux (modele d'embedding, connexion a la base
vectorielle) sont crees une seule fois, puis reutilises a chaque
synchronisation.
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
        # rag-service, qui le recalcule a partir de DATA_SOURCE.
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

        # Seul le connecteur Azure AI Search sait supprimer les
        # fiches d'une page. Avec les autres backends, la suppression
        # est desactivee (avertissement au demarrage).
        self.can_delete = hasattr(self.vector_store, "delete_pages")

        if not self.can_delete:
            print(
                f"ATTENTION : le backend '{self.vector_store_name}' ne gère pas la suppression : "
                "les pages supprimées ou raccourcies laisseront des fiches obsolètes."
            )

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

        print("Vérification des pages Confluence nouvelles, modifiées ou supprimées...")
        documents, current_page_ids = loader.load_changed_documents(sync_state)

        # Pages connues de l'index mais absentes de Confluence = supprimees.
        deleted_page_ids = sync_state.known_page_ids() - current_page_ids

        # Garde-fou : si Confluence ne renvoie AUCUNE page (cle d'espace
        # erronee, droits retires...), on ne vide pas l'index entier.
        if not current_page_ids and deleted_page_ids:
            print(
                "ATTENTION : Confluence n'a renvoyé aucune page. Suppression annulée "
                "par sécurité -- vérifier CONFLUENCE_SPACE_KEYS et les identifiants."
            )
            deleted_page_ids = set()

        summary = {
            "pages_processed": len(documents),
            "chunks_ingested": 0,
            "stale_chunks_deleted": 0,
            "pages_deleted": 0,
            "chunks_deleted": 0,
        }

        if not documents and not deleted_page_ids:
            print("Aucun changement depuis la dernière synchronisation.")
            summary["status"] = "up_to_date"
            return summary

        if documents:

            print(f"{len(documents)} page(s) nouvelle(s) ou modifiée(s) : ingestion en cours...")
            new_chunk_ids = self._index(documents)
            summary["chunks_ingested"] = len(new_chunk_ids)

            if self.can_delete:
                # Pages raccourcies : retire les anciennes fiches de ces
                # pages qui ne correspondent a aucun fragment actuel.
                summary["stale_chunks_deleted"] = self.vector_store.delete_pages(
                    [document.id for document in documents],
                    keep_ids=new_chunk_ids,
                )

        if deleted_page_ids and self.can_delete:

            print(f"{len(deleted_page_ids)} page(s) supprimée(s) de Confluence : nettoyage de l'index...")
            summary["chunks_deleted"] = self.vector_store.delete_pages(deleted_page_ids)
            summary["pages_deleted"] = len(deleted_page_ids)

            for page_id in deleted_page_ids:
                sync_state.remove(page_id)

        self._wait_for_indexing()

        # Sauvegarde APRES toutes les ecritures reussies : sync_state
        # reste le reflet exact de l'index.
        sync_state.save()

        print(
            f"Synchronisation terminée : {summary['chunks_ingested']} fiche(s) indexée(s), "
            f"{summary['stale_chunks_deleted'] + summary['chunks_deleted']} fiche(s) obsolète(s) supprimée(s)."
        )

        summary["status"] = "synced"

        return summary

    def _sync_local(self) -> dict:

        if not self.vector_store.is_empty():
            print("Base vectorielle déjà peuplée : ingestion sautée.")
            return {"status": "already_populated", "pages_processed": 0, "chunks_ingested": 0}

        documents = DocumentLoader(self.docs_dir).load_documents()
        chunk_ids = self._index(documents)
        self._wait_for_indexing()

        return {"status": "ingested", "pages_processed": len(documents), "chunks_ingested": len(chunk_ids)}

    def _index(self, documents) -> list:
        """
        Decoupe, vectorise et envoie les documents. Chaque fragment
        recoit le page_id de sa page d'origine. Retourne la liste des
        identifiants des fragments envoyes.
        """

        chunks = []

        # Decoupage page par page, pour savoir a quelle page appartient
        # chaque fragment.
        for document in documents:
            for chunk in self.chunker.chunk_documents([document]):
                chunk.page_id = document.id
                chunks.append(chunk)

        embedded_chunks = [self.embedding_service.embed_chunk(chunk) for chunk in chunks]

        self.vector_store.add_chunks(embedded_chunks)

        return [chunk.id for chunk in chunks]

    def _wait_for_indexing(self):

        if self.vector_store_name == "azure_search":
            # Indexation quasi temps reel cote Azure (valeur empirique).
            time.sleep(5)
