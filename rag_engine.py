import faiss
import numpy as np

class VectorDB:
    def __init__(self, embeddings, documents):
        self.documents = documents
        self.index = faiss.IndexFlatL2(len(embeddings[0]))
        self.index.add(np.array(embeddings))

    def search(self, query_embedding, k=5):
        import numpy as np
        query_embedding = np.array(query_embedding)
        distances, indices = self.index.search(query_embedding, k)
        return [self.documents[i] for i in indices[0]]