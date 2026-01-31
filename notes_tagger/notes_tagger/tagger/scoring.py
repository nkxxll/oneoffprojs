"""Similarity and ranking logic."""

import numpy as np
from numpy import ndarray

from notes_tagger.models import TagScore


def cosine_similarity(a: ndarray, b: ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def cosine_similarity_matrix(query: ndarray, corpus: ndarray) -> ndarray:
    """Compute cosine similarity between query and all corpus vectors.
    
    Args:
        query: Single embedding vector (embedding_dim,)
        corpus: Matrix of embeddings (num_topics, embedding_dim)
    
    Returns:
        Array of similarities (num_topics,)
    """
    query_norm = query / np.linalg.norm(query)
    corpus_norms = corpus / np.linalg.norm(corpus, axis=1, keepdims=True)
    return np.dot(corpus_norms, query_norm)


def rank_topics(
    similarities: ndarray,
    topic_names: list[str],
    threshold: float,
    max_tags: int,
) -> list[TagScore]:
    """Rank topics by similarity and filter by threshold.
    
    Args:
        similarities: Array of similarity scores
        topic_names: Names of topics in same order as similarities
        threshold: Minimum similarity to include
        max_tags: Maximum number of tags to return
    
    Returns:
        List of TagScore sorted by score descending
    """
    scored = [(name, float(sim)) for name, sim in zip(topic_names, similarities)]
    scored = [(name, sim) for name, sim in scored if sim >= threshold]
    scored.sort(key=lambda x: x[1], reverse=True)
    scored = scored[:max_tags]
    
    return [TagScore(topic=name, score=sim) for name, sim in scored]
