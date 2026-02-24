from __future__ import annotations

import subprocess
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_CONFIG_PATH = Path("~/.config/noteweaver/config.toml").expanduser()


def _detect_qwen_model() -> str:
    """Find the first installed Qwen model via `ollama list`, falling back to qwen3:latest."""
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.splitlines():
            name = line.split()[0]
            if name.lower().startswith("qwen3:"):
                return name
    except (FileNotFoundError, subprocess.TimeoutExpired, IndexError):
        pass
    return "qwen3:latest"


@dataclass
class ServerConfig:
    base_dir: str = "~/obsidian-notes"
    log_file: str = "noteweaver.log"
    model: str = ""
    embedding_model: str = "nomic-embed-text"

    def __post_init__(self):
        if not self.model:
            self.model = _detect_qwen_model()
        self.base_dir = str(Path(self.base_dir).expanduser().resolve())


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> ServerConfig:
    if path.exists():
        raw = tomllib.loads(path.read_text())
        section = raw.get("server", {})
        return ServerConfig(
            **{
                k: v
                for k, v in section.items()
                if k in ServerConfig.__dataclass_fields__
            }
        )
    return ServerConfig()
