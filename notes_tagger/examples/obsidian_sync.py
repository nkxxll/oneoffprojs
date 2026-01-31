"""Example: Tag all notes in an Obsidian vault."""

from pathlib import Path

from notes_tagger import TaggingEngine, DEFAULT_CONFIG
from notes_tagger.storage.obsidian import ObsidianNote, parse_markdown_note, apply_tags_to_note


def tag_obsidian_vault(vault_path: str, dry_run: bool = True) -> None:
    """Tag all markdown files in an Obsidian vault.
    
    Args:
        vault_path: Path to the Obsidian vault directory
        dry_run: If True, only print what would be done without writing
    """
    vault = Path(vault_path).expanduser()
    
    if not vault.exists():
        print(f"Vault not found: {vault}")
        return
    
    engine = TaggingEngine(DEFAULT_CONFIG)
    engine.initialize()
    
    print(f"Scanning vault: {vault}")
    print(f"Topics: {list(DEFAULT_CONFIG.topics.keys())}")
    print(f"Threshold: {DEFAULT_CONFIG.threshold}")
    print("-" * 60)
    
    markdown_files = list(vault.rglob("*.md"))
    print(f"Found {len(markdown_files)} markdown files\n")
    
    for note_path in markdown_files:
        try:
            note = parse_markdown_note(note_path)
            result = engine.tag_note(note)
            
            if result.tags:
                tag_names = [t.topic for t in result.tags]
                tags_str = ", ".join(f"{t.topic} ({t.score:.2f})" for t in result.tags)
                
                if dry_run:
                    print(f"[dry-run] {note.title}: {tags_str}")
                else:
                    apply_tags_to_note(note_path, tag_names, replace=False)
                    print(f"[tagged] {note.title}: {tags_str}")
            else:
                print(f"[skip] {note.title}: no tags above threshold")
                
        except Exception as e:
            print(f"[error] {note_path.name}: {e}")
    
    print("\nDone!")
    if dry_run:
        print("(This was a dry run. Set dry_run=False to actually write tags.)")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python obsidian_sync.py <vault_path> [--write]")
        print("\nExample:")
        print("  python obsidian_sync.py ~/Obsidian\\ Vault")
        print("  python obsidian_sync.py ~/Obsidian\\ Vault --write")
        sys.exit(1)
    
    vault_path = sys.argv[1]
    dry_run = "--write" not in sys.argv
    
    tag_obsidian_vault(vault_path, dry_run=dry_run)
