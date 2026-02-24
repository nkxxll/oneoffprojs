from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


class Logger:
    """Configure and expose a reusable application logger."""

    def __init__(
        self,
        name: str = "noteweaver",
        level: int = logging.INFO,
        to_stdout: bool = True,
        file_path: str | Path | None = None,
        max_bytes: int = 10 * 1024 * 1024,
        backup_count: int = 3,
        fmt: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    ) -> None:
        self.name = name
        self.level = level
        self.to_stdout = to_stdout
        self.file_path = Path(file_path) if file_path is not None else None
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.fmt = fmt

    def get(self) -> logging.Logger:
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        logger.propagate = False

        # Avoid duplicate handlers when get() is called multiple times.
        if logger.handlers:
            logger.handlers.clear()

        formatter = logging.Formatter(self.fmt)

        if self.to_stdout:
            handler: logging.Handler = logging.StreamHandler(sys.stdout)
        else:
            if self.file_path is None:
                raise ValueError("file_path is required when to_stdout=False")

            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            handler = RotatingFileHandler(
                filename=self.file_path,
                maxBytes=self.max_bytes,
                backupCount=self.backup_count,
            )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger
