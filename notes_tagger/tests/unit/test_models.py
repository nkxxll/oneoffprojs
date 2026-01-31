"""Unit tests for models."""

import pytest
from pydantic import ValidationError

from notes_tagger.models import (
    Config,
    EmbeddingMetadata,
    ModelType,
    Note,
    TagResult,
    TagScore,
)


class TestTagScore:
    def test_valid_tag_score(self):
        tag = TagScore(topic="finance", score=0.75)
        assert tag.topic == "finance"
        assert tag.score == 0.75

    def test_score_at_boundaries(self):
        low = TagScore(topic="test", score=0.0)
        high = TagScore(topic="test", score=1.0)
        assert low.score == 0.0
        assert high.score == 1.0

    def test_score_out_of_bounds(self):
        with pytest.raises(ValidationError):
            TagScore(topic="test", score=1.5)
        with pytest.raises(ValidationError):
            TagScore(topic="test", score=-0.1)


class TestNote:
    def test_note_with_all_fields(self):
        note = Note(id="1", title="Test", body="Content", tags=["finance"])
        assert note.id == "1"
        assert note.title == "Test"
        assert note.body == "Content"
        assert note.tags == ["finance"]

    def test_note_without_tags(self):
        note = Note(id="1", title="Test", body="Content")
        assert note.tags is None

    def test_note_with_empty_tags(self):
        note = Note(id="1", title="Test", body="Content", tags=[])
        assert note.tags == []


class TestTagResult:
    def test_tag_result_creation(self):
        tags = [TagScore(topic="finance", score=0.8), TagScore(topic="meeting", score=0.6)]
        result = TagResult(note_id="1", note_title="Test", tags=tags)
        assert result.note_id == "1"
        assert len(result.tags) == 2

    def test_sort_by_score(self):
        tags = [
            TagScore(topic="low", score=0.3),
            TagScore(topic="high", score=0.9),
            TagScore(topic="mid", score=0.6),
        ]
        result = TagResult(note_id="1", note_title="Test", tags=tags)
        sorted_result = result.sort_by_score()

        assert sorted_result.tags[0].topic == "high"
        assert sorted_result.tags[1].topic == "mid"
        assert sorted_result.tags[2].topic == "low"


class TestConfig:
    def test_config_with_topics(self):
        config = Config(topics={"finance": "money"})
        assert "finance" in config.topics
        assert config.threshold == 0.35
        assert config.max_tags == 3
        assert config.model_name == ModelType.MPNET

    def test_config_empty_topics_fails(self):
        with pytest.raises(ValidationError):
            Config(topics={})

    def test_config_custom_threshold(self):
        config = Config(topics={"test": "desc"}, threshold=0.5)
        assert config.threshold == 0.5

    def test_config_invalid_threshold(self):
        with pytest.raises(ValidationError):
            Config(topics={"test": "desc"}, threshold=1.5)


class TestEmbeddingMetadata:
    def test_embedding_metadata(self):
        meta = EmbeddingMetadata(
            model_name="test-model",
            num_topics=5,
            topics=["a", "b", "c", "d", "e"],
            embedding_dim=768,
            timestamp=1234567890.0,
        )
        assert meta.model_name == "test-model"
        assert meta.num_topics == 5
        assert len(meta.topics) == 5
        assert meta.embedding_dim == 768


class TestModelType:
    def test_model_type_values(self):
        assert ModelType.MPNET.value == "all-mpnet-base-v2"
        assert ModelType.MINILM.value == "all-MiniLM-L6-v2"
