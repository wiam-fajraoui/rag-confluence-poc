import json
from pathlib import Path


class SyncStateStore:
    """
    Suivi local des versions de pages Confluence deja ingerees, pour
    permettre une synchronisation incrementale : ne retraiter que les
    pages nouvelles ou modifiees depuis la derniere execution,
    plutot que de tout recharger a chaque fois.

    Stocke un simple fichier JSON {page_id: numero_de_version}, a
    cote des autres donnees generees du projet (chroma_data_*/) --
    pas destine a etre committe dans Git (donnee locale, pas du
    code).
    """

    def __init__(self, path):

        self.path = Path(path)
        self._state = self._load()

    def _load(self) -> dict:

        if not self.path.exists():
            return {}

        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self):

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._state, f, indent=2)

    def get_version(self, page_id: str):

        return self._state.get(page_id)

    def set_version(self, page_id: str, version: int):

        self._state[page_id] = version

    def known_page_ids(self) -> set:

        return set(self._state.keys())