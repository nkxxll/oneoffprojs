"""Caching logic for embeddings."""

import pickle
import time
from pathlib import Path
from typing import Optional

import numpy as np
from numpy import ndarray

from notes_tagger.models import EmbeddingMetadata


class EmbeddingCache:
    """Cache for topic embeddings."""

    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.embeddings_file = self.cache_dir / "topic_embeddings.pkl"
        self.metadata_file = self.cache_dir / "topic_metadata.pkl"

    def save(
        self,
        embeddings: ndarray,
        topics: list[str],
        model_name: str,
    ) -> None:
        """Save embeddings and metadata to cache."""
        metadata = EmbeddingMetadata(
            model_name=model_name,
            num_topics=len(topics),
            topics=topics,
            embedding_dim=embeddings.shape[1],
            timestamp=time.time(),
        )

        with open(self.embeddings_file, "wb") as f:
            pickle.dump(embeddings, f)

        with open(self.metadata_file, "wb") as f:
            pickle.dump(metadata.model_dump(), f)

    def load(
        self, expected_topics: list[str], model_name: str
    ) -> Optional[ndarray]:
        """Load cached embeddings if valid, else return None."""
        if not self.embeddings_file.exists() or not self.metadata_file.exists():
            return None

        try:
            with open(self.metadata_file, "rb") as f:
                metadata_dict = pickle.load(f)
            metadata = EmbeddingMetadata(**metadata_dict)

            if metadata.model_name != model_name:
                return None
            if metadata.topics != expected_topics:
                return None

            with open(self.embeddings_file, "rb") as f:
                embeddings = pickle.load(f)

            return embeddings

        except Exception:
            return None

    def clear(self) -> None:
        """Clear the cache."""
        if self.embeddings_file.exists():
            self.embeddings_file.unlink()
        if self.metadata_file.exists():
            self.metadata_file.unlink()
