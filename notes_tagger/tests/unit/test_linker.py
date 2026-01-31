"""Unit tests for the linker module."""

import tempfile
from pathlib import Path

import numpy as np
import pytest

from notes_tagger.linker.config import LinkConfig
from notes_tagger.linker.similarity import compute_similarity_scores, find_top_k_neighbors
from notes_tagger.models import Note, NoteLink


class TestLinkConfig:
    def test_default_values(self):
        config = LinkConfig()
        assert config.threshold == 0.45
        assert config.max_links == 5
        assert config.require_shared_tag is False

    def test_custom_values(self):
        config = LinkConfig(threshold=0.6, max_links=3, require_shared_tag=True)
        assert config.threshold == 0.6
        assert config.max_links == 3
        assert config.require_shared_tag is True

    def test_threshold_validation(self):
        with pytest.raises(ValueError):
            LinkConfig(threshold=1.5)
        with pytest.raises(ValueError):
            LinkConfig(threshold=-0.1)

    def test_max_links_validation(self):
        with pytest.raises(ValueError):
            LinkConfig(max_links=0)


class TestSimilarity:
    def test_compute_similarity_scores(self):
        embeddings = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 0.0],
        ])
        
        scores = compute_similarity_scores(embeddings, 0)
        
        assert scores[0] == 1.0
        assert scores[1] == 0.0
        assert scores[2] == 1.0

    def test_find_top_k_neighbors(self):
        scores = np.array([1.0, 0.8, 0.5, 0.3, 0.1])
        
        neighbors = find_top_k_neighbors(
            scores,
            exclude_idx=0,
            threshold=0.4,
            max_results=2,
        )
        
        assert len(neighbors) == 2
        assert neighbors[0] == (1, 0.8)
        assert neighbors[1] == (2, 0.5)

    def test_find_top_k_neighbors_respects_threshold(self):
        scores = np.array([1.0, 0.3, 0.2, 0.1])
        
        neighbors = find_top_k_neighbors(
            scores,
            exclude_idx=0,
            threshold=0.5,
            max_results=10,
        )
        
        assert len(neighbors) == 0

    def test_find_top_k_neighbors_excludes_self(self):
        scores = np.array([1.0, 0.9, 0.8])
        
        neighbors = find_top_k_neighbors(
            scores,
            exclude_idx=0,
            threshold=0.0,
            max_results=10,
        )
        
        assert all(idx != 0 for idx, _ in neighbors)


class TestNoteLink:
    def test_note_link_model(self):
        link = NoteLink(
            from_id="note1",
            to_id="note2",
            to_title="Note Two",
            similarity=0.75,
            shared_tags=["finance"],
        )
        
        assert link.from_id == "note1"
        assert link.to_id == "note2"
        assert link.to_title == "Note Two"
        assert link.similarity == 0.75
        assert link.shared_tags == ["finance"]

    def test_note_link_default_shared_tags(self):
        link = NoteLink(
            from_id="a",
            to_id="b",
            to_title="B",
            similarity=0.5,
        )
        
        assert link.shared_tags == []


class TestObsidianBacklinks:
    def test_add_backlinks(self):
        from notes_tagger.storage.obsidian import ObsidianNote
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("---\ntitle: Test Note\n---\n\nSome content here.")
            f.flush()
            
            links = [
                NoteLink(from_id="test", to_id="a", to_title="Note A", similarity=0.8),
                NoteLink(from_id="test", to_id="b", to_title="Note B", similarity=0.7),
            ]
            
            note = ObsidianNote(Path(f.name))
            note.add_backlinks(links)
            note.save()
            
            content = Path(f.name).read_text()
            
            assert "## Related Notes" in content
            assert "[[Note A]]" in content
            assert "[[Note B]]" in content

    def test_add_backlinks_replaces_existing(self):
        from notes_tagger.storage.obsidian import ObsidianNote
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("Content\n\n## Related Notes\n- [[Old Link]]\n")
            f.flush()
            
            links = [
                NoteLink(from_id="test", to_id="a", to_title="New Link", similarity=0.8),
            ]
            
            note = ObsidianNote(Path(f.name))
            note.add_backlinks(links)
            note.save()
            
            content = Path(f.name).read_text()
            
            assert "[[New Link]]" in content
            assert "[[Old Link]]" not in content

    def test_add_backlinks_empty_list_does_nothing(self):
        from notes_tagger.storage.obsidian import ObsidianNote
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            original = "Content here."
            f.write(original)
            f.flush()
            
            note = ObsidianNote(Path(f.name))
            note.add_backlinks([])
            note.save()
            
            content = Path(f.name).read_text()
            
            assert "Related Notes" not in content
