"""Batch tagging example using the notes_tagger library."""

from notes_tagger import TaggingEngine, DEFAULT_CONFIG
from notes_tagger.models import ModelType

config = DEFAULT_CONFIG.model_copy(
    update={
        "model_name": ModelType.MINILM,
        "threshold": 0.35,
        "max_tags": 2,
    }
)

engine = TaggingEngine(config)
engine.initialize()

texts = [
    "Reviewed quarterly budget and revenue forecasts",
    "Team meeting to discuss sprint progress and blockers",
    "New feature idea: implement dark mode for the app",
    "Reading papers on attention mechanisms in neural networks",
    "Planning next quarter's product roadmap and milestones",
]

print("Batch tagging multiple texts:")
print("-" * 60)

results = engine.tag_batch(texts)

for text, result in zip(texts, results):
    tags_str = ", ".join(f"{t.topic} ({t.score:.2f})" for t in result.tags)
    print(f"\n'{text[:50]}...'")
    print(f"  Tags: {tags_str if tags_str else '(none)'}")
