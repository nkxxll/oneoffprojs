"""Note-to-note linking module."""

from notes_tagger.linker.config import LinkConfig
from notes_tagger.linker.engine import LinkingEngine
from notes_tagger.linker.store import EmbeddingStore
from notes_tagger.models import NoteLink, LinkResult

__all__ = [
    "LinkConfig",
    "LinkingEngine",
    "EmbeddingStore",
    "NoteLink",
    "LinkResult",
]
