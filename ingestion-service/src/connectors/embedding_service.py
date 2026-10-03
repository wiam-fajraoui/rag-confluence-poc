from sentence_transformers import SentenceTransformer
from models.chunk import Chunk

class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def embed_chunk(self, chunk: Chunk):

        chunk.embedding = self.model.encode(
            chunk.content
        ).tolist()

        return chunk

    def generate_embedding(self, text: str):

        embedding = self.model.encode(text)

        return embedding.tolist()