# Notes Tagger - Implementation Plan

## Overview

Implement an automated note tagging system using **sentence embeddings** (Sentence-BERT) with **cosine similarity** matching against topic descriptions. No training required, fully local, semantic understanding.

**Core Strategy**: Embed topics once → embed incoming notes → find closest topics via cosine similarity → apply threshold filtering.

---

## 🏗️ Project Architecture

```
notes_tagger/
├── notes_tagger/                 # Main library package
│   ├── __init__.py               # Public API exports
│   ├── models.py                 # Pydantic models (core types)
│   ├── config.py                 # Configuration (topics, thresholds, etc.)
│   ├── embeddings/
│   │   ├── __init__.py
│   │   ├── model.py              # EmbeddingModel class
│   │   ├── cache.py              # Caching logic
│   │   └── utils.py              # Normalization, batch ops
│   ├── tagger/
│   │   ├── __init__.py
│   │   ├── engine.py             # TaggingEngine class
│   │   └── scoring.py            # Similarity, ranking logic
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── formats.py            # JSON, YAML parsing
│   │   ├── obsidian.py           # Markdown + YAML frontmatter handling
│   │   └── cache.py              # Pickle serialization
│   └── exceptions.py             # Custom exceptions
│
├── notes_tagger_cli/             # CLI application (separate)
│   ├── __init__.py
│   ├── main.py                   # Entry point (Click app)
│   ├── commands.py               # CLI commands
│   └── utils.py                  # CLI-specific utilities
│
├── tests/
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_embeddings.py
│   │   ├── test_tagger.py
│   │   └── test_storage.py
│   ├── integration/
│   │   ├── test_end_to_end.py
│   │   ├── test_obsidian_sync.py
│   │   └── test_batch_processing.py
│   └── fixtures/
│       ├── sample_notes/          # Test markdown files
│       └── expected_output/
│
├── examples/
│   ├── basic_tagging.py          # Library usage example
│   ├── batch_tagging.py
│   └── obsidian_sync.py
│
├── cache/
│   ├── topic_embeddings.pkl      # Cached topic embeddings
│   └── .gitkeep
│
├── main.py                       # CLI entry script
├── pyproject.toml                # Dependencies
└── README.md
```

**Key Principle**: Users can import `notes_tagger` as a library without CLI dependencies. CLI is optional and thin.

---

## 📦 Dependencies

### Core Library (No CLI)
```toml
[tool.poetry.dependencies]
python = "^3.9"
sentence-transformers = "^2.2.0"    # Embeddings
numpy = "^1.24.0"                   # Numerical ops
pydantic = "^2.0"                   # Type safety, validation
pyyaml = "^6.0"                     # YAML frontmatter parsing
pathlib = "^1.0.1"                  # Path manipulation (stdlib)
```

### CLI (Optional, Development)
```toml
[tool.poetry.group.dev.dependencies]
click = "^8.1.0"                    # CLI framework
tqdm = "^4.65.0"                    # Progress bars
pytest = "^7.0"                     # Testing
pytest-cov = "^4.0"                 # Coverage
```

**Rationale**: Core library has **zero CLI dependencies**. Users can use it anywhere.

---

## 🔧 Core Library Modules

### 1. `models.py` - Pydantic Data Models

**Core types for type safety & validation across the library.**

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum

# Enums
class ModelType(str, Enum):
    MPNET = "all-mpnet-base-v2"
    MINILM = "all-MiniLM-L6-v2"

# Pydantic Models
class TagScore(BaseModel):
    """A topic tag with similarity score."""
    topic: str
    score: float = Field(..., ge=0.0, le=1.0)

class Note(BaseModel):
    """A single note to be tagged."""
    id: str
    title: str
    body: str
    tags: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "note_001",
                "title": "Q3 Budget",
                "body": "Reviewed budget...",
            }
        }

