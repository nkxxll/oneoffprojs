"""CLI commands for notes tagger."""

import asyncio
from pathlib import Path
from typing import Optional

import click

from notes_tagger import TaggingEngine, DEFAULT_CONFIG, load_config, LinkingEngine, LinkConfig
from notes_tagger.embeddings import EmbeddingModel
from notes_tagger.linker import EmbeddingStore
from notes_tagger.linker.similarity import compute_similarity_scores, find_top_k_neighbors
from notes_tagger.models import NoteLink
from notes_tagger.storage import (
    parse_markdown_note,
    apply_tags_to_note,
    apply_backlinks_to_note,
    apply_backlinks_to_note_async,
)

from notes_tagger_cli.utils import find_markdown_files, format_tag_result

DEFAULT_DB_PATH = ".notes_tagger/embeddings.db"


def tag_directory(
    directory: Path,
    config_path: Optional[Path],
    threshold: Optional[float],
    max_tags: Optional[int],
    recursive: bool,
    dry_run: bool,
    verbose: bool,
    replace: bool,
) -> None:
    """Tag all markdown files in a directory."""
    # Load config
    if config_path:
        config = load_config(str(config_path))
    else:
        config = DEFAULT_CONFIG.model_copy()
    
    # Override with CLI args
    if threshold is not None:
        config = config.model_copy(update={"threshold": threshold})
    if max_tags is not None:
        config = config.model_copy(update={"max_tags": max_tags})
    
    # Initialize engine
    click.echo("Initializing tagging engine...")
    engine = TaggingEngine(config)
    engine.initialize()
    click.echo(f"Model loaded. Device: {engine._model.device}")
    click.echo(f"Topics: {list(config.topics.keys())}")
    click.echo(f"Threshold: {config.threshold}")
    click.echo("-" * 60)
    
    # Find and process files
    files = list(find_markdown_files(directory, recursive, ignore_files=config.ignore_files))
    if not files:
        click.echo(f"No markdown files found in {directory}")
        return
    
    click.echo(f"Found {len(files)} markdown files")
    
    tagged_count = 0
    for note_path in files:
        try:
            note = parse_markdown_note(note_path)
            result = engine.tag_note(note)
            
            if verbose:
                click.echo(format_tag_result(result, verbose=True))
            
            if result.tags and not dry_run:
                tag_names = [tag.topic for tag in result.tags]
                apply_tags_to_note(note_path, tag_names, replace=replace)
                tagged_count += 1
                if not verbose:
                    click.echo(format_tag_result(result, verbose=False))
            elif result.tags and dry_run:
                tagged_count += 1
                click.echo(f"  [dry-run] {format_tag_result(result, verbose=verbose)}")
                
        except Exception as e:
            click.echo(f"  Error processing {note_path.name}: {e}", err=True)
    
    click.echo("-" * 60)
    action = "would tag" if dry_run else "tagged"
    click.echo(f"Done! {action} {tagged_count}/{len(files)} files")


def tag_single_file(
    file_path: Path,
    config_path: Optional[Path],
    threshold: Optional[float],
    max_tags: Optional[int],
    dry_run: bool,
    verbose: bool,
    replace: bool,
) -> None:
    """Tag a single markdown file."""
    # Load config
    if config_path:
        config = load_config(str(config_path))
    else:
        config = DEFAULT_CONFIG.model_copy()
    
    # Override with CLI args
    if threshold is not None:
        config = config.model_copy(update={"threshold": threshold})
    if max_tags is not None:
        config = config.model_copy(update={"max_tags": max_tags})
    
    # Initialize engine
    if verbose:
        click.echo("Initializing tagging engine...")
    engine = TaggingEngine(config)
    engine.initialize()
    
    if verbose:
        click.echo(f"Model loaded. Device: {engine._model.device}")
        click.echo(f"Topics: {list(config.topics.keys())}")
        click.echo(f"Threshold: {config.threshold}")
        click.echo("-" * 60)
    
    try:
        note = parse_markdown_note(file_path)
        result = engine.tag_note(note)
        
        click.echo(format_tag_result(result, verbose=verbose))
        
        if result.tags and not dry_run:
            tag_names = [tag.topic for tag in result.tags]
            apply_tags_to_note(file_path, tag_names, replace=replace)
            click.echo("  Tags written to file")
        elif dry_run and result.tags:
            click.echo("  [dry-run] Tags not written")
            
    except Exception as e:
        click.echo(f"Error processing {file_path.name}: {e}", err=True)
        raise click.Abort()


