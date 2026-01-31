"""CLI entry point for notes tagger."""

from pathlib import Path
from typing import Optional

import click

from notes_tagger_cli.commands import (
    tag_directory,
    tag_single_file,
    link_directory,
    analyze_directory,
    link_from_store,
)


@click.group()
@click.version_option(version="0.1.0", prog_name="notes-tagger")
def cli() -> None:
    """Notes Tagger - Semantic note tagging using sentence embeddings."""
    pass


@cli.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "-c", "--config",
    type=click.Path(exists=True, path_type=Path),
    help="Path to config file (JSON/YAML)",
)
@click.option(
    "-t", "--threshold",
    type=float,
    help="Minimum similarity threshold (0.0-1.0)",
)
@click.option(
    "-m", "--max-tags",
    type=int,
    help="Maximum number of tags per note",
)
@click.option(
    "-r", "--recursive/--no-recursive",
    default=True,
    help="Recursively search directories (default: True)",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be tagged without writing",
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="Show detailed output with scores",
)
@click.option(
    "--replace/--append",
    default=False,
    help="Replace existing tags (default: append)",
)
def tag(
    path: Path,
    config: Optional[Path],
    threshold: Optional[float],
    max_tags: Optional[int],
    recursive: bool,
    dry_run: bool,
    verbose: bool,
    replace: bool,
) -> None:
    """Tag markdown notes with semantic topics.
    
    PATH can be a single markdown file or a directory.
    
    Examples:
    
        notes-tagger tag ./notes
        
        notes-tagger tag ./notes --threshold 0.4 --max-tags 2
        
        notes-tagger tag ./notes --dry-run --verbose
        
        notes-tagger tag note.md --replace
    """
    if path.is_file():
        tag_single_file(
            file_path=path,
            config_path=config,
            threshold=threshold,
            max_tags=max_tags,
            dry_run=dry_run,
            verbose=verbose,
            replace=replace,
        )
    elif path.is_dir():
        tag_directory(
            directory=path,
            config_path=config,
            threshold=threshold,
            max_tags=max_tags,
            recursive=recursive,
            dry_run=dry_run,
            verbose=verbose,
            replace=replace,
        )
    else:
        raise click.BadParameter(f"{path} is not a file or directory")


@cli.command()
def topics() -> None:
    """List available topics from the default configuration."""
    from notes_tagger import DEFAULT_CONFIG
    
    click.echo("Default topics:")
    click.echo("-" * 40)
    for topic, description in DEFAULT_CONFIG.topics.items():
        click.echo(f"  {topic}: {description}")


@cli.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "-t", "--threshold",
    type=float,
    default=0.45,
    help="Minimum similarity threshold (default: 0.45)",
)
@click.option(
    "-m", "--max-links",
    type=int,
    default=5,
    help="Maximum number of links per note (default: 5)",
)
@click.option(
    "--require-shared-tag",
    is_flag=True,
    help="Only link notes that share at least one tag",
)
@click.option(
    "-r", "--recursive/--no-recursive",
    default=True,
    help="Recursively search directories (default: True)",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Preview links without writing to files",
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="Show detailed output with similarity scores",
)
@click.option(
    "--sync",
    is_flag=True,
    help="Use synchronous file writes instead of async",
)
def link(
    path: Path,
    threshold: float,
    max_links: int,
    require_shared_tag: bool,
    recursive: bool,
    dry_run: bool,
    verbose: bool,
    sync: bool,
) -> None:
    """Add [[wiki links]] to semantically similar notes.
    
    PATH must be a directory containing markdown notes.
    
    Examples:
    
        notes-tagger link ./vault --dry-run
        
        notes-tagger link ./vault --threshold 0.5 --max-links 3
        
        notes-tagger link ./vault --require-shared-tag
    """
    if not path.is_dir():
        raise click.BadParameter(f"{path} must be a directory")
    
    link_directory(
        directory=path,
        threshold=threshold,
        max_links=max_links,
        require_shared_tag=require_shared_tag,
        recursive=recursive,
        dry_run=dry_run,
        verbose=verbose,
        sync=sync,
    )


@cli.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--db",
    type=click.Path(path_type=Path),
    help="Path to SQLite database (default: <path>/.notes_tagger/embeddings.db)",
)
@click.option(
    "--model",
    type=str,
    default="all-mpnet-base-v2",
    help="Embedding model name (default: all-mpnet-base-v2)",
)
@click.option(
    "--device",
    type=str,
    help="Device to use (cpu, cuda, mps). Auto-detected if not set.",
)
@click.option(
    "-r", "--recursive/--no-recursive",
    default=True,
    help="Recursively search directories (default: True)",
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="Show detailed output",
)
def analyze(
    path: Path,
    db: Optional[Path],
    model: str,
    device: Optional[str],
    recursive: bool,
    verbose: bool,
) -> None:
    """Analyze notes and store embeddings in SQLite database.
    
    This command reads all markdown files, computes embeddings, and stores
    them in a SQLite database. Run this before 'link-db' to avoid
    "too many open files" errors on large directories.
    
    Examples:
    
        notes-tagger analyze ./vault
        
        notes-tagger analyze ./vault --db ./my-embeddings.db
        
        notes-tagger analyze ./vault --model all-MiniLM-L6-v2
    """
    if not path.is_dir():
        raise click.BadParameter(f"{path} must be a directory")
    
    analyze_directory(
        directory=path,
        db_path=db,
        model_name=model,
        device=device,
        recursive=recursive,
        verbose=verbose,
    )


@cli.command("link-db")
@click.argument("path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--db",
    type=click.Path(path_type=Path),
    help="Path to SQLite database (default: <path>/.notes_tagger/embeddings.db)",
)
@click.option(
    "-t", "--threshold",
    type=float,
    default=0.45,
    help="Minimum similarity threshold (default: 0.45)",
)
@click.option(
    "-m", "--max-links",
    type=int,
    default=5,
    help="Maximum number of links per note (default: 5)",
)
@click.option(
    "--require-shared-tag",
    is_flag=True,
    help="Only link notes that share at least one tag",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Preview links without writing to files",
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="Show detailed output with similarity scores",
)
def link_db(
    path: Path,
    db: Optional[Path],
    threshold: float,
    max_links: int,
    require_shared_tag: bool,
    dry_run: bool,
    verbose: bool,
) -> None:
    """Add [[wiki links]] using pre-computed embeddings from SQLite.
    
    Run 'notes-tagger analyze' first to build the embedding database.
    This command reads embeddings from SQLite and applies links one file
    at a time, avoiding "too many open files" errors.
    
    Examples:
    
        notes-tagger link-db ./vault --dry-run
        
        notes-tagger link-db ./vault --threshold 0.5 --max-links 3
    """
    if not path.is_dir():
        raise click.BadParameter(f"{path} must be a directory")
    
    link_from_store(
        directory=path,
        db_path=db,
        threshold=threshold,
        max_links=max_links,
        require_shared_tag=require_shared_tag,
        dry_run=dry_run,
        verbose=verbose,
    )


if __name__ == "__main__":
    cli()
