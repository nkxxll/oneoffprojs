"""JSON and YAML parsing utilities for notes."""

import json
from pathlib import Path
from typing import Any

import yaml

from notes_tagger.models import Note, TagResult


def load_notes_from_json(path: Path | str) -> list[Note]:
    """Load notes from a JSON file."""
    path = Path(path)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    
    if isinstance(data, list):
        return [Note(**item) for item in data]
    raise ValueError("JSON file must contain a list of notes")


def save_notes_to_json(notes: list[Note], path: Path | str) -> None:
    """Save notes to a JSON file."""
    path = Path(path)
    data = [note.model_dump() for note in notes]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_notes_from_yaml(path: Path | str) -> list[Note]:
    """Load notes from a YAML file."""
    path = Path(path)
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    if isinstance(data, list):
        return [Note(**item) for item in data]
    raise ValueError("YAML file must contain a list of notes")


def save_notes_to_yaml(notes: list[Note], path: Path | str) -> None:
    """Save notes to a YAML file."""
    path = Path(path)
    data = [note.model_dump() for note in notes]
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


def save_results_to_json(results: list[TagResult], path: Path | str) -> None:
    """Save tagging results to a JSON file."""
    path = Path(path)
    data = [result.model_dump() for result in results]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_config_from_yaml(path: Path | str) -> dict[str, Any]:
    """Load configuration from a YAML file."""
    path = Path(path)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_config_from_json(path: Path | str) -> dict[str, Any]:
    """Load configuration from a JSON file."""
    path = Path(path)
    with open(path, encoding="utf-8") as f:
        return json.load(f)
