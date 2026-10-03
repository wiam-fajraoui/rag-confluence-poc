from dataclasses import dataclass

from models.citation import Citation


@dataclass
class ChatResponse:

    answer: str

    citations: list