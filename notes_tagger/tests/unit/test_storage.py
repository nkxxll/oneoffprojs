"""Unit tests for storage module."""

import json
import tempfile
from pathlib import Path

import pytest
import yaml

from notes_tagger.models import Note, TagResult, TagScore
from notes_tagger.storage.cache import PickleCache
from notes_tagger.storage.formats import (
    load_config_from_json,
    load_config_from_yaml,
    load_notes_from_json,
    load_notes_from_yaml,
    save_notes_to_json,
    save_notes_to_yaml,
    save_results_to_json,
)
from notes_tagger.storage.obsidian import (
    ObsidianNote,
    parse_markdown_note,
    apply_tags_to_note,
)


class TestPickleCache:
    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = PickleCache(tmpdir)
            data = {"key": "value", "number": 42}
            
            cache.save("test_key", data)
            loaded = cache.load("test_key")
            
            assert loaded == data

    def test_load_nonexistent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = PickleCache(tmpdir)
            assert cache.load("nonexistent") is None

    def test_exists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = PickleCache(tmpdir)
            cache.save("exists", "data")
            
            assert cache.exists("exists")
            assert not cache.exists("not_exists")

    def test_delete(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = PickleCache(tmpdir)
            cache.save("to_delete", "data")
            
            assert cache.delete("to_delete")
            assert not cache.exists("to_delete")
            assert not cache.delete("already_gone")

    def test_clear(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = PickleCache(tmpdir)
            cache.save("a", 1)
            cache.save("b", 2)
            
            count = cache.clear()
            
            assert count == 2
            assert len(cache.list_keys()) == 0

    def test_list_keys(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = PickleCache(tmpdir)
            cache.save("key1", 1)
            cache.save("key2", 2)
            
            keys = cache.list_keys()
            
            assert set(keys) == {"key1", "key2"}


class TestFormatsJson:
    def test_load_notes_from_json(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump([
                {"id": "1", "title": "Test", "body": "Content"},
                {"id": "2", "title": "Test2", "body": "Content2"},
            ], f)
            f.flush()
            
            notes = load_notes_from_json(f.name)
            
            assert len(notes) == 2
            assert notes[0].id == "1"
            assert notes[1].title == "Test2"

    def test_save_notes_to_json(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            notes = [Note(id="1", title="Test", body="Content")]
            save_notes_to_json(notes, f.name)
            
            with open(f.name) as rf:
                data = json.load(rf)
            
            assert len(data) == 1
            assert data[0]["id"] == "1"

    def test_save_results_to_json(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            results = [
                TagResult(
                    note_id="1",
                    note_title="Test",
                    tags=[TagScore(topic="finance", score=0.8)],
                )
            ]
            save_results_to_json(results, f.name)
            
            with open(f.name) as rf:
                data = json.load(rf)
            
            assert len(data) == 1
            assert data[0]["tags"][0]["topic"] == "finance"


class TestFormatsYaml:
    def test_load_notes_from_yaml(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump([
                {"id": "1", "title": "Test", "body": "Content"},
            ], f)
            f.flush()
            
            notes = load_notes_from_yaml(f.name)
            
            assert len(notes) == 1
            assert notes[0].id == "1"

    def test_save_notes_to_yaml(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            notes = [Note(id="1", title="Test", body="Content")]
            save_notes_to_yaml(notes, f.name)
            
            with open(f.name) as rf:
                data = yaml.safe_load(rf)
            
            assert len(data) == 1
            assert data[0]["id"] == "1"

    def test_load_config_from_yaml(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump({"threshold": 0.5, "max_tags": 5}, f)
            f.flush()
            
            config = load_config_from_yaml(f.name)
            
            assert config["threshold"] == 0.5
            assert config["max_tags"] == 5

    def test_load_config_from_json(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"threshold": 0.4}, f)
            f.flush()
            
            config = load_config_from_json(f.name)
            
            assert config["threshold"] == 0.4


class TestObsidianNote:
    def test_parse_with_frontmatter(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("---\ntitle: My Note\ntags:\n  - existing\n---\n\n# Heading\n\nContent here")
            f.flush()
            
            note = parse_markdown_note(Path(f.name))
            
            assert note.title == "My Note"
            assert note.tags == ["existing"]
            assert "Content here" in note.body

    def test_parse_without_frontmatter(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# My Title\n\nSome content")
            f.flush()
            
            note = parse_markdown_note(Path(f.name))
            
            assert note.title == "My Title"
            assert note.tags is None

    def test_parse_title_from_filename(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "my-note-file.md"
            path.write_text("Just content, no heading")
            
            note = parse_markdown_note(path)
            
            assert note.title == "my-note-file"

    def test_obsidian_note_add_tags_append(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("---\ntags:\n  - existing\n---\n\nContent")
            f.flush()
            
            obs_note = ObsidianNote(Path(f.name))
            obs_note.add_tags(["new", "another"], replace=False)
            
            assert set(obs_note.tags) == {"existing", "new", "another"}

    def test_obsidian_note_add_tags_replace(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("---\ntags:\n  - existing\n---\n\nContent")
            f.flush()
            
            obs_note = ObsidianNote(Path(f.name))
            obs_note.add_tags(["new"], replace=True)
            
            assert obs_note.tags == ["new"]

    def test_obsidian_note_save(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Title\n\nContent")
            f.flush()
            
            obs_note = ObsidianNote(Path(f.name))
            obs_note.add_tags(["finance"])
            obs_note.save()
            
            content = Path(f.name).read_text()
            assert "tags:" in content
            assert "finance" in content

    def test_apply_tags_to_note(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Title\n\nContent")
            f.flush()
            path = Path(f.name)
            
            apply_tags_to_note(path, ["tag1", "tag2"])
            
            content = path.read_text()
            assert "tag1" in content
            assert "tag2" in content
