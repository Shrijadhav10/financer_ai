"""Cache embeddings to disk for faster subsequent loads."""

import os
import pickle
import numpy as np
from pathlib import Path

CACHE_DIR = Path(__file__).parent / ".cache"

def get_cache_path(data_file):
    """Generate cache file path based on data file."""
    CACHE_DIR.mkdir(exist_ok=True)
    file_hash = hash(str(Path(data_file).resolve()))
    return CACHE_DIR / f"embeddings_{file_hash}.pkl"

def save_embeddings_cache(embeddings, data_file):
    """Save embeddings to disk cache."""
    try:
        cache_path = get_cache_path(data_file)
        with open(cache_path, 'wb') as f:
            pickle.dump(embeddings, f)
        print(f"✓ Embeddings cached to {cache_path}")
    except Exception as e:
        print(f"Warning: Could not cache embeddings: {e}")

def load_embeddings_cache(data_file):
    """Load embeddings from disk cache if available."""
    try:
        cache_path = get_cache_path(data_file)
        if cache_path.exists():
            with open(cache_path, 'rb') as f:
                embeddings = pickle.load(f)
            print(f"✓ Loaded cached embeddings from {cache_path}")
            return embeddings
    except Exception as e:
        print(f"Warning: Could not load cached embeddings: {e}")
    
    return None

def clear_cache():
    """Clear all cached embeddings."""
    try:
        import shutil
        if CACHE_DIR.exists():
            shutil.rmtree(CACHE_DIR)
            print("✓ Cache cleared")
    except Exception as e:
        print(f"Warning: Could not clear cache: {e}")
