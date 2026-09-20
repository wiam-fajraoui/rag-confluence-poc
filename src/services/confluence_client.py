import base64

import requests


class ConfluenceClient:
    """
    Client HTTP minimal pour l'API REST Confluence Cloud.

    Ne s'occupe que de l'authentification et de la pagination — la
    conversion du contenu (Storage Format -> Markdown) et le filtrage
    des pages sans intérêt documentaire sont délégués à d'autres
    composants (storage_format_converter.py, confluence_loader.py),
    pour respecter une responsabilité unique par fichier.
    """

    def __init__(self, site_url: str, email: str, api_token: str):

        self.wiki_base = site_url.rstrip("/") + "/wiki"
        api_base = self.wiki_base + "/rest/api"
        self.content_url = api_base + "/content"

        credentials = f"{email}:{api_token}"
        encoded = base64.b64encode(
            credentials.encode("utf-8")
        ).decode("utf-8")

        self.headers = {
            "Authorization": f"Basic {encoded}",
            "Accept": "application/json",
        }

    def get_pages_in_space(self, space_key: str, limit: int = 25) -> list:
        """
        Récupère toutes les pages d'un espace, avec pagination
        automatique, y compris leur contenu au format Storage
        (body.storage), leurs ancêtres (hiérarchie) et leur version
        (version.number -- nécessaire pour la synchronisation
        incrémentale : détecter qu'une page a changé depuis la
        dernière ingestion sans comparer tout le contenu).
        """

        pages = []

        url = self.content_url
        params = {
            "spaceKey": space_key,
            "expand": "body.storage,ancestors,version",
            "limit": limit,
        }

        while url:

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            data = response.json()
            pages.extend(data.get("results", []))

            next_link = data.get("_links", {}).get("next")

            if next_link:
                url = self.wiki_base + next_link
                params = None  # deja inclus dans next_link
            else:
                url = None

        return pages