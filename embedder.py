from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(documents):
    """
    Create embeddings for documents.
    Uses batch processing for efficiency.
    """
    if not documents:
        return np.array([])
    
    # Batch size for processing (larger batches = faster but more memory)
    batch_size = 32
    embeddings = []
    
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        batch_embeddings = model.encode(batch, show_progress_bar=False)
        embeddings.extend(batch_embeddings)
    
    return np.array(embeddings)