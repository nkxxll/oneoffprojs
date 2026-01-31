# Notes Tagger

Semantic note tagging using sentence embeddings. Automatically tag your markdown notes based on content similarity to predefined topics.

## Installation

```bash
uv sync
```

## CLI Usage

### Tag Notes

Tag all markdown files in a directory:

```bash
notes-tagger tag ./notes
```

Tag a single file:

```bash
notes-tagger tag note.md
```

### Options

| Option | Description |
|--------|-------------|
| `-c, --config PATH` | Path to config file (JSON/YAML) |
| `-t, --threshold FLOAT` | Minimum similarity threshold (0.0-1.0) |
| `-m, --max-tags INT` | Maximum number of tags per note |
| `-r, --recursive` | Recursively search directories (default: on) |
| `--dry-run` | Show what would be tagged without writing |
| `-v, --verbose` | Show detailed output with scores |
| `--replace` | Replace existing tags instead of appending |

### Examples

Preview tagging without modifying files:

```bash
notes-tagger tag ./notes --dry-run --verbose
```

Adjust threshold and max tags:

```bash
notes-tagger tag ./notes --threshold 0.4 --max-tags 2
```

Replace existing tags instead of appending:

```bash
notes-tagger tag ./notes --replace
```

### List Topics

Show available topics from the default configuration:

```bash
notes-tagger topics
```

## Library Usage

```python
from notes_tagger import TaggingEngine, DEFAULT_CONFIG

engine = TaggingEngine(DEFAULT_CONFIG)
engine.initialize()

result = engine.tag("Reviewed quarterly budget and revenue forecast")
for tag in result.tags:
    print(f"{tag.topic}: {tag.score:.3f}")
```