class TagResult(BaseModel):
    """Tagging result for a single note."""
    note_id: str
    note_title: str
    tags: List[TagScore]
    
    def sort_by_score(self) -> "TagResult":
        """Return copy sorted by score descending."""
        sorted_tags = sorted(self.tags, key=lambda t: t.score, reverse=True)
        return TagResult(note_id=self.note_id, note_title=self.note_title, tags=sorted_tags)

class Config(BaseModel):
    """Configuration for tagging engine."""
    topics: dict[str, str] = Field(
        ..., 
        description="Topic name -> semantic description mapping"
    )
    threshold: float = Field(default=0.35, ge=0.0, le=1.0)
    max_tags: int = Field(default=3, ge=1)
    model_name: ModelType = ModelType.MPNET
    cache_dir: str = Field(default="./cache")
    device: Optional[str] = None  # Auto-detect if None
    
    @validator('topics')
    def topics_not_empty(cls, v):
        if not v:
            raise ValueError("Must define at least one topic")
        return v

class EmbeddingMetadata(BaseModel):
    """Metadata for cached embeddings."""
    model_name: str
    num_topics: int
    topics: List[str]
    embedding_dim: int
    timestamp: float
```

---

### 2. `config.py` - Default Configuration

**Provides sensible defaults that users can override.**

```python
from pathlib import Path
from notes_tagger.models import Config, ModelType

DEFAULT_CONFIG = Config(
    topics={
        "finance": "money, budgeting, accounting, revenue, expenses, forecasts, costs",
        "meeting": "meetings, discussions, agendas, decisions, action items, notes, attendees",
        "ideas": "new ideas, brainstorming, proposals, creative thoughts, innovation",
        "research": "investigation, reading papers, experiments, analysis, learning",
        "planning": "roadmaps, future plans, scheduling, prioritization, milestones",
    },
    threshold=0.35,
    max_tags=3,
    model_name=ModelType.MPNET,
    cache_dir=str(Path(__file__).parent.parent / "cache"),
    device=None,
)

def load_config(path: Optional[str] = None) -> Config:
    """Load config from JSON file or use defaults."""
    if path is None:
        return DEFAULT_CONFIG
    # ... load from file, validate with Pydantic
```

### 3. `embeddings/model.py` - Model Management & Embedding

**Handles sentence transformer loading and inference.**

```python
from sentence_transformers import SentenceTransformer
from numpy import ndarray
from pathlib import Path
from notes_tagger.models import ModelType, EmbeddingMetadata

class EmbeddingModel:
    """Wrapper around SentenceTransformer for consistent interface."""
    
    def __init__(self, model_name: ModelType | str, device: Optional[str] = None):
        self.model_name = str(model_name)
        self.device = device or self._auto_detect_device()
        self.model = SentenceTransformer(self.model_name, device=self.device)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
    
    def embed(self, text: str) -> ndarray:
        """Single text → embedding."""
        return self.model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
    
    def embed_batch(self, texts: list[str], batch_size: int = 32) -> ndarray:
        """Batch encode with automatic normalization."""
        return self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )
    
    def _auto_detect_device(self) -> str:
        """Detect GPU availability."""
        try:
            import torch
            return "cuda" if torch.cuda.is_available() else "cpu"
        except:
            return "cpu"

Key exports:
  - EmbeddingModel: class with embed(), embed_batch()
```

---

### 4. `embeddings/cache.py` - Embedding Caching

**Save/load topic embeddings with metadata for validation.**

```python
from pathlib import Path
from pickle import dump, load
from notes_tagger.models import EmbeddingMetadata
from numpy import ndarray
from time import time

