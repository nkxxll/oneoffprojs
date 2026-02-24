from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from noteweaver.models import Task, TaskCreate, TaskStatus, TaskType, TaskUpdate

DEFAULT_DB_PATH = Path("noteweaver_queue.db")


def _connect(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db(db_path: Path = DEFAULT_DB_PATH) -> None:
    conn = _connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_type TEXT NOT NULL,
            path TEXT NOT NULL,
            priority INTEGER NOT NULL DEFAULT 1,
            status TEXT NOT NULL DEFAULT 'QUEUED',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def _row_to_task(row: sqlite3.Row) -> Task:
    return Task(
        id=row["id"],
        task_type=TaskType(row["task_type"]),
        path=row["path"],
        priority=row["priority"],
        status=TaskStatus(row["status"]),
        created_at=datetime.fromisoformat(row["created_at"]),
    )


def create_task(data: TaskCreate, db_path: Path = DEFAULT_DB_PATH) -> Task:
    conn = _connect(db_path)
    now = datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
        "INSERT INTO tasks (task_type, path, priority, status, created_at) VALUES (?, ?, ?, ?, ?)",
        (data.task_type.value, data.path, data.priority, TaskStatus.QUEUED.value, now),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return _row_to_task(row)


def get_task(task_id: int, db_path: Path = DEFAULT_DB_PATH) -> Task | None:
    conn = _connect(db_path)
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return _row_to_task(row) if row else None


def list_tasks(db_path: Path = DEFAULT_DB_PATH) -> list[Task]:
    conn = _connect(db_path)
    rows = conn.execute("SELECT * FROM tasks ORDER BY priority DESC, created_at ASC").fetchall()
    conn.close()
    return [_row_to_task(r) for r in rows]


def update_task(task_id: int, data: TaskUpdate, db_path: Path = DEFAULT_DB_PATH) -> Task | None:
    existing = get_task(task_id, db_path)
    if existing is None:
        return None

    updates: list[str] = []
    values: list[object] = []
    if data.task_type is not None:
        updates.append("task_type = ?")
        values.append(data.task_type.value)
    if data.path is not None:
        updates.append("path = ?")
        values.append(data.path)
    if data.priority is not None:
        updates.append("priority = ?")
        values.append(data.priority)
    if data.status is not None:
        updates.append("status = ?")
        values.append(data.status.value)

    if not updates:
        return existing

    values.append(task_id)
    conn = _connect(db_path)
    conn.execute(f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?", values)
    conn.commit()
    conn.close()
    return get_task(task_id, db_path)


def delete_task(task_id: int, db_path: Path = DEFAULT_DB_PATH) -> Task | None:
    task = get_task(task_id, db_path)
    if task is None:
        return None
    conn = _connect(db_path)
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return task


def get_queue(db_path: Path = DEFAULT_DB_PATH) -> list[Task]:
    conn = _connect(db_path)
    rows = conn.execute(
        "SELECT * FROM tasks WHERE status IN (?, ?) ORDER BY priority DESC, created_at ASC",
        (TaskStatus.QUEUED.value, TaskStatus.IN_PROGRESS.value),
    ).fetchall()
    conn.close()
    return [_row_to_task(r) for r in rows]


def claim_next_task(db_path: Path = DEFAULT_DB_PATH) -> Task | None:
    conn = _connect(db_path)
    # Pick up tasks already marked IN_PROGRESS (pre-claimed by the route) first,
    # then fall back to the next QUEUED task.
    row = conn.execute(
        "SELECT * FROM tasks WHERE status IN (?, ?) "
        "ORDER BY CASE status WHEN ? THEN 0 ELSE 1 END, priority DESC, created_at ASC LIMIT 1",
        (TaskStatus.IN_PROGRESS.value, TaskStatus.QUEUED.value, TaskStatus.IN_PROGRESS.value),
    ).fetchone()
    if row is None:
        conn.close()
        return None
    if row["status"] == TaskStatus.QUEUED.value:
        conn.execute(
            "UPDATE tasks SET status = ? WHERE id = ?",
            (TaskStatus.IN_PROGRESS.value, row["id"]),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (row["id"],)).fetchone()
    conn.close()
    return _row_to_task(row)


def empty_queue(db_path: Path = DEFAULT_DB_PATH) -> int:
    conn = _connect(db_path)
    cur = conn.execute(
        "DELETE FROM tasks WHERE status IN (?, ?)",
        (TaskStatus.QUEUED.value, TaskStatus.IN_PROGRESS.value),
    )
    conn.commit()
    count = cur.rowcount
    conn.close()
    return count
