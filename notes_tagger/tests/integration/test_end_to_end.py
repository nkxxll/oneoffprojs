"""End-to-end integration tests for notes tagger."""

import tempfile
from pathlib import Path

import pytest

from notes_tagger import TaggingEngine, DEFAULT_CONFIG
from notes_tagger.models import Config, ModelType, Note
from notes_tagger.storage.obsidian import parse_markdown_note, apply_tags_to_note


@pytest.fixture(scope="module")
def engine():
    """Create a tagging engine with MiniLM for faster tests."""
    config = DEFAULT_CONFIG.model_copy(
        update={
            "model_name": ModelType.MINILM,
            "threshold": 0.3,
            "max_tags": 3,
        }
    )
    eng = TaggingEngine(config)
    eng.initialize()
    return eng


class TestEndToEnd:
    def test_tag_finance_text(self, engine):
        text = "Reviewed the quarterly budget and revenue forecasts for next year"
        result = engine.tag(text)
        
        tag_names = [t.topic for t in result.tags]
        assert "finance" in tag_names or "planning" in tag_names

    def test_tag_meeting_text(self, engine):
        text = "Team meeting to discuss project status, action items were assigned"
        result = engine.tag(text)
        
        tag_names = [t.topic for t in result.tags]
        assert "meeting" in tag_names

    def test_tag_research_text(self, engine):
        text = "Reading papers about machine learning algorithms and neural networks"
        result = engine.tag(text)
        
        tag_names = [t.topic for t in result.tags]
        assert "research" in tag_names

    def test_tag_note_object(self, engine):
        note = Note(
            id="test-1",
            title="Budget Review",
            body="Discussed the annual budget with the finance team",
        )
        result = engine.tag_note(note)
        
        assert result.note_id == "test-1"
        assert result.note_title == "Budget Review"
        assert len(result.tags) > 0

    def test_batch_tagging(self, engine):
        texts = [
            "Budget review and financial planning",
            "Team standup meeting notes",
            "New feature idea for the product",
        ]
        results = engine.tag_batch(texts)
        
        assert len(results) == 3
        for result in results:
            assert len(result.tags) >= 0

    def test_batch_matches_single(self, engine):
        texts = ["Budget review meeting", "New product ideas"]
        
        batch_results = engine.tag_batch(texts)
        single_results = [engine.tag(t) for t in texts]
        
        for batch, single in zip(batch_results, single_results):
            batch_topics = {t.topic for t in batch.tags}
            single_topics = {t.topic for t in single.tags}
            assert batch_topics == single_topics

    def test_deterministic_results(self, engine):
        text = "Quarterly earnings report and revenue analysis"
        
        result1 = engine.tag(text)
        result2 = engine.tag(text)
        
        assert [t.topic for t in result1.tags] == [t.topic for t in result2.tags]
        for t1, t2 in zip(result1.tags, result2.tags):
            assert abs(t1.score - t2.score) < 0.001


class TestObsidianIntegration:
    def test_tag_and_apply_to_markdown(self, engine):
        with tempfile.TemporaryDirectory() as tmpdir:
            note_path = Path(tmpdir) / "budget.md"
            note_path.write_text("# Q3 Budget\n\nReviewed quarterly budget and expenses")
            
            note = parse_markdown_note(note_path)
            result = engine.tag_note(note)
            
            if result.tags:
                tag_names = [t.topic for t in result.tags]
                apply_tags_to_note(note_path, tag_names)
                
                content = note_path.read_text()
                assert "tags:" in content

    def test_preserve_existing_content(self, engine):
        with tempfile.TemporaryDirectory() as tmpdir:
            note_path = Path(tmpdir) / "note.md"
            original = "---\nauthor: John\n---\n\n# Meeting Notes\n\nDiscussed project timeline"
            note_path.write_text(original)
            
            note = parse_markdown_note(note_path)
            result = engine.tag_note(note)
            
            if result.tags:
                tag_names = [t.topic for t in result.tags]
                apply_tags_to_note(note_path, tag_names, replace=False)
                
                content = note_path.read_text()
                assert "Meeting Notes" in content
                assert "project timeline" in content
