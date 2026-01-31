"""Embedding model and utilities."""

from notes_tagger.embeddings.model import EmbeddingModel
from notes_tagger.embeddings.cache import EmbeddingCache
from notes_tagger.embeddings.utils import (
    normalize_embedding,
    normalize_embeddings,
    chunk_texts,
    average_embeddings,
    weighted_average_embeddings,
)

__all__ = [
    "EmbeddingModel",
    "EmbeddingCache",
    "normalize_embedding",
    "normalize_embeddings",
    "chunk_texts",
    "average_embeddings",
    "weighted_average_embeddings",
]