class EmbeddingCache:
    """Persistent storage for embeddings."""
    
    def save(self, embeddings: ndarray, topics: list[str], 
             model_name: str, cache_dir: Path) -> Path:
        """Save embeddings + metadata."""
        cache_path = cache_dir / "topic_embeddings.pkl"
        metadata = EmbeddingMetadata(
            model_name=model_name,
            num_topics=len(topics),
            topics=topics,
            embedding_dim=embeddings.shape[1],
            timestamp=time(),
        )
        # Save with pickle: (embeddings, metadata)
        cache_path.parent.mkdir(exist_ok=True)
        with open(cache_path, 'wb') as f:
            dump((embeddings, metadata), f)
        return cache_path
    
    def load(self, cache_path: Path) -> tuple[ndarray, EmbeddingMetadata] | None:
        """Load embeddings + metadata, or None if invalid."""
        if not cache_path.exists():
            return None
        try:
            with open(cache_path, 'rb') as f:
                return load(f)
        except:
            return None
    
    def is_valid(self, metadata: EmbeddingMetadata, topics: list[str], 
                 model_name: str) -> bool:
        """Check if cached embeddings match current config."""
        return (
            metadata.model_name == model_name and
            metadata.topics == topics
        )
```

---

### 5. `tagger/engine.py` - Core Tagging Engine

**Main API for tagging notes.**

```python
from numpy import ndarray, dot
from notes_tagger.models import Config, Note, TagResult, TagScore
from notes_tagger.embeddings.model import EmbeddingModel
from notes_tagger.embeddings.cache import EmbeddingCache

class TaggingEngine:
    """Main interface for tagging notes."""
    
    def __init__(self, config: Config):
        self.config = config
        self.embedding_model = EmbeddingModel(config.model_name, config.device)
        self.cache = EmbeddingCache()
        self.topic_embeddings: ndarray = None
        self.topic_names: list[str] = None
    
    def initialize(self) -> None:
        """Load/create topic embeddings."""
        cache_path = Path(self.config.cache_dir) / "topic_embeddings.pkl"
        
        # Try load from cache
        cached = self.cache.load(cache_path)
        if cached is not None:
            embeddings, metadata = cached
            if self.cache.is_valid(metadata, list(self.config.topics.keys()), 
                                    str(self.config.model_name)):
                self.topic_embeddings = embeddings
                self.topic_names = list(self.config.topics.keys())
                return
        
        # Generate new embeddings
        self.topic_names = list(self.config.topics.keys())
        topic_texts = list(self.config.topics.values())
        self.topic_embeddings = self.embedding_model.embed_batch(topic_texts)
        
        # Save to cache
        self.cache.save(
            self.topic_embeddings,
            self.topic_names,
            str(self.config.model_name),
            Path(self.config.cache_dir)
        )
    
    def tag(self, text: str) -> TagResult:
        """Tag a single note."""
        if self.topic_embeddings is None:
            self.initialize()
        
        note_emb = self.embedding_model.embed(text)
        scores = dot(self.topic_embeddings, note_emb)
        
        tags = [
            TagScore(topic=t, score=float(s))
            for t, s in zip(self.topic_names, scores)
            if s >= self.config.threshold
        ]
        tags.sort(key=lambda x: x.score, reverse=True)
        
        return TagResult(
            note_id="",
            note_title="",
            tags=tags[:self.config.max_tags]
        )
    
    def tag_batch(self, texts: list[str]) -> list[TagResult]:
        """Tag multiple notes efficiently."""
        if self.topic_embeddings is None:
            self.initialize()
        
        embeddings = self.embedding_model.embed_batch(texts)
        results = []
        for text, emb in zip(texts, embeddings):
            scores = dot(self.topic_embeddings, emb)
            tags = [
                TagScore(topic=t, score=float(s))
                for t, s in zip(self.topic_names, scores)
                if s >= self.config.threshold
            ]
            tags.sort(key=lambda x: x.score, reverse=True)
            results.append(TagResult(
                note_id="",
                note_title="",
                tags=tags[:self.config.max_tags]
            ))
        return results
```

---

### 6. `storage/obsidian.py` - Obsidian Markdown Handling

**Parse and update YAML frontmatter in markdown files.**

```python
from pathlib import Path
from yaml import safe_load, safe_dump
from notes_tagger.models import TagScore
from typing import Optional

