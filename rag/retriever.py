from vector_database.index_builder import IndexBuilder
from langchain.schema import Document

class Retriever:
    def __init__(self, index_builder=None):
        self.index_builder = index_builder if index_builder else IndexBuilder()

    def retrieve(self, query, k=5):
        """Retrieve top k relevant log messages from FAISS."""
        results = self.index_builder.query_index(query, k)
        return [Document(page_content=r["message"]) for r in results]