def link_directory(
    directory: Path,
    threshold: float,
    max_links: int,
    require_shared_tag: bool,
    recursive: bool,
    dry_run: bool,
    verbose: bool,
    sync: bool = False,
) -> None:
    """Find similar notes and add [[wiki links]] to them."""
    if sync:
        _link_directory_sync(
            directory, threshold, max_links, require_shared_tag,
            recursive, dry_run, verbose
        )
    else:
        asyncio.run(_link_directory_async(
            directory, threshold, max_links, require_shared_tag,
            recursive, dry_run, verbose
        ))


async def _link_directory_async(
    directory: Path,
    threshold: float,
    max_links: int,
    require_shared_tag: bool,
    recursive: bool,
    dry_run: bool,
    verbose: bool,
) -> None:
    """Async implementation of link_directory."""
    config = LinkConfig(
        threshold=threshold,
        max_links=max_links,
        require_shared_tag=require_shared_tag,
    )
    
    click.echo("Initializing linking engine...")
    engine = LinkingEngine(config)
    engine.initialize()
    click.echo(f"Model loaded. Device: {engine._model.device}")
    click.echo(f"Threshold: {config.threshold}, Max links: {config.max_links}")
    click.echo("-" * 60)
    
    files = list(find_markdown_files(directory, recursive))
    if not files:
        click.echo(f"No markdown files found in {directory}")
        return
    
    click.echo(f"Found {len(files)} markdown files")
    click.echo("Embedding notes...")
    
    notes = [parse_markdown_note(f) for f in files]
    engine.embed_notes(notes)
    
    click.echo("Finding similar notes...")
    results = engine.link_all()
    
    tasks = []
    to_link = []
    for result in results:
        if not result.links:
            continue
        
        note_path = Path(result.note_id)
        note_title = note_path.stem
        
        if verbose:
            click.echo(f"\n{note_title}:")
            for link in result.links:
                click.echo(f"  → [[{link.to_title}]] ({link.similarity:.3f})")
        
        if not dry_run:
            tasks.append(apply_backlinks_to_note_async(note_path, result.links))
            to_link.append((note_title, result.links))
        else:
            if not verbose:
                link_titles = [f"[[{l.to_title}]]" for l in result.links]
                click.echo(f"[dry-run] {note_title}: {', '.join(link_titles)}")
    
    if tasks:
        await asyncio.gather(*tasks)
        if not verbose:
            for note_title, links in to_link:
                link_titles = [f"[[{l.to_title}]]" for l in links]
                click.echo(f"{note_title}: {', '.join(link_titles)}")
    
    linked_count = len(to_link) if not dry_run else sum(1 for r in results if r.links)
    click.echo("-" * 60)
    action = "would link" if dry_run else "linked"
    click.echo(f"Done! {action} {linked_count}/{len(files)} files")


def analyze_directory(
    directory: Path,
    db_path: Optional[Path],
    model_name: str,
    device: Optional[str],
    recursive: bool,
    verbose: bool,
) -> None:
    """Analyze notes and store embeddings in SQLite database."""
    from notes_tagger.models import ModelType
    
    resolved_db = db_path or (directory / DEFAULT_DB_PATH)
    
    click.echo("Initializing embedding model...")
    model = EmbeddingModel(model_name, device)
    click.echo(f"Model loaded: {model.model_name}, Device: {model.device}")
    click.echo("-" * 60)
    
    files = list(find_markdown_files(directory, recursive))
    if not files:
        click.echo(f"No markdown files found in {directory}")
        return
    
    click.echo(f"Found {len(files)} markdown files")
    click.echo("Parsing and embedding notes...")
    
    notes_data = []
    texts = []
    for f in files:
        note = parse_markdown_note(f)
        notes_data.append((note.id, note.title, note.tags or []))
        texts.append(f"{note.title}\n\n{note.body}")
    
    embeddings = model.embed_batch(texts)
    
    click.echo(f"Storing embeddings in {resolved_db}...")
    with EmbeddingStore(resolved_db) as store:
        store.clear()
        store.upsert_notes_batch(notes_data, embeddings, model.model_name)
        store.set_metadata("source_directory", str(directory.resolve()))
    
    click.echo("-" * 60)
    click.echo(f"Done! Analyzed {len(files)} notes, embeddings stored in {resolved_db}")


