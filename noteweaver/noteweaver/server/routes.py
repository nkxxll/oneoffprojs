from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from noteweaver.models import (
    SearchRequest,
    SearchResult,
    Task,
    TaskCreate,
    TaskStatus,
    TaskType,
    TaskUpdate,
)
from noteweaver.server import db, indexer, worker

router = APIRouter()


@router.post("/tasks", status_code=201)
def create_task(data: TaskCreate) -> Task:
    task = db.create_task(data)
    worker.notify()
    return task


@router.get("/tasks")
def list_tasks() -> list[Task]:
    return db.list_tasks()


@router.get("/tasks/{task_id}")
def get_task(task_id: int) -> Task:
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@router.patch("/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate) -> Task:
    task = db.update_task(task_id, data)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> Task:
    task = db.delete_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@router.post("/search")
def search_notes(data: SearchRequest) -> list[SearchResult]:
    from noteweaver.server.app import config

    return indexer.search(
        data.query, config.base_dir, config.embedding_model, data.top_k
    )


@router.post("/index")
def reindex() -> dict[str, int]:
    from noteweaver.server.app import config

    count = indexer.index_directory(config.base_dir, config.embedding_model)
    return {"indexed_chunks": count}


@router.get("/queue")
def get_queue() -> list[Task]:
    return db.get_queue()


@router.post("/queue/empty")
def empty_queue() -> dict[str, int]:
    count = db.empty_queue()
    return {"removed": count}


class RefineRequest(BaseModel):
    path: str


@router.post("/refine", status_code=202)
def refine_note(data: RefineRequest) -> Task:
    from noteweaver.server.app import config

    base = Path(config.base_dir).expanduser().resolve()
    file_path = (base / data.path).resolve()
    if not file_path.is_relative_to(base):
        raise HTTPException(status_code=400, detail="Path must be inside base_dir")
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"File not found: {data.path}")

    task = db.create_task(TaskCreate(task_type=TaskType.REFINE, path=data.path))
    worker.notify()
    return task
