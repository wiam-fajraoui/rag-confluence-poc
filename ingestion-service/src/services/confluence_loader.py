from connectors.confluence_client import ConfluenceClient
from connectors.storage_format_converter import StorageFormatConverter
from models.document import Document

# Titres de pages générées automatiquement par Confluence à la
# création d'un espace, sans contenu documentaire réel -> à exclure
# systématiquement de l'ingestion.
_DEFAULT_EXCLUDED_TITLES = {
    "Template - How-to guide",
    "Template - Troubleshooting article",
}


class ConfluenceLoader:
    """
    Charge les documents depuis Confluence, en remplacement de
    DocumentLoader (qui lit des fichiers docs/*.md en local).

    Fournit deux méthodes :
    - load_documents() : charge tout le corpus (comportement
      d'origine, toujours disponible si besoin d'un rechargement
      complet).
    - load_changed_documents(sync_state) : ne charge que les pages
      nouvelles ou dont le numéro de version a changé depuis la
      dernière synchronisation. Fonctionne aussi bien pour un
      premier chargement (sync_state vide -> tout est "nouveau")
      que pour les suivants (sync_state déjà rempli -> seules les
      vraies modifications sont retournées), ce qui évite d'avoir
      deux chemins de code séparés pour ces deux cas.
    """

    def __init__(
        self,
        site_url: str,
        email: str,
        api_token: str,
        space_keys: list,
        excluded_titles: set = None,
    ):

        self.client = ConfluenceClient(site_url, email, api_token)
        self.converter = StorageFormatConverter()
        self.space_keys = space_keys
        self.excluded_titles = (
            excluded_titles
            if excluded_titles is not None
            else set(_DEFAULT_EXCLUDED_TITLES)
        )

    def load_documents(self) -> list:

        documents = []

        for space_key in self.space_keys:

            pages = self.client.get_pages_in_space(space_key)

            for page in pages:

                if self._should_skip(page, space_key):
                    continue

                document = self._to_document(page, space_key)
                documents.append(document)

        return documents

    def load_changed_documents(self, sync_state) -> list:
        """
        Ne retourne que les pages nouvelles ou modifiees depuis la
        derniere synchronisation. Met a jour sync_state en place
        (set_version) pour chaque page conservee -- l'appelant est
        responsable d'appeler sync_state.save() une fois
        l'ingestion de ces documents terminee avec succes (pas
        avant, pour ne pas marquer une page comme synchronisee si
        l'embedding/l'indexation echoue en cours de route).
        """

        changed_documents = []

        for space_key in self.space_keys:

            pages = self.client.get_pages_in_space(space_key)

            for page in pages:

                if self._should_skip(page, space_key):
                    continue

                page_id = page.get("id", "")
                current_version = page.get("version", {}).get("number")

                known_version = sync_state.get_version(page_id)

                if known_version is not None and known_version == current_version:
                    continue  # pas de changement depuis la derniere fois

                document = self._to_document(page, space_key)
                changed_documents.append(document)

                sync_state.set_version(page_id, current_version)

        return changed_documents

    def _should_skip(self, page: dict, space_key: str) -> bool:

        title = page.get("title", "")

        if title in self.excluded_titles:
            return True

        # Heuristique : la page d'accueil auto-générée d'un espace
        # porte généralement le même titre que l'espace lui-même
        # (sauf renommage manuel).
        if title == space_key:
            return True

        return False

    def _to_document(self, page: dict, space_key: str) -> Document:

        title = page.get("title", "")
        page_id = page.get("id", "")

        storage_value = (
            page.get("body", {})
            .get("storage", {})
            .get("value", "")
        )

        body_markdown = self.converter.convert(storage_value)

        content = f"# {title}\n\n{body_markdown}"

        ancestors = page.get("ancestors", [])
        parent_title = ancestors[-1]["title"] if ancestors else None

        return Document(
            id=page_id,
            title=title,
            filename=f"{title}.md",
            content=content,
            metadata={
                "source": f"{title}.md",
                "space": space_key,
                "confluence_id": page_id,
                "parent_title": parent_title,
            },
        )