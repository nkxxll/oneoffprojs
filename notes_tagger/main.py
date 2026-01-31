"""Test script for notes tagger with test_notes directory."""

import asyncio
from pathlib import Path

from notes_tagger import TaggingEngine, DEFAULT_CONFIG
from notes_tagger.storage import parse_markdown_note_async, apply_tags_to_note_async


async def process_note(engine: TaggingEngine, note_path: Path) -> tuple[Path, list[str]]:
    """Process a single note: parse, tag, and apply tags."""
    note = await parse_markdown_note_async(note_path)
    result = engine.tag_note(note)
    
    if result.tags:
        tag_names = [tag.topic for tag in result.tags]
        await apply_tags_to_note_async(note_path, tag_names, replace=True)
        return note_path, [(tag.topic, tag.score) for tag in result.tags]
    return note_path, []


async def main():
    print("Initializing TaggingEngine...")
    engine = TaggingEngine(DEFAULT_CONFIG)
    engine.initialize()
    print(f"Model loaded. Device: {engine._model.device}")
    print(f"Topics: {list(DEFAULT_CONFIG.topics.keys())}")
    print(f"Threshold: {DEFAULT_CONFIG.threshold}")
    print("-" * 60)

    test_notes_dir = Path(__file__).parent / "test_notes"
    note_paths = sorted(test_notes_dir.glob("*.md"))
    
    tasks = [process_note(engine, path) for path in note_paths]
    results = await asyncio.gather(*tasks)
    
    for note_path, tags in results:
        print(f"\n📄 {note_path.stem}")
        print(f"   File: {note_path.name}")
        if tags:
            for topic, score in tags:
                print(f"   🏷️  {topic}: {score:.3f}")
            print(f"   ✅ Tags written to file")
        else:
            print("   (no tags above threshold)")


if __name__ == "__main__":
    asyncio.run(main())
