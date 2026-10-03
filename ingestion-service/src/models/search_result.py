from dataclasses import dataclass


@dataclass
class SearchResult:

    id: str

    content: str

    source: str

    distance: float