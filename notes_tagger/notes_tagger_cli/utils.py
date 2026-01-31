"""CLI-specific utilities."""

from pathlib import Path
from typing import Iterator

from notes_tagger.models import TagResult


ALLOWED_EXTENSIONS = {".md", ".txt", ".mdx"}


def find_markdown_files(
    directory: Path,
    recursive: bool = True,
    extensions: set[str] | None = None,
    ignore_files: list[str] | None = None,
) -> Iterator[Path]:
    """Find all text note files in a directory.
    
    Only processes plain text formats (md, txt, mdx) - not binary or source code.
    """
    if extensions is None:
        extensions = ALLOWED_EXTENSIONS
    if ignore_files is None:
        ignore_files = []
    
    ignore_set = set(ignore_files)
    pattern = "**/*" if recursive else "*"
    yield from sorted(
        p for p in directory.glob(pattern) 
        if p.is_file() and p.suffix.lower() in extensions and p.name not in ignore_set
    )


def format_tag_result(result: TagResult, verbose: bool = False) -> str:
    """Format a tag result for display."""
    if not result.tags:
        return f"  {result.note_title}: (no tags above threshold)"
    
    tags_str = ", ".join(
        f"{t.topic} ({t.score:.2f})" if verbose else t.topic
        for t in result.tags
    )
    return f"  {result.note_title}: {tags_str}"
