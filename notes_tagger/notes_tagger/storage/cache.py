"""Generic pickle serialization cache for storage."""

import pickle
from pathlib import Path
from typing import Any, Optional


class PickleCache:
    """Generic pickle-based cache for serializable objects."""

    def __init__(self, cache_dir: str | Path):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_path(self, key: str) -> Path:
        """Get the file path for a cache key."""
        safe_key = "".join(c if c.isalnum() or c in "-_" else "_" for c in key)
        return self.cache_dir / f"{safe_key}.pkl"

    def save(self, key: str, data: Any) -> None:
        """Save data to cache."""
        path = self._get_path(key)
        with open(path, "wb") as f:
            pickle.dump(data, f)

    def load(self, key: str) -> Optional[Any]:
        """Load data from cache. Returns None if not found."""
        path = self._get_path(key)
        if not path.exists():
            return None
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except Exception:
            return None

    def exists(self, key: str) -> bool:
        """Check if a cache key exists."""
        return self._get_path(key).exists()

    def delete(self, key: str) -> bool:
        """Delete a cache entry. Returns True if deleted."""
        path = self._get_path(key)
        if path.exists():
            path.unlink()
            return True
        return False

    def clear(self) -> int:
        """Clear all cache files. Returns number of files deleted."""
        count = 0
        for path in self.cache_dir.glob("*.pkl"):
            path.unlink()
            count += 1
        return count

    def list_keys(self) -> list[str]:
        """List all cache keys."""
        return [p.stem for p in self.cache_dir.glob("*.pkl")]
