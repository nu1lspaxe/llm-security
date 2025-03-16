from curses import meta
import faiss
import numpy as np
import pickle
import os

class VectorStore:
    def __init__(self, index_path="faiss_index.bin", metadata_path="faiss_metadata.pkl", dimension=384):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.dimension = dimension
        self.metadata = []
        
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            
    def add_vectors(self, vectors, metadata):
        """Add vectors and metadata to the store."""
        vectors = np.array(vectors, dtype=np.float32)
        self.index.add(vectors)
        self.metadata.extend(metadata)
        
    def search(self, query_vector, k=5):
        """Search for k nearest neighbors."""
        query_vector = np.array([query_vector], dtype=np.float32)
        distances, indices = self.index.search(query_vector, k)
        results = [self.metadata[i] for i in indices[0] if i < len(self.metadata)]
        return results
    
    def save(self):
        """Save the index and metadata to disk."""
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
            
    def get_total_vectors(self):
        """Return the total number of vectors in the index."""
        return self.index.ntotal