class ObsidianNote:
    """Parse and manipulate Obsidian markdown notes."""
    
    def __init__(self, file_path: Path):
        self.path = file_path
        self.content = file_path.read_text(encoding='utf-8')
        self.frontmatter: dict = {}
        self.body: str = ""
        self._parse()
    
    def _parse(self) -> None:
        """Extract YAML frontmatter and body."""
        if self.content.startswith("---"):
            parts = self.content.split("---", 2)
            if len(parts) >= 3:
                try:
                    self.frontmatter = safe_load(parts[1]) or {}
                    self.body = parts[2].lstrip()
                except:
                    self.body = self.content
            else:
                self.body = self.content
        else:
            self.body = self.content
    
    def get_combined_text(self) -> str:
        """Return title + body for tagging."""
        title = self.frontmatter.get('title', self.path.stem)
        return f"{title}. {self.body[:500]}"  # First 500 chars
    
    def add_tags(self, new_tags: list[TagScore], replace: bool = False) -> None:
        """Add or replace tags in frontmatter."""
        if self.frontmatter is None:
            self.frontmatter = {}
        
        tag_names = [t.topic for t in new_tags]
        
        if replace:
            self.frontmatter['tags'] = tag_names
        else:
            existing = self.frontmatter.get('tags', [])
            if isinstance(existing, str):
                existing = [existing]
            combined = list(set(existing) | set(tag_names))
            self.frontmatter['tags'] = combined
    
    def save(self) -> None:
        """Write frontmatter + body back to file."""
        if self.frontmatter:
            yaml_str = safe_dump(self.frontmatter, default_flow_style=False)
            new_content = f"---\n{yaml_str}---\n{self.body}"
        else:
            new_content = self.body
        
        self.path.write_text(new_content, encoding='utf-8')

class ObsidianVault:
    """Walk through Obsidian vault and batch tag notes."""
    
    def __init__(self, vault_dir: Path):
        self.vault_dir = Path(vault_dir)
    
    def get_notes(self, pattern: str = "**/*.md") -> list[Path]:
        """Find all markdown files."""
        return list(self.vault_dir.glob(pattern))
    
    def process_vault(self, tag_func, output_stats: bool = True):
        """Apply tagging function to all notes."""
        notes = self.get_notes()
        for note_path in notes:
            obsidian_note = ObsidianNote(note_path)
            text = obsidian_note.get_combined_text()
            tags = tag_func(text)
            obsidian_note.add_tags(tags)
            obsidian_note.save()
```

---

### 7. `storage/formats.py` - Data Format Loading

**Load notes from various formats.**

```python
import json
from pathlib import Path
from notes_tagger.models import Note

def load_json_notes(path: Path) -> list[Note]:
    """Load notes from JSON."""
    with open(path) as f:
        data = json.load(f)
    return [Note(**n) for n in data]

def save_json_notes(notes: list[Note], path: Path) -> None:
    """Save notes to JSON."""
    with open(path, 'w') as f:
        json.dump([n.dict() for n in notes], f, indent=2)
```

---

### 8. `__init__.py` - Public Library API

**Users import from here.**

```python
from notes_tagger.models import Config, Note, TagResult, TagScore, ModelType
from notes_tagger.config import DEFAULT_CONFIG, load_config
from notes_tagger.tagger.engine import TaggingEngine
from notes_tagger.storage.obsidian import ObsidianNote, ObsidianVault
from notes_tagger.storage.formats import load_json_notes, save_json_notes

__all__ = [
    'Config',
    'Note',
    'TagResult',
    'TagScore',
    'ModelType',
    'DEFAULT_CONFIG',
    'load_config',
    'TaggingEngine',
    'ObsidianNote',
    'ObsidianVault',
    'load_json_notes',
    'save_json_notes',
]
```

---

## 🔌 CLI Module (`notes_tagger_cli/`)

### `notes_tagger_cli/main.py` - Click CLI Entry

```python
import click
from pathlib import Path
from notes_tagger import TaggingEngine, DEFAULT_CONFIG, ObsidianVault
from notes_tagger_cli.commands import tag_vault, tag_file, calibrate

