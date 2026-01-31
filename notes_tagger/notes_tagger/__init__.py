"""Notes Tagger - Semantic note tagging using sentence embeddings."""

from notes_tagger.models import (
    Config,
    ModelType,
    Note,
    TagResult,
    TagScore,
    NoteLink,
    LinkResult,
)
from notes_tagger.config import DEFAULT_CONFIG, load_config
from notes_tagger.tagger.engine import TaggingEngine
from notes_tagger.linker import LinkConfig, LinkingEngine

__all__ = [
    "Config",
    "ModelType",
    "Note",
    "TagResult",
    "TagScore",
    "NoteLink",
    "LinkResult",
    "DEFAULT_CONFIG",
    "load_config",
    "TaggingEngine",
    "LinkConfig",
    "LinkingEngine",
]
