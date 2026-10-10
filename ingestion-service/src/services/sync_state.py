import json
from pathlib import Path


class SyncStateStore:
    """
    Memoire des pages deja indexees : {page_id: derniere_version_indexee}.

    Doit toujours refleter le contenu reel de l'index : une page n'y
    est notee qu'apres une indexation reussie, et en est retiree des
    que ses fiches sont supprimees de l'index.
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

    def remove(self, page_id: str):

        self._state.pop(page_id, None)

    def known_page_ids(self) -> set:

        return set(self._state.keys())
