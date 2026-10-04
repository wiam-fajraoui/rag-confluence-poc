FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1
# PyTorch en version CPU uniquement (installe avant
# sentence-transformers) : evite d'embarquer les librairies CUDA,
# inutiles ici, qui alourdiraient l'image de plusieurs Go.
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
COPY docs/ ./docs/

ENV DATA_DIR=/data \
    DOCS_DIR=/app/docs

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
