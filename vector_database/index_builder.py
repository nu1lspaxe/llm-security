from sentence_transformers import SentenceTransformer
from vector_database.vector_store import VectorStore

class IndexBuilder:
    def __init__(self, model_name='all-MiniLM-L6-v2', vector_store=None):
        self.model = SentenceTransformer(model_name)
        self.vector_store = vector_store if vector_store else VectorStore()
        
    def build_index(self, messages):
        """Generate embeddings and add them to the vector store."""
        embeddings = self.model.encode(messages, convert_to_numpy=True)
        metadata = [{"message": msg} for msg in messages]  # Store original messages as metadata
        self.vector_store.add_vectors(embeddings, metadata)
        self.vector_store.save()
        return embeddings
    
    def query_index(self, query_text, k=5):
        """Generate embedding for query and search the index."""
        query_embedding = self.model.encode([query_text], convert_to_numpy=True)[0]
        results = self.vector_store.search(query_embedding, k)
        return results