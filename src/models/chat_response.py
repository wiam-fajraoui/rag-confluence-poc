from dataclasses import dataclass


@dataclass
class ChatResponse:

    answer: str

    sources: list[str]