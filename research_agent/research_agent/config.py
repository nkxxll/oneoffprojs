from __future__ import annotations

from pathlib import Path
import os
import re
import tomllib

from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen3:14b"
    output_dir: Path = Field(default_factory=lambda: Path("research"))
    sources: list[str] = Field(default_factory=list)
    run_mode: str = "oneshot"  # oneshot | service
    job_queue_dir: Path = Field(default_factory=lambda: Path(".job_queue"))
    request_timeout_sec: float = 120.0
    max_chunk_chars: int = 4000
    max_context_chunks: int = 6
    max_additional_sources: int = 20
    github_client_id: str | None = None
    github_token: str | None = None
    skip_github: bool = False


def _expand_path(path: str | Path) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(str(path)))).resolve()


def load_config(path: str | Path) -> AgentConfig:
    cfg_path = _expand_path(path)
    if not cfg_path.exists():
        raise FileNotFoundError(f"Config file not found: {cfg_path}")

    raw = tomllib.loads(cfg_path.read_text())
    if "ollama_base_url" in raw:
        raw["ollama_base_url"] = str(raw["ollama_base_url"]).rstrip("/")
    if "ollama_model" in raw:
        raw["ollama_model"] = str(raw["ollama_model"]).strip()
    if "output_dir" in raw:
        raw["output_dir"] = _expand_path(raw["output_dir"])
    if "job_queue_dir" in raw:
        raw["job_queue_dir"] = _expand_path(raw["job_queue_dir"])
    if "github_client_id" not in raw:
        env_client_id = os.environ.get("GITHUB_CLIENT_ID")
        if env_client_id:
            raw["github_client_id"] = env_client_id
    if "github_token" not in raw:
        env_token = os.environ.get("GITHUB_TOKEN")
        if env_token:
            raw["github_token"] = env_token
    if raw.get("github_token") == "":
        raw["github_token"] = None
    if raw.get("github_client_id") == "":
        raw["github_client_id"] = None

    return AgentConfig.model_validate(raw)


def update_config_value(path: str | Path, key: str, value: str) -> None:
    cfg_path = _expand_path(path)
    text = cfg_path.read_text() if cfg_path.exists() else ""
    lines = text.splitlines()
    updated = False
    for idx, line in enumerate(lines):
        if re.match(rf"^\\s*{re.escape(key)}\\s*=", line):
            lines[idx] = f'{key} = \"{value}\"'
            updated = True
            break
    if not updated:
        if lines and lines[-1].strip() != "":
            lines.append("")
        lines.append(f'{key} = \"{value}\"')
    cfg_path.write_text("\n".join(lines) + "\n")
