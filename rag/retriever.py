from vector_database.index_builder import IndexBuilder
from langchain.schema import Document
from config.logging import logger

class Retriever:
    def __init__(self, index_builder=None):
        self.index_builder = index_builder if index_builder else IndexBuilder()
        logger.info("Initialized Retriever")

    def retrieve(self, query, k=5):
        """Retrieve top k relevant log messages from FAISS."""
        try:
            results = self.index_builder.query_index(query, k)
            return [Document(page_content=r["message"]) for r in results]
        except Exception as e:
            logger.error(f"Retrieval failed for query '{query}': {str(e)}")
            raise