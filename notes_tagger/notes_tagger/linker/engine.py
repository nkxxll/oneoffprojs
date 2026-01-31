"""LinkingEngine for finding semantically similar notes."""

from typing import Optional

from numpy import ndarray

from notes_tagger.embeddings import EmbeddingModel
from notes_tagger.linker.config import LinkConfig
from notes_tagger.linker.similarity import compute_similarity_scores, find_top_k_neighbors
from notes_tagger.models import Note, NoteLink, LinkResult


class LinkingEngine:
    """Engine for finding semantically similar notes and creating links."""

    def __init__(self, config: Optional[LinkConfig] = None):
        self.config = config or LinkConfig()
        self._model: Optional[EmbeddingModel] = None
        self._note_embeddings: Optional[ndarray] = None
        self._notes: list[Note] = []

    def initialize(self) -> None:
        """Load embedding model."""
        self._model = EmbeddingModel(self.config.model_name, self.config.device)

    def embed_notes(self, notes: list[Note]) -> None:
        """Embed all notes and store for similarity search.
        
        Args:
            notes: List of notes to embed
        """
        if self._model is None:
            raise RuntimeError("Engine not initialized. Call initialize() first.")
        
        self._notes = notes
        texts = [f"{n.title}\n\n{n.body}" for n in notes]
        self._note_embeddings = self._model.embed_batch(texts)

    def _get_shared_tags(self, note_a: Note, note_b: Note) -> list[str]:
        """Get shared tags between two notes."""
        tags_a = set(note_a.tags or [])
        tags_b = set(note_b.tags or [])
        return sorted(tags_a & tags_b)

    def find_similar(self, note_idx: int) -> list[NoteLink]:
        """Find top-K similar notes for a given note.
        
        Args:
            note_idx: Index of the note in the embedded notes list
            
        Returns:
            List of NoteLink objects for similar notes
        """
        if self._note_embeddings is None:
            raise RuntimeError("No notes embedded. Call embed_notes() first.")
        
        scores = compute_similarity_scores(self._note_embeddings, note_idx)
        neighbors = find_top_k_neighbors(
            scores,
            exclude_idx=note_idx,
            threshold=self.config.threshold,
            max_results=self.config.max_links,
        )
        
        source_note = self._notes[note_idx]
        links = []
        
        for idx, score in neighbors:
            target_note = self._notes[idx]
            shared_tags = self._get_shared_tags(source_note, target_note)
            
            if self.config.require_shared_tag and not shared_tags:
                continue
            
            links.append(NoteLink(
                from_id=source_note.id,
                to_id=target_note.id,
                to_title=target_note.title,
                similarity=score,
                shared_tags=shared_tags,
            ))
        
        return links

    def link_all(self) -> list[LinkResult]:
        """Find similar notes for all notes.
        
        Returns:
            List of LinkResult objects, one per note
        """
        if self._note_embeddings is None:
            raise RuntimeError("No notes embedded. Call embed_notes() first.")
        
        results = []
        for i in range(len(self._notes)):
            links = self.find_similar(i)
            results.append(LinkResult(note_id=self._notes[i].id, links=links))
        return results
