from connectors.confluence_client import ConfluenceClient
from connectors.storage_format_converter import StorageFormatConverter
from models.document import Document


_DEFAULT_EXCLUDED_TITLES = {
    "Template - How-to guide",
    "Template - Troubleshooting article",
}


class ConfluenceLoader:
    """
    Charge les pages Confluence et les convertit en objets Document.

    load_changed_documents(sync_state) retourne :
    - les pages nouvelles ou modifiees depuis la derniere
      synchronisation ;
    - l'ensemble des identifiants de pages qui existent ACTUELLEMENT
      dans Confluence (hors pages parasites). En le comparant a
      sync_state, l'appelant detecte les pages supprimees.
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

            for page in self.client.get_pages_in_space(space_key):

                if self._should_skip(page, space_key):
                    continue

                documents.append(self._to_document(page, space_key))

        return documents

    def load_changed_documents(self, sync_state):
        """
        Met a jour sync_state en place (set_version) pour chaque page
        retenue ; l'appelant appelle sync_state.save() seulement apres
        une indexation reussie.
        """

        changed_documents = []
        current_page_ids = set()

        for space_key in self.space_keys:

            for page in self.client.get_pages_in_space(space_key):

                if self._should_skip(page, space_key):
                    continue

                page_id = page.get("id", "")
                current_page_ids.add(page_id)

                current_version = page.get("version", {}).get("number")
                known_version = sync_state.get_version(page_id)

                if known_version is not None and known_version == current_version:
                    continue

                changed_documents.append(self._to_document(page, space_key))
                sync_state.set_version(page_id, current_version)

        return changed_documents, current_page_ids

    def _should_skip(self, page: dict, space_key: str) -> bool:

        title = page.get("title", "")

        if title in self.excluded_titles:
            return True

        # La page d'accueil d'un espace porte generalement son nom.
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

        ancestors = page.get("ancestors", [])
        parent_title = ancestors[-1]["title"] if ancestors else None

        return Document(
            id=page_id,
            title=title,
            filename=f"{title}.md",
            content=f"# {title}\n\n{body_markdown}",
            metadata={
                "source": f"{title}.md",
                "space": space_key,
                "confluence_id": page_id,
                "parent_title": parent_title,
            },
        )
