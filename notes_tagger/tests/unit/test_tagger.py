"""Unit tests for tagger module."""

import numpy as np
import pytest

from notes_tagger.tagger.scoring import (
    cosine_similarity,
    cosine_similarity_matrix,
    rank_topics,
)
from notes_tagger.models import TagScore


class TestCosineSimilarity:
    def test_identical_vectors(self):
        a = np.array([1.0, 0.0, 0.0])
        sim = cosine_similarity(a, a)
        assert pytest.approx(sim, abs=1e-6) == 1.0

    def test_orthogonal_vectors(self):
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 1.0])
        sim = cosine_similarity(a, b)
        assert pytest.approx(sim, abs=1e-6) == 0.0

    def test_opposite_vectors(self):
        a = np.array([1.0, 0.0])
        b = np.array([-1.0, 0.0])
        sim = cosine_similarity(a, b)
        assert pytest.approx(sim, abs=1e-6) == -1.0

    def test_similar_vectors(self):
        a = np.array([1.0, 1.0])
        b = np.array([1.0, 0.9])
        sim = cosine_similarity(a, b)
        assert sim > 0.9


class TestCosineSimilarityMatrix:
    def test_single_query_multiple_corpus(self):
        query = np.array([1.0, 0.0])
        corpus = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
        sims = cosine_similarity_matrix(query, corpus)

        assert len(sims) == 3
        assert pytest.approx(sims[0], abs=1e-6) == 1.0
        assert pytest.approx(sims[1], abs=1e-6) == 0.0
        assert sims[2] > 0.5

    def test_normalized_vectors(self):
        query = np.array([0.6, 0.8])
        corpus = np.array([[0.6, 0.8], [0.8, 0.6]])
        sims = cosine_similarity_matrix(query, corpus)

        assert pytest.approx(sims[0], abs=1e-6) == 1.0
        assert sims[1] < 1.0


class TestRankTopics:
    def test_rank_and_filter(self):
        similarities = np.array([0.8, 0.4, 0.6, 0.2])
        topic_names = ["a", "b", "c", "d"]
        
        result = rank_topics(similarities, topic_names, threshold=0.3, max_tags=3)
        
        assert len(result) == 3
        assert result[0].topic == "a"
        assert result[0].score == 0.8
        assert result[1].topic == "c"
        assert result[2].topic == "b"

    def test_threshold_filters(self):
        similarities = np.array([0.5, 0.3, 0.1])
        topic_names = ["a", "b", "c"]
        
        result = rank_topics(similarities, topic_names, threshold=0.4, max_tags=10)
        
        assert len(result) == 1
        assert result[0].topic == "a"

    def test_max_tags_limits(self):
        similarities = np.array([0.9, 0.8, 0.7, 0.6])
        topic_names = ["a", "b", "c", "d"]
        
        result = rank_topics(similarities, topic_names, threshold=0.0, max_tags=2)
        
        assert len(result) == 2

    def test_empty_result(self):
        similarities = np.array([0.1, 0.2])
        topic_names = ["a", "b"]
        
        result = rank_topics(similarities, topic_names, threshold=0.5, max_tags=10)
        
        assert len(result) == 0

    def test_returns_tag_scores(self):
        similarities = np.array([0.75])
        topic_names = ["finance"]
        
        result = rank_topics(similarities, topic_names, threshold=0.0, max_tags=5)
        
        assert len(result) == 1
        assert isinstance(result[0], TagScore)
        assert result[0].topic == "finance"
        assert result[0].score == 0.75
