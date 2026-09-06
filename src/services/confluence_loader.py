from services.confluence_client import ConfluenceClient
from services.storage_format_converter import StorageFormatConverter
from models.document import Document


# Titres de pages generées automatiquement par Confluence à la
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

    Fournit la même interface (load_documents() -> list[Document])
    afin que le reste du pipeline (chunker.py, embedding_service.py,
    vector_store.py, rag_service.py) fonctionne sans modification.
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

    def _should_skip(self, page: dict, space_key: str) -> bool:

        title = page.get("title", "")

        if title in self.excluded_titles:
            return True

        # Heuristique : la page d'accueil auto-générée d'un espace
        # porte généralement le même titre que l'espace lui-même
        # (sauf renommage manuel).
        # Limite connue : si une vraie page de contenu portait ce
        # même titre exact que l'espace, elle serait aussi exclue à
        # tort. À surveiller si ce cas se présente un jour.
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

        # Le titre H1 du document vient du titre de la page Confluence,
        # pas du corps -- cohérent avec le format des fichiers locaux
        # (document_title extrait de la ligne "# Titre" par chunker.py).
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