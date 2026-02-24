from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "noteweaver"
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULTS = {
    "server_url": "http://localhost:8321",
}


@dataclass
class Config:
    server_url: str = DEFAULTS["server_url"]


def load_config() -> Config:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "rb") as f:
            data = tomllib.load(f)
        return Config(server_url=data.get("server_url", DEFAULTS["server_url"]))
    return Config()
