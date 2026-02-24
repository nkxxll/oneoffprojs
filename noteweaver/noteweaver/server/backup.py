from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

from noteweaver.logger import Logger

logger = Logger(name="noteweaver.backup").get()

MAX_BACKUPS = 10


def backup_before_refine(file_path: Path, base_dir: str) -> Path:
    base = Path(base_dir).resolve()
    rel = file_path.resolve().relative_to(base)

    backup_dir = base / ".noteweaver" / "backups" / rel.parent
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_file = backup_dir / f"{rel.name}.{timestamp}"

    shutil.copy2(file_path, backup_file)
    logger.info("Backed up %s to %s", file_path, backup_file)

    existing = sorted(backup_dir.glob(f"{rel.name}.*"))
    if len(existing) > MAX_BACKUPS:
        for old in existing[: len(existing) - MAX_BACKUPS]:
            old.unlink()
            logger.info("Pruned old backup %s", old)

    return backup_file
