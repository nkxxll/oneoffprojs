"""Main tagging engine."""

from typing import Optional

import numpy as np
from numpy import ndarray

from notes_tagger.embeddings.cache import EmbeddingCache
from notes_tagger.embeddings.model import EmbeddingModel
from notes_tagger.exceptions import ModelNotInitializedError
from notes_tagger.models import Config, Note, TagResult, TagScore
from notes_tagger.tagger.scoring import cosine_similarity_matrix, rank_topics


class TaggingEngine:
    """Main engine for tagging notes using semantic similarity."""

    def __init__(self, config: Config):
        self.config = config
        self._model: Optional[EmbeddingModel] = None
        self._topic_embeddings: Optional[ndarray] = None
        self._topic_names: list[str] = list(config.topics.keys())
        self._cache = EmbeddingCache(config.cache_dir)
        self._initialized = False

    def initialize(self, force_reload: bool = False) -> None:
        """Load model and compute/cache topic embeddings."""
        self._model = EmbeddingModel(self.config.model_name, self.config.device)

        if not force_reload:
            cached = self._cache.load(self._topic_names, self._model.model_name)
            if cached is not None:
                self._topic_embeddings = cached
                self._initialized = True
                return

        topic_descriptions = [self.config.topics[name] for name in self._topic_names]
        self._topic_embeddings = self._model.embed_batch(topic_descriptions)

        self._cache.save(
            self._topic_embeddings,
            self._topic_names,
            self._model.model_name,
        )
        self._initialized = True

    def _ensure_initialized(self) -> None:
        if not self._initialized or self._model is None:
            raise ModelNotInitializedError(
                "Engine not initialized. Call initialize() first."
            )

    def tag(self, text: str, note_id: str = "", note_title: str = "") -> TagResult:
        """Tag a single text and return results."""
        self._ensure_initialized()
        assert self._model is not None
        assert self._topic_embeddings is not None

        embedding = self._model.embed(text)
        similarities = cosine_similarity_matrix(embedding, self._topic_embeddings)
        
        tags = rank_topics(
            similarities,
            self._topic_names,
            self.config.threshold,
            self.config.max_tags,
        )

        return TagResult(note_id=note_id, note_title=note_title, tags=tags)

    def tag_note(self, note: Note) -> TagResult:
        """Tag a Note object."""
        combined = f"{note.title}\n\n{note.body}"
        return self.tag(combined, note_id=note.id, note_title=note.title)

    def tag_batch(
        self, texts: list[str], ids: Optional[list[str]] = None, titles: Optional[list[str]] = None
    ) -> list[TagResult]:
        """Tag multiple texts in batch."""
        self._ensure_initialized()
        assert self._model is not None
        assert self._topic_embeddings is not None

        if ids is None:
            ids = [f"note_{i}" for i in range(len(texts))]
        if titles is None:
            titles = ["" for _ in texts]

        embeddings = self._model.embed_batch(texts)
        
        results = []
        for i, embedding in enumerate(embeddings):
            similarities = cosine_similarity_matrix(embedding, self._topic_embeddings)
            tags = rank_topics(
                similarities,
                self._topic_names,
                self.config.threshold,
                self.config.max_tags,
            )
            results.append(TagResult(note_id=ids[i], note_title=titles[i], tags=tags))

        return results
