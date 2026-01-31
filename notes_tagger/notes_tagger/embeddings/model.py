"""Embedding model wrapper for sentence transformers."""

import os
from pathlib import Path
from typing import Optional

import numpy as np
from huggingface_hub import snapshot_download, try_to_load_from_cache
from huggingface_hub.utils import LocalEntryNotFoundError
from numpy import ndarray
from sentence_transformers import SentenceTransformer

from notes_tagger.models import ModelType

# Increase timeout for Hugging Face Hub downloads (default is 10s)
os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", "120")

# Use ~/.cache for HF models (default HuggingFace location)
HF_CACHE_DIR = Path(os.environ.get("HF_HOME", Path.home() / ".cache" / "huggingface")) / "hub"


class EmbeddingModel:
    """Wrapper around SentenceTransformer for consistent interface."""

    def __init__(self, model_name: ModelType | str, device: Optional[str] = None):
        self.model_name = str(model_name.value if isinstance(model_name, ModelType) else model_name)
        self.device = device or self._auto_detect_device()
        self.model = self._load_model_with_retry()
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

    def embed(self, text: str) -> ndarray:
        """Single text → embedding."""
        return self.model.encode(text, convert_to_numpy=True, normalize_embeddings=True)

    def embed_batch(self, texts: list[str], batch_size: int = 32) -> ndarray:
        """Batch encode with automatic normalization."""
        return self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

    def _is_model_cached(self) -> bool:
        """Check if model is already downloaded in HF cache."""
        try:
            result = try_to_load_from_cache(self.model_name, "config.json")
            return result is not None and not isinstance(result, LocalEntryNotFoundError)
        except Exception:
            return False

    def _ensure_model_downloaded(self) -> None:
        """Download model to cache if not already present."""
        if not self._is_model_cached():
            snapshot_download(
                self.model_name,
                local_files_only=False,
            )

    def _load_model_with_retry(self, max_retries: int = 3) -> SentenceTransformer:
        """Load model with retry on timeout, using cache when available."""
        import time
        from httpx import ReadTimeout
        
        if self._is_model_cached():
            return SentenceTransformer(self.model_name, device=self.device, local_files_only=True)
        
        for attempt in range(max_retries):
            try:
                self._ensure_model_downloaded()
                return SentenceTransformer(self.model_name, device=self.device, local_files_only=True)
            except ReadTimeout:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                else:
                    raise

    def _auto_detect_device(self) -> str:
        """Detect GPU availability."""
        try:
            import torch
            if torch.backends.mps.is_available():
                return "mps"
            return "cuda" if torch.cuda.is_available() else "cpu"
        except Exception:
            return "cpu"
