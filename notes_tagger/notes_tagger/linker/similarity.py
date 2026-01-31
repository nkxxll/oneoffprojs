"""Similarity computation utilities for note linking."""

import numpy as np
from numpy import ndarray


def compute_similarity_scores(embeddings: ndarray, query_idx: int) -> ndarray:
    """Compute cosine similarity scores between a query and all embeddings.
    
    Args:
        embeddings: Normalized embedding matrix (N x D)
        query_idx: Index of the query embedding
        
    Returns:
        Array of similarity scores (N,)
    """
    query = embeddings[query_idx]
    return embeddings @ query


def find_top_k_neighbors(
    scores: ndarray,
    exclude_idx: int,
    threshold: float,
    max_results: int,
) -> list[tuple[int, float]]:
    """Find top-K neighbors above threshold.
    
    Args:
        scores: Similarity scores array
        exclude_idx: Index to exclude (usually self)
        threshold: Minimum similarity threshold
        max_results: Maximum number of results
        
    Returns:
        List of (index, score) tuples, sorted by score descending
    """
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    
    results = []
    for idx, score in ranked:
        if idx == exclude_idx:
            continue
        if score < threshold:
            break
        if len(results) >= max_results:
            break
        results.append((idx, float(score)))
    
    return results
