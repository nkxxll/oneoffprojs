from __future__ import annotations

import warnings
warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality")

from pathlib import Path

import uvicorn
from fastapi import FastAPI

from noteweaver.logger import Logger
from noteweaver.server.config import DEFAULT_CONFIG_PATH, ServerConfig, load_config
from noteweaver.server.db import init_db
from noteweaver.server.indexer import index_directory, index_exists
from noteweaver.server.routes import router
from noteweaver.server.worker import start_worker

config: ServerConfig = ServerConfig()


def create_app(cfg: ServerConfig | None = None) -> FastAPI:
    global config
    config = cfg or config

    application = FastAPI(title="NoteWeaver", version="0.1.0")
    application.include_router(router)

    logger = Logger(
        name="noteweaver.server",
        to_stdout=False,
        file_path=config.log_file,
    ).get()

    @application.on_event("startup")
    def startup() -> None:
        init_db()
        logger.info("Server started (model=%s, log_file=%s)", config.model, config.log_file)
        if not index_exists(config.base_dir):
            logger.info("No existing index found, triggering initial indexing")
            index_directory(config.base_dir, config.embedding_model)
        start_worker(config.base_dir)

    return application


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="NoteWeaver server")
    parser.add_argument(
        "-c", "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help=f"Path to TOML config file (default: {DEFAULT_CONFIG_PATH})",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)
    init_db()
    create_app(cfg)
    uvicorn.run("noteweaver.server.app:app", host="0.0.0.0", port=8321, reload=True)


app = create_app()

if __name__ == "__main__":
    main()
