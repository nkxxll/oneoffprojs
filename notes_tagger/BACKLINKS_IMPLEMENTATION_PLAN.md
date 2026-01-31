# Note-to-Note Backlinks - Implementation Plan

## Goal

Find semantically similar notes and insert Obsidian `[[wiki links]]` into each note's body or frontmatter.

---

## Architecture

```
notes_tagger/
├── linker/                      # NEW module
│   ├── __init__.py
│   ├── engine.py                # LinkingEngine class
│   ├── similarity.py            # Note similarity scoring
│   └── policy.py                # Link constraints (threshold, max links, etc.)
```

---

## Phase 1: Core Data Models

Add to `models.py`:

```python
class NoteLink(BaseModel):
    """A link between two notes with similarity score."""
    from_id: str
    to_id: str
    to_title: str           # For generating [[title]]
    similarity: float
    shared_tags: list[str] = []

class LinkResult(BaseModel):
    """Linking result for a single note."""
    note_id: str
    links: list[NoteLink]
```

---

## Phase 2: LinkingEngine

**`linker/engine.py`** - reuses existing `EmbeddingModel`:

1. **Embed all notes** once (batch) → store in memory/cache
2. **Build similarity matrix** (N×N dot product of normalized embeddings)
3. **For each note**: find top-K neighbors above threshold
4. **Apply constraints**: shared tags, temporal, max links

```python
class LinkingEngine:
    def __init__(self, config: LinkConfig):
        self.config = config
        self._model: EmbeddingModel = None
        self._note_embeddings: ndarray = None
        self._notes: list[Note] = []
    
    def initialize(self) -> None:
        """Load embedding model."""
        self._model = EmbeddingModel(self.config.model_name, self.config.device)
    
    def embed_notes(self, notes: list[Note]) -> None:
        """Embed all notes and store for similarity search."""
        self._notes = notes
        texts = [f"{n.title}\n\n{n.body}" for n in notes]
        self._note_embeddings = self._model.embed_batch(texts)
    
    def find_similar(self, note_idx: int) -> list[NoteLink]:
        """Find top-K similar notes for a given note."""
        query = self._note_embeddings[note_idx]
        scores = self._note_embeddings @ query  # dot product (normalized = cosine)
        
        # Rank and filter
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        
        links = []
        for idx, score in ranked:
            if idx == note_idx:
                continue
            if score < self.config.threshold:
                break
            if len(links) >= self.config.max_links:
                break
            
            links.append(NoteLink(
                from_id=self._notes[note_idx].id,
                to_id=self._notes[idx].id,
                to_title=self._notes[idx].title,
                similarity=float(score),
            ))
        
        return links
    
    def link_all(self) -> list[LinkResult]:
        """Find similar notes for all notes."""
        results = []
        for i in range(len(self._notes)):
            links = self.find_similar(i)
            results.append(LinkResult(note_id=self._notes[i].id, links=links))
        return results
```

---

## Phase 3: Link Policy Configuration

**`linker/policy.py`** - configurable rules:

```python
class LinkConfig(BaseModel):
    """Configuration for note linking."""
    threshold: float = Field(default=0.45, ge=0.0, le=1.0)
    max_links: int = Field(default=5, ge=1)
    require_shared_tag: bool = False
    model_name: ModelType = ModelType.MPNET
    device: Optional[str] = None
```

| Setting | Default | Description |
|---------|---------|-------------|
| `threshold` | 0.45 | Min similarity to create link |
| `max_links` | 5 | Max outgoing links per note |
| `require_shared_tag` | False | Only link if notes share a tag |

### Similarity Thresholds Reference

| Similarity | Meaning |
|------------|---------|
| `0.80+` | Near duplicate |
| `0.65–0.80` | Very related |
| `0.45–0.65` | Same topic |
| `0.30–0.45` | Weakly related |
| `<0.30` | Noise |

---

## Phase 4: Obsidian Integration

Extend `storage/obsidian.py`:

