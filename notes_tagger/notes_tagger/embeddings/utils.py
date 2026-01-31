"""Utility functions for embeddings normalization and batch operations."""

import numpy as np
from numpy import ndarray


def normalize_embedding(embedding: ndarray) -> ndarray:
    """Normalize a single embedding to unit length."""
    norm = np.linalg.norm(embedding)
    if norm == 0:
        return embedding
    return embedding / norm


def normalize_embeddings(embeddings: ndarray) -> ndarray:
    """Normalize batch of embeddings to unit length (row-wise)."""
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1, norms)
    return embeddings / norms


def chunk_texts(texts: list[str], chunk_size: int) -> list[list[str]]:
    """Split texts into chunks for batch processing."""
    return [texts[i : i + chunk_size] for i in range(0, len(texts), chunk_size)]


def average_embeddings(embeddings: ndarray) -> ndarray:
    """Compute the average of multiple embeddings."""
    return np.mean(embeddings, axis=0)


def weighted_average_embeddings(embeddings: ndarray, weights: list[float]) -> ndarray:
    """Compute weighted average of multiple embeddings."""
    weights_arr = np.array(weights).reshape(-1, 1)
    weighted = embeddings * weights_arr
    return np.sum(weighted, axis=0) / np.sum(weights_arr)
