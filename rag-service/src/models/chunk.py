from dataclasses import dataclass, field


@dataclass
class Chunk:
    id: str
    content: str
    source: str
    embedding: list[float] | None = field(default=None)