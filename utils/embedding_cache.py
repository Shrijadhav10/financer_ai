"""Cache embeddings to disk for faster subsequent loads.

Cache invalidation strategy:
- The cache key is derived from the data file's name + size + last-modified
  time, NOT just its path. This means that if `finance_curated.csv` is
  regenerated with new/changed expense rows, its mtime and/or size will
  change, the cache key changes, and the old (stale) cache is automatically
  skipped in favor of regenerating fresh embeddings.
- Embeddings and the documents list they were generated from are cached
  TOGETHER as one object, so they can never get out of sync with each other
  (e.g. embedding[5] always corresponds to documents[5] for that cache entry).
"""

import pickle
from pathlib import Path

CACHE_DIR = Path(__file__).parent / ".cache"


def _cache_key(data_file):
    """Build a cache key from filename + size + mtime.

    Using size+mtime (instead of hashing file content) is a cheap freshness
    check: any edit to the file changes its mtime, and most edits change
    its size too, so a stale cache is detected without reading the file.
    """
    path = Path(data_file).resolve()
    stat = path.stat()
    # mtime_ns avoids float-precision rounding issues vs st_mtime
    return f"{path.name}_{stat.st_size}_{stat.st_mtime_ns}"


def get_cache_path(data_file):
    """Generate cache file path based on the data file's current state."""
    CACHE_DIR.mkdir(exist_ok=True)
    key = _cache_key(data_file)
    return CACHE_DIR / f"embeddings_{key}.pkl"


def save_embeddings_cache(embeddings, documents, data_file):
    """Save embeddings AND the documents they correspond to, as one unit.

    Storing them together guarantees that loading the cache later can never
    pair embeddings from one data version with documents from another.
    """
    try:
        cache_path = get_cache_path(data_file)
        payload = {"embeddings": embeddings, "documents": documents}
        with open(cache_path, "wb") as f:
            pickle.dump(payload, f)
        print(f"✓ Embeddings + documents cached to {cache_path}")
    except Exception as e:
        print(f"Warning: Could not cache embeddings: {e}")


def load_embeddings_cache(data_file):
    """Load (embeddings, documents) from disk cache if available and fresh.

    Returns (None, None) if there's no cache for the CURRENT state of
    data_file (i.e. the file changed since it was last cached), so the
    caller will regenerate embeddings from scratch — this is what fixes
    the stale-data bug, since a changed file naturally produces a
    different cache key.
    """
    try:
        cache_path = get_cache_path(data_file)
        if cache_path.exists():
            with open(cache_path, "rb") as f:
                payload = pickle.load(f)
            print(f"✓ Loaded cached embeddings from {cache_path}")
            return payload["embeddings"], payload["documents"]
    except Exception as e:
        print(f"Warning: Could not load cached embeddings: {e}")

    return None, None


def clear_cache():
    """Clear all cached embeddings (e.g. for manual troubleshooting)."""
    try:
        import shutil
        if CACHE_DIR.exists():
            shutil.rmtree(CACHE_DIR)
            print("✓ Cache cleared")
    except Exception as e:
        print(f"Warning: Could not clear cache: {e}")