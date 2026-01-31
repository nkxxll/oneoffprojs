"""Custom exceptions for notes tagger."""


class NotesTaggerError(Exception):
    """Base exception for notes tagger."""
    pass


class ModelNotInitializedError(NotesTaggerError):
    """Raised when trying to use engine before initialization."""
    pass


class EmbeddingError(NotesTaggerError):
    """Raised when embedding generation fails."""
    pass
