from dataclasses import dataclass


@dataclass
class Document:
    id: str
    title: str
    filename: str
    content: str
    metadata: dict