def link_from_store(
    directory: Path,
    db_path: Optional[Path],
    threshold: float,
    max_links: int,
    require_shared_tag: bool,
    dry_run: bool,
    verbose: bool,
) -> None:
    """Find similar notes from SQLite store and apply backlinks."""
    resolved_db = db_path or (directory / DEFAULT_DB_PATH)
    
    if not resolved_db.exists():
        click.echo(f"Database not found: {resolved_db}")
        click.echo("Run 'notes-tagger analyze' first to build the embedding database.")
        raise SystemExit(1)
    
    click.echo(f"Loading embeddings from {resolved_db}...")
    
    with EmbeddingStore(resolved_db) as store:
        note_ids, embeddings = store.get_all_embeddings()
        
        if len(note_ids) == 0:
            click.echo("No embeddings found in database.")
            return
        
        click.echo(f"Loaded {len(note_ids)} note embeddings")
        click.echo(f"Threshold: {threshold}, Max links: {max_links}")
        click.echo("-" * 60)
        
        id_to_idx = {nid: i for i, nid in enumerate(note_ids)}
        note_metadata = {nid: store.get_note_metadata(nid) for nid in note_ids}
    
    click.echo("Finding similar notes...")
    linked_count = 0
    
    for i, note_id in enumerate(note_ids):
        note_path = Path(note_id)
        if not note_path.exists():
            if verbose:
                click.echo(f"Skipping {note_id}: file not found")
            continue
        
        scores = compute_similarity_scores(embeddings, i)
        neighbors = find_top_k_neighbors(
            scores,
            exclude_idx=i,
            threshold=threshold,
            max_results=max_links,
        )
        
        source_meta = note_metadata.get(note_id)
        source_tags = set(source_meta[1]) if source_meta else set()
        
        links = []
        for idx, score in neighbors:
            target_id = note_ids[idx]
            target_meta = note_metadata.get(target_id)
            if not target_meta:
                continue
            
            target_title, target_tags = target_meta
            shared_tags = sorted(source_tags & set(target_tags))
            
            if require_shared_tag and not shared_tags:
                continue
            
            links.append(NoteLink(
                from_id=note_id,
                to_id=target_id,
                to_title=target_title,
                similarity=score,
                shared_tags=shared_tags,
            ))
        
        if not links:
            continue
        
        note_title = note_path.stem
        
        if verbose:
            click.echo(f"\n{note_title}:")
            for link in links:
                click.echo(f"  → [[{link.to_title}]] ({link.similarity:.3f})")
        
        if not dry_run:
            apply_backlinks_to_note(note_path, links)
            linked_count += 1
            if not verbose:
                link_titles = [f"[[{l.to_title}]]" for l in links]
                click.echo(f"{note_title}: {', '.join(link_titles)}")
        else:
            linked_count += 1
            if not verbose:
                link_titles = [f"[[{l.to_title}]]" for l in links]
                click.echo(f"[dry-run] {note_title}: {', '.join(link_titles)}")
    
    click.echo("-" * 60)
    action = "would link" if dry_run else "linked"
    click.echo(f"Done! {action} {linked_count}/{len(note_ids)} files")


def _link_directory_sync(
    directory: Path,
    threshold: float,
    max_links: int,
    require_shared_tag: bool,
    recursive: bool,
    dry_run: bool,
    verbose: bool,
) -> None:
    """Sync implementation of link_directory."""
    config = LinkConfig(
        threshold=threshold,
        max_links=max_links,
        require_shared_tag=require_shared_tag,
    )
    
    click.echo("Initializing linking engine...")
    engine = LinkingEngine(config)
    engine.initialize()
    click.echo(f"Model loaded. Device: {engine._model.device}")
    click.echo(f"Threshold: {config.threshold}, Max links: {config.max_links}")
    click.echo("-" * 60)
    
    files = list(find_markdown_files(directory, recursive))
    if not files:
        click.echo(f"No markdown files found in {directory}")
        return
    
    click.echo(f"Found {len(files)} markdown files")
    click.echo("Embedding notes...")
    
    notes = [parse_markdown_note(f) for f in files]
    engine.embed_notes(notes)
    
    click.echo("Finding similar notes...")
    results = engine.link_all()
    
    linked_count = 0
    for result in results:
        if not result.links:
            continue
        
        note_path = Path(result.note_id)
        note_title = note_path.stem
        
        if verbose:
            click.echo(f"\n{note_title}:")
            for link in result.links:
                click.echo(f"  → [[{link.to_title}]] ({link.similarity:.3f})")
        
        if not dry_run:
            apply_backlinks_to_note(note_path, result.links)
            linked_count += 1
            if not verbose:
                link_titles = [f"[[{l.to_title}]]" for l in result.links]
                click.echo(f"{note_title}: {', '.join(link_titles)}")
        else:
            linked_count += 1
            if not verbose:
                link_titles = [f"[[{l.to_title}]]" for l in result.links]
                click.echo(f"[dry-run] {note_title}: {', '.join(link_titles)}")
    
    click.echo("-" * 60)
    action = "would link" if dry_run else "linked"
    click.echo(f"Done! {action} {linked_count}/{len(files)} files")
