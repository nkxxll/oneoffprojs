"""Basic tagging example using the notes_tagger library."""

from notes_tagger import TaggingEngine, DEFAULT_CONFIG

config = DEFAULT_CONFIG.model_copy(update={"threshold": 0.35})

engine = TaggingEngine(config)
engine.initialize()

result = engine.tag("Reviewed quarterly budget and revenue forecast for Q4")

print("Tagged text: 'Reviewed quarterly budget and revenue forecast for Q4'")
print("\nResults:")
for tag in result.tags:
    print(f"  {tag.topic}: {tag.score:.3f}")
