from __future__ import annotations

import httpx

from noteweaver.cli.config import load_config

_config = load_config()


def _url(path: str) -> str:
    return f"{_config.server_url}{path}"


def create_task(task_type: str, path: str, priority: int = 1) -> dict:
    r = httpx.post(_url("/tasks"), json={"task_type": task_type, "path": path, "priority": priority})
    r.raise_for_status()
    return r.json()


def list_tasks() -> list[dict]:
    r = httpx.get(_url("/tasks"))
    r.raise_for_status()
    return r.json()


def get_task(task_id: int) -> dict:
    r = httpx.get(_url(f"/tasks/{task_id}"))
    r.raise_for_status()
    return r.json()


def update_task(task_id: int, **fields: object) -> dict:
    payload = {k: v for k, v in fields.items() if v is not None}
    r = httpx.patch(_url(f"/tasks/{task_id}"), json=payload)
    r.raise_for_status()
    return r.json()


def delete_task(task_id: int) -> dict:
    r = httpx.delete(_url(f"/tasks/{task_id}"))
    r.raise_for_status()
    return r.json()


def get_queue() -> list[dict]:
    r = httpx.get(_url("/queue"))
    r.raise_for_status()
    return r.json()


def empty_queue() -> dict:
    r = httpx.post(_url("/queue/empty"))
    r.raise_for_status()
    return r.json()
