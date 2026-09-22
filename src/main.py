"""
Script de demonstration en ligne de commande. Toute la logique de
configuration (choix des backends, ingestion/synchronisation) vit
desormais dans services/app_setup.py, partagee avec l'API (api.py).
"""

from services.app_setup import build_rag_service


rag_service = build_rag_service()


# -----------------------------
# Chat
# -----------------------------

question = "Comment fonctionne un Deployment Kubernetes ?"

response = rag_service.ask(question)

print("\nRéponse\n")

print(response.answer)

print("\nCitations\n")

for citation in response.citations:
    print(f"[{citation.number}] {citation.source} — {citation.excerpt}")