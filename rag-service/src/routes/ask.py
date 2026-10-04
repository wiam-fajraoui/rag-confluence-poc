"""Endpoint de question-réponse."""

from fastapi import APIRouter, HTTPException, Request

from schemas.ask import AskRequest, AskResponse, CitationOut

router = APIRouter(tags=["Assistant"])


@router.post("/ask", response_model=AskResponse, summary="Pose une question à l'assistant")
def ask(payload: AskRequest, request: Request):

    rag_pipeline = getattr(request.app.state, "rag_pipeline", None)

    if rag_pipeline is None:
        raise HTTPException(status_code=503, detail="Service en cours d'initialisation.")

    question = payload.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="La question ne peut pas être vide.")

    response = rag_pipeline.ask(question)

    return AskResponse(
        answer=response.answer,
        citations=[
            CitationOut(number=c.number, source=c.source, excerpt=c.excerpt)
            for c in response.citations
        ],
    )
