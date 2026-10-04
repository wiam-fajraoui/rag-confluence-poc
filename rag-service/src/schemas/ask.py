"""
Formats d'entree/sortie de l'API (contrat HTTP), distincts des
modeles internes de models/ (dataclasses du pipeline).
"""

from pydantic import BaseModel, Field


class AskRequest(BaseModel):

    question: str = Field(..., min_length=1, examples=["Comment fonctionne un Deployment Kubernetes ?"])


class CitationOut(BaseModel):

    number: int
    source: str
    excerpt: str


class AskResponse(BaseModel):

    answer: str
    citations: list[CitationOut]
