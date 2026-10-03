from dataclasses import dataclass


@dataclass
class Citation:
    number: int
    source: str
    excerpt: str