@click.group()
def cli():
    """Notes Tagger - Semantic note tagging with Sentence-BERT."""
    pass

@cli.command()
@click.argument('vault_path', type=click.Path(exists=True))
@click.option('--threshold', type=float, default=None, help='Override default threshold')
@click.option('--model', type=click.Choice(['mpnet', 'minilm']), default='mpnet')
@click.option('--dry-run', is_flag=True, help='Show changes without writing')
def vault(vault_path: str, threshold: float, model: str, dry_run: bool):
    """Tag all markdown notes in an Obsidian vault."""
    tag_vault(Path(vault_path), threshold=threshold, model_choice=model, dry_run=dry_run)

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', type=click.Path(), default=None, help='Save as JSON')
@click.option('--show-scores', is_flag=True, help='Display similarity scores')
def file(file_path: str, output: str, show_scores: bool):
    """Tag a single file (JSON or Markdown)."""
    tag_file(Path(file_path), output_path=Path(output) if output else None, show_scores=show_scores)

@cli.command()
@click.option('--sample-size', type=int, default=20, help='Number of notes to calibrate on')
@click.argument('vault_path', type=click.Path(exists=True))
def calibrate_cmd(sample_size: int, vault_path: str):
    """Interactively tune threshold on sample notes."""
    calibrate(Path(vault_path), sample_size=sample_size)

if __name__ == '__main__':
    cli()
```

### `notes_tagger_cli/commands.py` - CLI Command Implementations

```python
from pathlib import Path
from tqdm import tqdm
from notes_tagger import TaggingEngine, DEFAULT_CONFIG, ObsidianVault, ModelType
import click

def tag_vault(vault_path: Path, threshold: float = None, model_choice: str = 'mpnet', 
              dry_run: bool = False):
    """Tag all markdown files in vault."""
    model_map = {
        'mpnet': ModelType.MPNET,
        'minilm': ModelType.MINILM,
    }
    
    config = DEFAULT_CONFIG.copy(update={
        'threshold': threshold or DEFAULT_CONFIG.threshold,
        'model_name': model_map[model_choice],
    })
    
    engine = TaggingEngine(config)
    engine.initialize()
    
    vault = ObsidianVault(vault_path)
    notes = vault.get_notes()
    
    click.echo(f"Found {len(notes)} markdown files")
    
    def tag_func(text: str):
        result = engine.tag(text)
        return result.tags
    
    for note_path in tqdm(notes, desc="Tagging"):
        from notes_tagger import ObsidianNote
        note = ObsidianNote(note_path)
        text = note.get_combined_text()
        tags = tag_func(text)
        
        if not dry_run:
            note.add_tags(tags, replace=False)
            note.save()
        else:
            click.echo(f"\n{note_path.name}: {[t.topic for t in tags]}")

def tag_file(file_path: Path, output_path: Path = None, show_scores: bool = False):
    """Tag single note file."""
    engine = TaggingEngine(DEFAULT_CONFIG)
    engine.initialize()
    
    if file_path.suffix == '.md':
        from notes_tagger import ObsidianNote
        note = ObsidianNote(file_path)
        text = note.get_combined_text()
    else:
        text = file_path.read_text()
    
    result = engine.tag(text)
    
    for tag in result.tags:
        if show_scores:
            click.echo(f"{tag.topic}: {tag.score:.3f}")
        else:
            click.echo(tag.topic)

def calibrate(vault_path: Path, sample_size: int = 20):
    """Interactive threshold calibration."""
    # ... implementation for user feedback loop
    pass