```python
class ObsidianNote:
    def add_backlinks(
        self, 
        links: list[NoteLink], 
        section_title: str = "Related Notes"
    ) -> None:
        """Append [[wiki links]] section to note body."""
        if not links:
            return
        
        # Remove existing section if present
        self._remove_section(section_title)
        
        # Build new section
        lines = [f"\n\n## {section_title}\n"]
        for link in links:
            lines.append(f"- [[{link.to_title}]]\n")
        
        self._body = self._body.rstrip() + "".join(lines)
    
    def _remove_section(self, title: str) -> None:
        """Remove an existing section by title."""
        pattern = rf"\n*## {re.escape(title)}\n(?:- \[\[.*?\]\]\n)*"
        self._body = re.sub(pattern, "", self._body)
```

### Output Format

```markdown
---
title: My Note
tags:
  - finance
---

Note content here...

## Related Notes
- [[Budget Planning 2024]]
- [[Q3 Financial Review]]
- [[Revenue Forecast]]
```

---

## Phase 5: CLI Command

Add `link` command:

```bash
# Preview links (dry run)
notes-tagger link ./vault --dry-run

# Apply links with custom settings
notes-tagger link ./vault --threshold 0.5 --max-links 3

# Only link notes that share tags
notes-tagger link ./vault --require-shared-tag
```

**CLI implementation** in `notes_tagger_cli/commands.py`:

```python
@cli.command()
@click.argument("vault_path", type=click.Path(exists=True))
@click.option("--threshold", default=0.45, help="Minimum similarity")
@click.option("--max-links", default=5, help="Max links per note")
@click.option("--require-shared-tag", is_flag=True)
@click.option("--dry-run", is_flag=True, help="Preview without writing")
def link(vault_path, threshold, max_links, require_shared_tag, dry_run):
    """Add [[wiki links]] to similar notes."""
    ...
```

---

## Phase 6: Scaling (Future)

| Note Count | Approach |
|------------|----------|
| <1k | NumPy dot product |
| 1k–10k | FAISS IndexFlatIP |
| 10k+ | FAISS IVF/HNSW |

FAISS integration (optional):

```python
import faiss

index = faiss.IndexFlatIP(embedding_dim)
index.add(embeddings)
distances, indices = index.search(query, k=max_links)
```

---

## File Structure

```
notes_tagger/
├── linker/
│   ├── __init__.py          # Exports: LinkingEngine, LinkConfig, NoteLink, LinkResult
│   ├── engine.py            # LinkingEngine class
│   ├── similarity.py        # build_similarity_matrix(), find_neighbors()
│   └── config.py            # LinkConfig model
├── models.py                # Add NoteLink, LinkResult
├── storage/
│   └── obsidian.py          # Add add_backlinks() method
```

---

## Implementation Order

1. [ ] Add `NoteLink` and `LinkResult` models to `models.py`
2. [ ] Create `linker/config.py` with `LinkConfig`
3. [ ] Create `linker/similarity.py` with matrix operations
4. [ ] Create `linker/engine.py` with `LinkingEngine`
5. [ ] Add `add_backlinks()` to `ObsidianNote`
6. [ ] Add `link` CLI command
7. [ ] Write tests
8. [ ] Test on real vault

---

## Design Decisions

### 1. Where to insert links?

**Decision**: Append `## Related Notes` section with `[[links]]`

Rationale:
- Visible in note preview
- Standard Obsidian wiki link format
- Easy to update/regenerate
- Doesn't pollute frontmatter

### 2. Link by filename or title?

**Decision**: Use note **title** (stem of filename)

Rationale:
- Obsidian resolves `[[title]]` to the matching file
- More readable than full paths
- Works with Obsidian's linking system

### 3. Regeneration behavior?

**Decision**: Remove and regenerate existing `## Related Notes` section

Rationale:
- Idempotent operation
- Links stay up-to-date as vault grows
- User can manually add links elsewhere (won't be touched)
