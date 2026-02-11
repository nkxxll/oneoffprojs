from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Storage:
    run_dir: Path

    @classmethod
    def create(cls, base_dir: Path, run_name: str) -> "Storage":
        run_dir = base_dir / run_name
        run_dir.mkdir(parents=True, exist_ok=True)
        return cls(run_dir=run_dir)

    def write_markdown(self, filename: str, content: str, metadata: dict[str, str] | None = None) -> Path:
        path = self.run_dir / filename
        lines: list[str] = []
        if metadata:
            lines.append("---")
            for key, value in metadata.items():
                lines.append(f"{key}: {value}")
            lines.append("---\n")
        lines.append(content.strip())
        path.write_text("\n".join(lines))
        return path

    def write_sources(self, sources: list[str], model: str) -> Path:
        content = "\n".join(f"- {src}" for src in sources)
        return self.write_markdown(
            "sources.md",
            content,
            metadata={
                "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                "model": model,
            },
        )
