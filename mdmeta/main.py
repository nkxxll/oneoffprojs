#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
import argparse
import sys
from datetime import datetime
from pathlib import Path
import re
import readline
import atexit
import os


def setup_readline():
    """Configure readline with emacs keybindings and auto-completion"""
    # Enable emacs-style editing (ctrl-w delete word, ctrl-u delete line, etc.)
    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("set editing-mode emacs")
    
    # Disable history file to avoid clutter
    # (readline automatically saves to ~/.python_history, but we disable it)
    
    # Custom completer for common values
    def completer(text, state):
        options = {
            "author": ["Anonymous", ""],
            "tags": [""],
        }
        return None
    
    readline.set_completer(completer)


def parse_args():
    parser = argparse.ArgumentParser(description="Add/update YAML metadata to markdown files")
    parser.add_argument("file", help="Path to markdown file")
    parser.add_argument("--title", "-t", help="Metadata title")
    parser.add_argument("--author", "-a", help="Metadata author")
    parser.add_argument("--description", "-d", help="Metadata description")
    parser.add_argument("--date", help=f"Metadata date (default: today)")
    parser.add_argument("--tags", help="Comma-separated tags")
    return parser.parse_args()


def has_frontmatter(content: str) -> bool:
    """Check if content starts with YAML frontmatter"""
    return content.startswith("---")


def extract_frontmatter(content: str) -> tuple[str, str]:
    """Extract YAML frontmatter and remaining content"""
    if not has_frontmatter(content):
        return "", content
    
    # Find closing ---
    match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if match:
        return match.group(1), match.group(2)
    return "", content


def get_metadata(args) -> dict:
    """Prompt user for metadata with sensible defaults, or use provided flags"""
    print("\n=== Markdown Metadata Setup ===\n")
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Title (required)
    if args.title:
        title = args.title
    else:
        title = input("Title [required]: ").strip()
        while not title:
            title = input("Title is required. Please enter a title: ").strip()
    
    # Author
    if args.author:
        author = args.author
    else:
        author = input("Author [Anonymous]: ").strip() or "Anonymous"
    
    # Description
    if args.description:
        description = args.description
    else:
        description = input("Description (optional): ").strip() or ""
    
    # Date
    if args.date:
        date = args.date
    else:
        date = input(f"Date [{today}]: ").strip() or today
    
    # Tags
    if args.tags:
        tags = args.tags
    else:
        tags = input("Tags (comma-separated, optional): ").strip()
    
    metadata = {
        "title": title,
        "date": date,
        "author": author,
    }
    
    if description:
        metadata["description"] = description
    if tags:
        metadata["tags"] = [t.strip() for t in tags.split(",")]
    
    return metadata


def dict_to_yaml(data: dict) -> str:
    """Convert dict to YAML format"""
    lines = []
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f'  - "{item}"')
        elif isinstance(value, str):
            lines.append(f'{key}: "{value}"')
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines)


def create_frontmatter(metadata: dict) -> str:
    """Create frontmatter string"""
    yaml_content = dict_to_yaml(metadata)
    return f"---\n{yaml_content}\n---\n"


def main():
    setup_readline()
    args = parse_args()
    file_path = Path(args.file)
    
    # Get metadata from user or flags
    metadata = get_metadata(args)
    frontmatter = create_frontmatter(metadata)
    
    if file_path.exists():
        # File exists - check for existing frontmatter
        content = file_path.read_text()
        
        if has_frontmatter(content):
            # Has frontmatter - ask to overwrite
            response = input("\nFrontmatter already exists. Overwrite? (y/n): ").strip().lower()
            if response != "y":
                print("Aborted.")
                sys.exit(0)
            
            # Remove old frontmatter and prepend new one
            _, remaining = extract_frontmatter(content)
            new_content = frontmatter + remaining
        else:
            # No frontmatter - prepend new one
            new_content = frontmatter + content
        
        file_path.write_text(new_content)
        print(f"\n✓ Updated {file_path}")
    else:
        # File doesn't exist - create with metadata
        file_path.write_text(frontmatter)
        print(f"\n✓ Created {file_path}")


if __name__ == "__main__":
    main()