```

---

## 🚀 Implementation Roadmap

### Phase 1: Core Models & Config (Priority 1)
- [ ] `notes_tagger/models.py` - Define all Pydantic models
- [ ] `notes_tagger/config.py` - Default config + loader
- [ ] `notes_tagger/exceptions.py` - Custom exceptions
- [ ] Update `pyproject.toml` with dependencies

**Checkpoint**: Can import `from notes_tagger import Config, TagScore`, validate data.

---

### Phase 2: Core Engine (Priority 2)
- [ ] `notes_tagger/embeddings/model.py` - EmbeddingModel wrapper
- [ ] `notes_tagger/embeddings/cache.py` - Caching logic
- [ ] `notes_tagger/tagger/engine.py` - TaggingEngine class
- [ ] Basic tests for tagging

**Checkpoint**: Can tag a text string and get scores back.

---

### Phase 3: Storage & Obsidian (Priority 3)
- [ ] `notes_tagger/storage/obsidian.py` - Parse/write markdown + YAML
- [ ] `notes_tagger/storage/formats.py` - JSON loading
- [ ] Test with sample Obsidian vault
- [ ] Create fixture files

**Checkpoint**: Can load markdown, tag it, update YAML frontmatter, save.

---

### Phase 4: Public Library API (Priority 4)
- [ ] `notes_tagger/__init__.py` - Export public API
- [ ] Add docstrings to all modules
- [ ] Create `examples/basic_tagging.py` example
- [ ] Create `examples/obsidian_sync.py` example

**Checkpoint**: Users can `from notes_tagger import TaggingEngine, ObsidianVault` and use library.

---

### Phase 5: CLI Layer (Priority 5)
- [ ] `notes_tagger_cli/main.py` - Click CLI structure
- [ ] `notes_tagger_cli/commands.py` - Implement commands
- [ ] Add `vault`, `file`, `calibrate` commands
- [ ] Test end-to-end

**Checkpoint**: `python main.py vault /path/to/obsidian --threshold 0.35`

---

### Phase 6: Testing & Polish (Priority 6)
- [ ] Unit tests for all library modules
- [ ] Integration tests for Obsidian workflow
- [ ] Add progress bars + logging
- [ ] Create comprehensive `README.md`

**Checkpoint**: All tests pass, ready for real usage.

---

## 🧠 Implementation Details

### Topic Definitions (config.py)

Start with 5–10 topics. Each has a **semantic description** (not just a label).

**Example**:
```python
TOPICS = {
    "finance": "money, budgeting, accounting, revenue, expenses, forecasts, costs",
    "meeting": "meetings, discussions, agendas, decisions, action items, notes, attendees",
    "ideas": "new ideas, brainstorming, proposals, creative thoughts, innovation, concepts",
    "research": "investigation, reading papers, experiments, analysis, learning, study",
    "planning": "roadmaps, future plans, scheduling, prioritization, milestones, timeline",
}
```

**Do not** use vague descriptions. Descriptions should capture the semantic space.

---

### Embedding & Caching Strategy

1. **First Run**:
   - Load model (download ~400MB for mpnet, ~100MB for minilm)
   - Embed topics once
   - Cache embeddings to `cache/topic_embeddings.pkl`

2. **Subsequent Runs**:
   - Load cached topic embeddings
   - Only embed incoming notes (fast)

3. **Cache Invalidation**:
   - If topics change → rebuild cache
   - If model changes → rebuild cache
   - Cache version in metadata for safety

---

### Similarity Matching (tagger.py)

```python
# Pseudocode
def tag(note_text):
    note_emb = model.embed(note_text)  # Shape: (384,) or (768,)
    
    scores = dot(topic_embeddings, note_emb)  # Cosine similarity
    # topic_embeddings: (num_topics, embedding_dim)
    # Result: scores shape (num_topics,)
    
    ranked = sorted(zip(topics, scores), key=lambda x: x[1], reverse=True)
    
    return [
        {"topic": t, "score": float(s)}
        for t, s in ranked[:max_tags]
        if s >= threshold
    ]
