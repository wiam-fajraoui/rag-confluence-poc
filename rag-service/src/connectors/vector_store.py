import chromadb

from models.chunk import Chunk
from models.search_result import SearchResult


class VectorStore:

    def __init__(self, persist_directory):

        # PersistentClient écrit la collection sur disque, au lieu de la
        # recréer en mémoire à chaque exécution (comportement précédent
        # avec chromadb.Client()). Cela évite de refaire l'ingestion
        # complète (chargement + chunking + embeddings) à chaque run
        # quand le corpus n'a pas changé.
        self.client = chromadb.PersistentClient(
            path=str(persist_directory)
        )

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

    def is_empty(self) -> bool:

        return self.collection.count() == 0

    def add_chunks(self, chunks: list):

        # upsert() plutot que add() : necessaire pour la
        # synchronisation incrementale -- si une page Confluence est
        # modifiee, ses chunks reutilisent les memes ids, et add()
        # echouerait avec une erreur de doublon. upsert() met a jour
        # le chunk existant si l'id est deja present, l'ajoute sinon.
        self.collection.upsert(
            ids=[chunk.id for chunk in chunks],
            documents=[chunk.content for chunk in chunks],
            embeddings=[chunk.embedding for chunk in chunks],
            metadatas=[
                {
                    "source": chunk.source
                }
                for chunk in chunks
            ]
        )

    def search(self, query_embedding, n_results=3, query_text: str = None):

        # query_text n'est pas utilise par ChromaDB (pas de recherche
        # hybride ici) -- present uniquement pour garder la meme
        # signature que les 4 connecteurs (voir vector_store_azure_search.py
        # qui, lui, l'utilise reellement).

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        search_results = []

        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for id_, document, metadata, distance in zip(
            ids,
            documents,
            metadatas,
            distances
        ):

            search_result = SearchResult(
                id=id_,
                content=document,
                source=metadata["source"],
                distance=distance
            )

            search_results.append(search_result)

        return search_results