from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from langchain_ollama import OllamaEmbeddings

from noteweaver.logger import Logger
from noteweaver.models import SearchResult

INDEX_DIR_NAME = ".noteweaver_index"
INDEX_FILE = "index.json"
SUPPORTED_EXTENSIONS = {".txt", ".md"}
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

logger = Logger(name="noteweaver.indexer").get()


def _split_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    if len(text) <= chunk_size:
        return [text] if text.strip() else []
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def _index_path(base_dir: Path) -> Path:
    return base_dir / INDEX_DIR_NAME / INDEX_FILE


def _collect_chunks(base_dir: Path) -> list[dict]:
    chunks: list[dict] = []
    for ext in SUPPORTED_EXTENSIONS:
        for file_path in base_dir.rglob(f"*{ext}"):
            if INDEX_DIR_NAME in file_path.parts:
                continue
            try:
                text = file_path.read_text(encoding="utf-8")
            except Exception:
                logger.warning("Skipping unreadable file %s", file_path)
                continue
            rel_path = str(file_path.relative_to(base_dir))
            split = _split_text(text)
            for i, chunk in enumerate(split):
                chunks.append({"source": rel_path, "chunk_index": i, "text": chunk})
    return chunks


def index_directory(base_dir: str, embedding_model: str) -> int:
    base = Path(base_dir).resolve()
    logger.info("Indexing directory %s with model %s", base, embedding_model)

    chunks = _collect_chunks(base)
    if not chunks:
        logger.info("No documents found to index")
        return 0

    embeddings = OllamaEmbeddings(model=embedding_model)
    texts = [c["text"] for c in chunks]
    vectors = embeddings.embed_documents(texts)

    index_data = {
        "chunks": chunks,
        "vectors": [v for v in vectors],
    }

    index_file = _index_path(base)
    index_file.parent.mkdir(parents=True, exist_ok=True)
    index_file.write_text(json.dumps(index_data), encoding="utf-8")

    logger.info("Indexed %d chunks from %s", len(chunks), base)
    return len(chunks)


def search(query: str, base_dir: str, embedding_model: str, top_k: int = 5) -> list[SearchResult]:
    base = Path(base_dir).resolve()
    index_file = _index_path(base)

    if not index_file.exists():
        return []

    index_data = json.loads(index_file.read_text(encoding="utf-8"))
    chunks = index_data["chunks"]
    vectors = np.array(index_data["vectors"])

    embeddings = OllamaEmbeddings(model=embedding_model)
    query_vector = np.array(embeddings.embed_query(query))

    # Cosine similarity
    norms = np.linalg.norm(vectors, axis=1) * np.linalg.norm(query_vector)
    norms = np.where(norms == 0, 1, norms)
    similarities = vectors @ query_vector / norms

    top_indices = np.argsort(similarities)[::-1][:top_k]

    return [
        SearchResult(
            path=chunks[i]["source"],
            chunk=chunks[i]["text"],
            score=round(float(similarities[i]), 4),
        )
        for i in top_indices
    ]


def index_exists(base_dir: str) -> bool:
    return _index_path(Path(base_dir).resolve()).exists()
