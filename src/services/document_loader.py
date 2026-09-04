from pathlib import Path

from models.document import Document


class DocumentLoader:

    def __init__(self, docs_path):

        self.docs_path = Path(docs_path)

    def load_documents(self):

        documents = []

        for file in self.docs_path.glob("*.md"):

            content = file.read_text(encoding="utf-8")

            document = Document(
                id=file.stem,
                title=file.stem,
                filename=file.name,
                content=content,
                metadata={
                    "source": file.name
                }
            )

            documents.append(document)

        return documents