```

**Key**: Use **normalized embeddings** so dot product = cosine similarity.

---

### Threshold Tuning Workflow

1. Start with `threshold = 0.35`
2. Tag ~100 sample notes
3. Review false positives / false negatives
4. Adjust threshold:
   - Too many false positives → increase to 0.40–0.45
   - Too many false negatives → decrease to 0.30–0.35
5. Lock in final threshold

**Interactive calibration** (optional):
```bash
python main.py calibrate --sample 50
# Shows notes + current tags, asks user to confirm
# Suggests optimal threshold based on feedback
```

---

### Batch Processing

For large note sets (1000+):
```python
def tag_batch(notes: list[str], batch_size=32):
    results = []
    for i in tqdm(range(0, len(notes), batch_size)):
        batch = notes[i:i+batch_size]
        batch_embs = model.embed_batch(batch)
        for emb in batch_embs:
            results.append(tag_with_embedding(emb))
    return results
```

Sentence-transformers supports batching natively. Use batch_size=32–64.

---

## 🧪 Testing Strategy

### Unit Tests (test_tagger.py)
- [ ] Tag returns correct format
- [ ] Scores are between 0–1
- [ ] Threshold filtering works
- [ ] Max tags respected

### Unit Tests (test_embeddings.py)
- [ ] Model loads correctly
- [ ] Embeddings have expected shape
- [ ] Normalized embeddings sum to 1
- [ ] Cache save/load works

### Integration Tests (test_integration.py)
- [ ] Tag a sample note with known topics
- [ ] Batch tagging matches single tagging
- [ ] Results are deterministic
- [ ] End-to-end CLI works

---

## 📊 Performance Targets

| Task | Target | Model |
|------|--------|-------|
| Load model + embed topics | < 5s | mpnet or minilm |
| Tag 1 note | < 100ms | After topics cached |
| Tag 1000 notes | < 30s | Batch size 32–64 |
| Memory footprint | < 2GB | Entire system |

---

## 🎯 Model Selection Decision Tree

```
Q: Do you need maximum semantic quality?
  → YES: Use "all-mpnet-base-v2" (best)
  → NO: Use "all-MiniLM-L6-v2" (fast, 95% quality)

Q: Do you have GPU?
  → YES: Either model, fast
  → NO: MiniLM recommended

Q: Note volume > 10k notes?
  → YES: Use MiniLM or batch process mpnet
  → NO: mpnet is fine
```

**Default**: `all-mpnet-base-v2` (start here, switch if too slow)

---

## 📝 Input/Output Formats

### Input: Obsidian Markdown (Primary Use Case)

**Before tagging:**
```markdown
# Q3 Budget Review

Reviewed quarterly budget, updated revenue forecast by +5%.
Discussed with finance team on Jan 20.
```

**After tagging:**
```markdown
---
title: Q3 Budget Review
tags:
  - finance
  - planning
---

Reviewed quarterly budget, updated revenue forecast by +5%.
Discussed with finance team on Jan 20.
```

The system:
1. Parses YAML frontmatter (or creates it)
2. Extracts title + body for embedding
3. Tags based on semantic similarity
4. Appends tags to existing frontmatter list (no duplicates)
5. Writes back to file

---

### Input: JSON Notes (Alternative)

```json
[
  {
    "id": "note_001",
    "title": "Q3 Budget Review",
    "body": "Reviewed quarterly budget, updated revenue forecast by +5%",
  },
  ...
]
```

---

### Output: JSON Results

```json
[
  {
    "note_id": "note_001",
    "note_title": "Q3 Budget Review",
    "tags": [
      {"topic": "finance", "score": 0.68},
      {"topic": "planning", "score": 0.42}
    ]
  },
  ...
]
```

---

## 📚 Library Usage Examples

### Example 1: Basic Tagging (Library Only)

```python
from notes_tagger import TaggingEngine, DEFAULT_CONFIG

# Use defaults or customize
config = DEFAULT_CONFIG.copy(update={
    "threshold": 0.40,
})

engine = TaggingEngine(config)
engine.initialize()  # Load model + cache topics

result = engine.tag("Reviewed quarterly budget and revenue forecast")
for tag in result.tags:
    print(f"{tag.topic}: {tag.score:.3f}")

