"""Unit tests for embeddings module."""

import tempfile
from pathlib import Path

import numpy as np
import pytest

from notes_tagger.embeddings.cache import EmbeddingCache
from notes_tagger.embeddings.utils import (
    average_embeddings,
    chunk_texts,
    normalize_embedding,
    normalize_embeddings,
    weighted_average_embeddings,
)


class TestNormalizeEmbedding:
    def test_normalize_single_embedding(self):
        embedding = np.array([3.0, 4.0])
        normalized = normalize_embedding(embedding)
        np.testing.assert_almost_equal(np.linalg.norm(normalized), 1.0)

    def test_normalize_zero_vector(self):
        embedding = np.array([0.0, 0.0, 0.0])
        normalized = normalize_embedding(embedding)
        np.testing.assert_array_equal(normalized, embedding)


class TestNormalizeEmbeddings:
    def test_normalize_batch(self):
        embeddings = np.array([[3.0, 4.0], [1.0, 0.0], [0.0, 2.0]])
        normalized = normalize_embeddings(embeddings)
        
        for row in normalized:
            np.testing.assert_almost_equal(np.linalg.norm(row), 1.0)

    def test_normalize_with_zero_row(self):
        embeddings = np.array([[3.0, 4.0], [0.0, 0.0]])
        normalized = normalize_embeddings(embeddings)
        np.testing.assert_almost_equal(np.linalg.norm(normalized[0]), 1.0)


class TestChunkTexts:
    def test_chunk_texts_even(self):
        texts = ["a", "b", "c", "d"]
        chunks = chunk_texts(texts, 2)
        assert len(chunks) == 2
        assert chunks[0] == ["a", "b"]
        assert chunks[1] == ["c", "d"]

    def test_chunk_texts_uneven(self):
        texts = ["a", "b", "c", "d", "e"]
        chunks = chunk_texts(texts, 2)
        assert len(chunks) == 3
        assert chunks[-1] == ["e"]

    def test_chunk_texts_larger_than_input(self):
        texts = ["a", "b"]
        chunks = chunk_texts(texts, 10)
        assert len(chunks) == 1
        assert chunks[0] == ["a", "b"]


class TestAverageEmbeddings:
    def test_average_embeddings(self):
        embeddings = np.array([[1.0, 2.0], [3.0, 4.0]])
        avg = average_embeddings(embeddings)
        np.testing.assert_array_equal(avg, [2.0, 3.0])


class TestWeightedAverageEmbeddings:
    def test_weighted_average(self):
        embeddings = np.array([[0.0, 0.0], [2.0, 4.0]])
        weights = [0.0, 1.0]
        avg = weighted_average_embeddings(embeddings, weights)
        np.testing.assert_array_equal(avg, [2.0, 4.0])

    def test_equal_weights(self):
        embeddings = np.array([[1.0, 2.0], [3.0, 4.0]])
        weights = [1.0, 1.0]
        avg = weighted_average_embeddings(embeddings, weights)
        np.testing.assert_array_equal(avg, [2.0, 3.0])


class TestEmbeddingCache:
    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = EmbeddingCache(tmpdir)
            embeddings = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
            topics = ["finance", "meeting"]
            model_name = "test-model"

            cache.save(embeddings, topics, model_name)
            loaded = cache.load(topics, model_name)

            np.testing.assert_array_equal(loaded, embeddings)

    def test_load_wrong_model(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = EmbeddingCache(tmpdir)
            embeddings = np.array([[1.0, 2.0]])
            topics = ["test"]
            
            cache.save(embeddings, topics, "model-a")
            loaded = cache.load(topics, "model-b")
            
            assert loaded is None

    def test_load_wrong_topics(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = EmbeddingCache(tmpdir)
            embeddings = np.array([[1.0, 2.0]])
            
            cache.save(embeddings, ["topic-a"], "model")
            loaded = cache.load(["topic-b"], "model")
            
            assert loaded is None

    def test_load_nonexistent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = EmbeddingCache(tmpdir)
            loaded = cache.load(["any"], "any")
            assert loaded is None

    def test_clear(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = EmbeddingCache(tmpdir)
            embeddings = np.array([[1.0, 2.0]])
            cache.save(embeddings, ["test"], "model")
            
            cache.clear()
            
            assert not cache.embeddings_file.exists()
            assert not cache.metadata_file.exists()
