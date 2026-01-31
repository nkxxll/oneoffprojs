"""Pydantic data models for notes tagger."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ModelType(str, Enum):
    MPNET = "all-mpnet-base-v2"
    MINILM = "all-MiniLM-L6-v2"


class TagScore(BaseModel):
    """A topic tag with similarity score."""

    topic: str
    score: float = Field(..., ge=0.0, le=1.0)


class Note(BaseModel):
    """A single note to be tagged."""

    id: str
    title: str
    body: str
    tags: Optional[list[str]] = None


class TagResult(BaseModel):
    """Tagging result for a single note."""

    note_id: str
    note_title: str
    tags: list[TagScore]

    def sort_by_score(self) -> "TagResult":
        """Return copy sorted by score descending."""
        sorted_tags = sorted(self.tags, key=lambda t: t.score, reverse=True)
        return TagResult(
            note_id=self.note_id, note_title=self.note_title, tags=sorted_tags
        )


class Config(BaseModel):
    """Configuration for tagging engine."""

    topics: dict[str, str] = Field(
        ..., description="Topic name -> semantic description mapping"
    )
    threshold: float = Field(default=0.35, ge=0.0, le=1.0)
    max_tags: int = Field(default=3, ge=1)
    model_name: ModelType = ModelType.MPNET
    cache_dir: str = Field(default="./cache")
    device: Optional[str] = None
    ignore_files: list[str] = Field(
        default_factory=lambda: ["backup.md", "backlog.txt"],
        description="List of filenames to ignore during processing",
    )

    @field_validator("topics")
    @classmethod
    def topics_not_empty(cls, v: dict[str, str]) -> dict[str, str]:
        if not v:
            raise ValueError("Must define at least one topic")
        return v


class EmbeddingMetadata(BaseModel):
    """Metadata for cached embeddings."""

    model_name: str
    num_topics: int
    topics: list[str]
    embedding_dim: int
    timestamp: float


class NoteLink(BaseModel):
    """A link between two notes with similarity score."""

    from_id: str
    to_id: str
    to_title: str
    similarity: float
    shared_tags: list[str] = []


class LinkResult(BaseModel):
    """Linking result for a single note."""

    note_id: str
    links: list[NoteLink]