# Output:
# finance: 0.68
# planning: 0.42
```

---

### Example 2: Tag Obsidian Vault (Library Only)

```python
from pathlib import Path
from notes_tagger import TaggingEngine, ObsidianVault, DEFAULT_CONFIG

vault = ObsidianVault(Path("~/Obsidian Vault"))
engine = TaggingEngine(DEFAULT_CONFIG)
engine.initialize()

for note_path in vault.get_notes():
    note = ObsidianNote(note_path)
    text = note.get_combined_text()
    tags = engine.tag(text).tags
    
    note.add_tags(tags, replace=False)  # Append, don't overwrite
    note.save()
```

---

### Example 3: Custom Config + Batch Processing

```python
from notes_tagger import Config, TaggingEngine, ModelType

config = Config(
    topics={
        "backend": "databases, APIs, servers, microservices, queries, caching",
        "frontend": "UI, CSS, React, Vue, components, styling, UX",
        "devops": "docker, kubernetes, CI/CD, deployment, monitoring, logs",
    },
    threshold=0.4,
    max_tags=2,
    model_name=ModelType.MINILM,  # Faster on CPU
)

engine = TaggingEngine(config)
engine.initialize()

texts = [
    "Built REST API with FastAPI",
    "Fixed CSS grid layout bug",
    "Set up Docker containers",
]

results = engine.tag_batch(texts)
for result in results:
    print([t.topic for t in result.tags])
```

---

## 🔄 Optional Enhancements (Post-MVP)

- [ ] **Multi-language support**: Use multilingual model variant
- [ ] **Confidence calibration**: Train a simple threshold optimizer
- [ ] **Topic refinement**: Suggest better descriptions based on mislabeled notes
- [ ] **Web UI**: Flask/FastAPI app for tagging on demand
- [ ] **Batch retraining**: Periodically update topic embeddings
- [ ] **Vault backup**: Auto-backup before bulk tagging
- [ ] **Hook integration**: Integration with note creation workflows

---

## 🚦 Next Steps

1. **Read this plan** → understand library/CLI separation
2. **Implement Phase 1** → models + config (easy, no dependencies)
3. **Implement Phase 2** → embeddings + tagging engine (core logic)
4. **Test with 10 notes** → validate threshold
5. **Implement Phase 3** → Obsidian integration (YAML handling)
6. **Implement Phase 4** → Public API (clean exports)
7. **Test library in isolation** → ensure zero CLI dependencies
8. **Implement Phase 5** → CLI (thin wrapper around library)
9. **Run on 100 notes** → calibrate threshold + descriptions
10. **Deploy** → integrate with Obsidian vault

---

## 💡 Key Design Principles

1. **Library First**: `notes_tagger` can be used without CLI dependencies
2. **Type Safety**: All data validated via Pydantic
3. **Testability**: Each module independently testable
4. **Obsidian Native**: Direct YAML frontmatter support
5. **No Training**: Use pre-trained embeddings, not ML training
6. **Cacheable**: Embeddings cached, fast iteration
7. **Threshold Tuning**: Easy to adjust via config or CLI flag

---

## 🔗 Integration Points

| Component | Can be used independently? | Dependencies |
|-----------|---------------------------|-----|
| `notes_tagger` (library) | ✅ Yes | sentence-transformers, pydantic, numpy, pyyaml |
| `notes_tagger_cli` (CLI) | ❌ No | Requires `notes_tagger` + click, tqdm |
| `TaggingEngine` | ✅ Yes | Core library only |
| `ObsidianVault` | ✅ Yes | Core library only |
| `EmbeddingModel` | ✅ Yes | sentence-transformers, numpy |

**Result**: Users can `pip install notes_tagger` and use just the library. CLI is optional.

---

## 📚 References

- [Sentence-Transformers Docs](https://sbert.net/)
- [Pre-trained Model Cards](https://huggingface.co/models?library=sentence-transformers)
- [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity)
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) (compare models)
