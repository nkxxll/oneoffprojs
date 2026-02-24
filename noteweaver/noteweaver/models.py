from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class TaskType(StrEnum):
    RESEARCH = "research"
    REFINE = "refine"


class TaskStatus(StrEnum):
    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    FAILED = "FAILED"


class TaskCreate(BaseModel):
    task_type: TaskType = TaskType.REFINE
    path: str
    priority: int = Field(default=1, ge=1)


class TaskUpdate(BaseModel):
    task_type: TaskType | None = None
    path: str | None = None
    priority: int | None = Field(default=None, ge=1)
    status: TaskStatus | None = None


class Task(BaseModel):
    id: int
    task_type: TaskType
    path: str
    priority: int
    status: TaskStatus
    created_at: datetime


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchResult(BaseModel):
    path: str
    chunk: str
    score: float
