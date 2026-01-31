"""Obsidian markdown file handling with YAML frontmatter."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, TYPE_CHECKING

import aiofiles
import yaml

from notes_tagger.models import Note

if TYPE_CHECKING:
    from notes_tagger.models import NoteLink


FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


def _parse_content_to_note(path: Path, content: str) -> Note:
    """Parse markdown content into a Note object."""
    frontmatter: dict = {}
    body = content
    
    match = FRONTMATTER_PATTERN.match(content)
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            frontmatter = {}
        body = content[match.end():]
    
    title = frontmatter.get("title", "")
    if not title:
        for line in body.split("\n"):
            line = line.strip()
            if line.startswith("# "):
                title = line[2:].strip()
                break
    
    if not title:
        title = path.stem
    
    existing_tags = frontmatter.get("tags", [])
    if isinstance(existing_tags, str):
        existing_tags = [existing_tags]
    
    return Note(
        id=str(path),
        title=title,
        body=body.strip(),
        tags=existing_tags if existing_tags else None,
    )


def parse_markdown_note(path: Path) -> Note:
    """Parse a markdown file into a Note object."""
    content = path.read_text(encoding="utf-8")
    return _parse_content_to_note(path, content)


async def parse_markdown_note_async(path: Path) -> Note:
    """Parse a markdown file into a Note object asynchronously."""
    async with aiofiles.open(path, encoding="utf-8") as f:
        content = await f.read()
    return _parse_content_to_note(path, content)


class ObsidianNote:
    """Represents an Obsidian markdown note with frontmatter handling."""

    def __init__(self, path: Path):
        self.path = path
        self._content = path.read_text(encoding="utf-8")
        self._frontmatter: dict = {}
        self._body = self._content
        self._parse()

    def _parse(self) -> None:
        """Parse frontmatter and body from content."""
        match = FRONTMATTER_PATTERN.match(self._content)
        if match:
            try:
                self._frontmatter = yaml.safe_load(match.group(1)) or {}
            except yaml.YAMLError:
                self._frontmatter = {}
            self._body = self._content[match.end():]
        else:
            self._frontmatter = {}
            self._body = self._content

    @property
    def title(self) -> str:
        """Get note title from frontmatter or first heading."""
        if "title" in self._frontmatter:
            return self._frontmatter["title"]
        
        for line in self._body.split("\n"):
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
        
        return self.path.stem

    @property
    def body(self) -> str:
        """Get note body (without frontmatter)."""
        return self._body.strip()

    @property
    def tags(self) -> list[str]:
        """Get existing tags from frontmatter."""
        tags = self._frontmatter.get("tags", [])
        if isinstance(tags, str):
            return [tags]
        return tags or []

    def get_combined_text(self) -> str:
        """Get title + body for embedding."""
        return f"{self.title}\n\n{self.body}"

    def add_tags(self, new_tags: list[str], replace: bool = False) -> None:
        """Add tags to the note."""
        if replace:
            self._frontmatter["tags"] = new_tags
        else:
            existing = set(self.tags)
            for tag in new_tags:
                if tag not in existing:
                    existing.add(tag)
            self._frontmatter["tags"] = sorted(existing)

    def add_backlinks(
        self,
        links: list[NoteLink],
        section_title: str = "Related Notes",
    ) -> None:
        """Append [[wiki links]] section to note body.
        
        Args:
            links: List of NoteLink objects to add
            section_title: Title of the backlinks section
        """
        if not links:
            return
        
        self._remove_section(section_title)
        
        lines = [f"\n\n## {section_title}\n"]
        for link in links:
            lines.append(f"- [[{link.to_title}]]\n")
        
        self._body = self._body.rstrip() + "".join(lines)

    def _remove_section(self, title: str) -> None:
        """Remove an existing section by title."""
        pattern = rf"\n*## {re.escape(title)}\n(?:- \[\[.*?\]\]\n)*"
        self._body = re.sub(pattern, "", self._body)

    def _build_content(self) -> str:
        """Build the full content with frontmatter."""
        if self._frontmatter:
            frontmatter_str = yaml.dump(
                self._frontmatter, 
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            ).strip()
            return f"---\n{frontmatter_str}\n---\n\n{self._body}"
        return self._body

    def save(self) -> None:
        """Save the note back to disk with updated frontmatter."""
        new_content = self._build_content()
        self.path.write_text(new_content, encoding="utf-8")
        self._content = new_content

    async def save_async(self) -> None:
        """Save the note back to disk with updated frontmatter asynchronously."""
        new_content = self._build_content()
        async with aiofiles.open(self.path, "w", encoding="utf-8") as f:
            await f.write(new_content)
        self._content = new_content

    @classmethod
    async def from_path_async(cls, path: Path) -> "ObsidianNote":
        """Create an ObsidianNote from a path asynchronously."""
        async with aiofiles.open(path, encoding="utf-8") as f:
            content = await f.read()
        note = object.__new__(cls)
        note.path = path
        note._content = content
        note._frontmatter = {}
        note._body = content
        note._parse()
        return note


def apply_tags_to_note(
    path: Path,
    tags: list[str],
    replace: bool = True,
) -> None:
    """Apply tags to a markdown note file in Obsidian style.
    
    Args:
        path: Path to the markdown file
        tags: List of tag names to apply
        replace: If True, replace existing tags; if False, merge with existing
    """
    note = ObsidianNote(path)
    note.add_tags(tags, replace=replace)
    note.save()


async def apply_tags_to_note_async(
    path: Path,
    tags: list[str],
    replace: bool = True,
) -> None:
    """Apply tags to a markdown note file in Obsidian style asynchronously.
    
    Args:
        path: Path to the markdown file
        tags: List of tag names to apply
        replace: If True, replace existing tags; if False, merge with existing
    """
    note = await ObsidianNote.from_path_async(path)
    note.add_tags(tags, replace=replace)
    await note.save_async()


def apply_backlinks_to_note(
    path: Path,
    links: list[NoteLink],
    section_title: str = "Related Notes",
) -> None:
    """Apply backlinks to a markdown note file.
    
    Args:
        path: Path to the markdown file
        links: List of NoteLink objects to add
        section_title: Title of the backlinks section
    """
    note = ObsidianNote(path)
    note.add_backlinks(links, section_title=section_title)
    note.save()


async def apply_backlinks_to_note_async(
    path: Path,
    links: list[NoteLink],
    section_title: str = "Related Notes",
) -> None:
    """Apply backlinks to a markdown note file asynchronously.
    
    Args:
        path: Path to the markdown file
        links: List of NoteLink objects to add
        section_title: Title of the backlinks section
    """
    note = await ObsidianNote.from_path_async(path)
    note.add_backlinks(links, section_title=section_title)
    await note.save_async()
