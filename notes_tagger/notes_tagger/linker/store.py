"""SQLite-based storage for note embeddings."""

import sqlite3
from pathlib import Path
from typing import Optional
import numpy as np
from numpy import ndarray


class EmbeddingStore:
    """SQLite store for note embeddings with metadata."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        """Open database connection and create tables."""
        self._conn = sqlite3.connect(self.db_path)
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                tags TEXT,
                embedding BLOB NOT NULL,
                model_name TEXT NOT NULL,
                embedding_dim INTEGER NOT NULL
            )
        """)
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        self._conn.commit()

    def close(self) -> None:
        """Close database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "EmbeddingStore":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def clear(self) -> None:
        """Clear all stored embeddings."""
        if not self._conn:
            raise RuntimeError("Not connected")
        self._conn.execute("DELETE FROM notes")
        self._conn.commit()

    def upsert_note(
        self,
        note_id: str,
        title: str,
        tags: list[str],
        embedding: ndarray,
        model_name: str,
    ) -> None:
        """Insert or update a note embedding."""
        if not self._conn:
            raise RuntimeError("Not connected")
        
        tags_str = ",".join(tags) if tags else ""
        embedding_blob = embedding.astype(np.float32).tobytes()
        
        self._conn.execute("""
            INSERT OR REPLACE INTO notes (id, title, tags, embedding, model_name, embedding_dim)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (note_id, title, tags_str, embedding_blob, model_name, len(embedding)))
        self._conn.commit()

    def upsert_notes_batch(
        self,
        notes: list[tuple[str, str, list[str]]],
        embeddings: ndarray,
        model_name: str,
    ) -> None:
        """Batch insert/update note embeddings.
        
        Args:
            notes: List of (id, title, tags) tuples
            embeddings: Embedding matrix (N x D)
            model_name: Model used to create embeddings
        """
        if not self._conn:
            raise RuntimeError("Not connected")
        
        rows = []
        for i, (note_id, title, tags) in enumerate(notes):
            tags_str = ",".join(tags) if tags else ""
            embedding_blob = embeddings[i].astype(np.float32).tobytes()
            rows.append((note_id, title, tags_str, embedding_blob, model_name, embeddings.shape[1]))
        
        self._conn.executemany("""
            INSERT OR REPLACE INTO notes (id, title, tags, embedding, model_name, embedding_dim)
            VALUES (?, ?, ?, ?, ?, ?)
        """, rows)
        self._conn.commit()

    def get_note_count(self) -> int:
        """Get number of stored notes."""
        if not self._conn:
            raise RuntimeError("Not connected")
        cursor = self._conn.execute("SELECT COUNT(*) FROM notes")
        return cursor.fetchone()[0]

    def get_all_notes(self) -> list[tuple[str, str, list[str]]]:
        """Get all notes (id, title, tags)."""
        if not self._conn:
            raise RuntimeError("Not connected")
        
        cursor = self._conn.execute("SELECT id, title, tags FROM notes")
        results = []
        for row in cursor:
            note_id, title, tags_str = row
            tags = tags_str.split(",") if tags_str else []
            results.append((note_id, title, tags))
        return results

    def get_all_embeddings(self) -> tuple[list[str], ndarray]:
        """Load all embeddings into memory for similarity search.
        
        Returns:
            Tuple of (note_ids list, embeddings matrix)
        """
        if not self._conn:
            raise RuntimeError("Not connected")
        
        cursor = self._conn.execute(
            "SELECT id, embedding, embedding_dim FROM notes ORDER BY id"
        )
        
        note_ids = []
        embeddings_list = []
        
        for row in cursor:
            note_id, embedding_blob, dim = row
            embedding = np.frombuffer(embedding_blob, dtype=np.float32)
            note_ids.append(note_id)
            embeddings_list.append(embedding)
        
        if not embeddings_list:
            return [], np.array([])
        
        return note_ids, np.vstack(embeddings_list)

    def get_note_metadata(self, note_id: str) -> Optional[tuple[str, list[str]]]:
        """Get title and tags for a note.
        
        Returns:
            Tuple of (title, tags) or None if not found
        """
        if not self._conn:
            raise RuntimeError("Not connected")
        
        cursor = self._conn.execute(
            "SELECT title, tags FROM notes WHERE id = ?", (note_id,)
        )
        row = cursor.fetchone()
        if row:
            title, tags_str = row
            tags = tags_str.split(",") if tags_str else []
            return title, tags
        return None

    def set_metadata(self, key: str, value: str) -> None:
        """Set a metadata value."""
        if not self._conn:
            raise RuntimeError("Not connected")
        self._conn.execute(
            "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
            (key, value)
        )
        self._conn.commit()

    def get_metadata(self, key: str) -> Optional[str]:
        """Get a metadata value."""
        if not self._conn:
            raise RuntimeError("Not connected")
        cursor = self._conn.execute(
            "SELECT value FROM metadata WHERE key = ?", (key,)
        )
        row = cursor.fetchone()
        return row[0] if row else None
