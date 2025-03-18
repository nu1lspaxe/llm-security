from sentence_transformers import SentenceTransformer
from vector_database.vector_store import VectorStore
from config.logging import logger

class IndexBuilder:
    def __init__(self, model_name='all-MiniLM-L6-v2', vector_store=None):
        self.model = SentenceTransformer(model_name)
        self.vector_store = vector_store if vector_store else VectorStore()
        logger.info(f"Initialized IndexBuilder with model: {model_name}")
        
    def build_index(self, messages):
        """Generate embeddings and add them to the vector store."""
        try:
            embeddings = self.model.encode(messages, convert_to_numpy=True)
            metadata = [{"message": msg} for msg in messages] 
            self.vector_store.add_vectors(embeddings, metadata)
            self.vector_store.save()
            logger.debug(f"Built index for {len(messages)} messages")
            return embeddings
        except Exception as e:
            logger.error(f"Failed to build index: {str(e)}")
            raise
    
    def query_index(self, query_text, k=5):
        """Generate embedding for query and search the index."""
        try:
            query_embedding = self.model.encode([query_text], convert_to_numpy=True)[0]
            results = self.vector_store.search(query_embedding, k)
            logger.debug(f"Queried index with '{query_text}', found {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Query index failed: {str(e)}")
            raise