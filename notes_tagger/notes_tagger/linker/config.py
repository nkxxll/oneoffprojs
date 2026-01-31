"""Configuration for note linking."""

from typing import Optional

from pydantic import BaseModel, Field

from notes_tagger.models import ModelType


class LinkConfig(BaseModel):
    """Configuration for note linking."""

    threshold: float = Field(default=0.45, ge=0.0, le=1.0)
    max_links: int = Field(default=5, ge=1)
    require_shared_tag: bool = False
    model_name: ModelType = ModelType.MPNET
    device: Optional[str] = None
