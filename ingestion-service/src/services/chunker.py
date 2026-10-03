from models.chunk import Chunk


class Chunker:

    # Un chunk composé essentiellement d'un bloc de code (ex. exemple
    # YAML) produit un embedding peu représentatif d'une requête en
    # langage naturel, et se retrouve rarement récupéré par le
    # retrieval même si l'information qu'il contient est pertinente.
    # On fusionne ce type de chunk avec le chunk précédent du même
    # document, qui contient généralement le texte explicatif associé.
    #
    # Remarque : une première version de cette correction utilisait un
    # seuil de taille (caractères), mais celui-ci s'est révélé bien
    # trop large sur ce corpus (il fusionnait plus de la moitié des
    # chunks du projet, la plupart des sections faisant naturellement
    # 200-400 caractères). La détection du bloc de code est un critère
    # beaucoup plus ciblé : un seul document du corpus est concerné.
    CODE_BLOCK_MARKER = "```"

    def chunk_documents(self, documents):

        chunks = []

        for document in documents:

            document_chunks = self._chunk_single_document(document)

            document_chunks = self._merge_small_chunks(document_chunks)

            chunks.extend(document_chunks)

        return chunks

    def _chunk_single_document(self, document):

        document_chunks = []

        lines = document.content.splitlines()

        document_title = ""
        current_chunk = []
        chunk_index = 1

        for line in lines:

            # Titre principal (# ...)
            if line.startswith("# "):
                document_title = line
                continue

            # Nouveau sous-titre (## ou ###)
            if line.startswith("##"):

                if current_chunk:

                    content = (
                        document_title
                        + "\n\n"
                        + "\n".join(current_chunk).strip()
                    )

                    document_chunks.append(
                        Chunk(
                            id=f"{document.id}_{chunk_index}",
                            source=document.filename,
                            content=content
                        )
                    )

                    chunk_index += 1

                current_chunk = [line]

            else:

                if current_chunk:
                    current_chunk.append(line)

        # Dernier chunk
        if current_chunk:

            content = (
                document_title
                + "\n\n"
                + "\n".join(current_chunk).strip()
            )

            document_chunks.append(
                Chunk(
                    id=f"{document.id}_{chunk_index}",
                    source=document.filename,
                    content=content
                )
            )

        return document_chunks

    def _merge_small_chunks(self, document_chunks):

        if not document_chunks:
            return document_chunks

        merged_chunks = [document_chunks[0]]

        for chunk in document_chunks[1:]:

            previous_chunk = merged_chunks[-1]

            if self.CODE_BLOCK_MARKER in chunk.content:

                # Chaque contenu de chunk est préfixé par le titre du
                # document ("# Titre\n\n..."). On retire ce préfixe du
                # chunk fusionné pour éviter de le dupliquer.
                _, _, section_content = chunk.content.partition("\n\n")

                previous_chunk.content = (
                    previous_chunk.content
                    + "\n\n"
                    + section_content
                )

            else:

                merged_chunks.append(chunk)

        return merged_chunks