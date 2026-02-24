from __future__ import annotations

import threading
from pathlib import Path

from noteweaver.logger import Logger
from noteweaver.models import TaskStatus, TaskUpdate
from noteweaver.refine import RefineNote
from noteweaver.server import db
from noteweaver.server.backup import backup_before_refine

logger = Logger(name="noteweaver.worker").get()

_task_available = threading.Event()


def notify() -> None:
    """Signal the worker that a new task has been enqueued."""
    _task_available.set()


def _process_one(base_dir: str) -> bool:
    """Claim and process the next queued task. Returns True if a task was processed."""
    task = db.claim_next_task()
    if task is None:
        return False

    logger.info("Processing task %d (%s) for %s", task.id, task.task_type, task.path)
    base = Path(base_dir).expanduser().resolve()
    file_path = (base / task.path).resolve()

    try:
        backup_before_refine(file_path, base_dir)
        refined = RefineNote.refine(str(file_path))
        file_path.write_text(refined)
        db.update_task(task.id, TaskUpdate(status=TaskStatus.DONE))
        logger.info("Task %d completed successfully", task.id)
    except Exception:
        db.update_task(task.id, TaskUpdate(status=TaskStatus.FAILED))
        logger.exception("Task %d failed", task.id)

    return True


def _run(base_dir: str, stop_event: threading.Event) -> None:
    logger.info("Queue worker started (push mode)")
    while not stop_event.is_set():
        # Process all available tasks before waiting
        processed = False
        try:
            while _process_one(base_dir):
                processed = True
                if stop_event.is_set():
                    return
        except Exception:
            logger.exception("Unexpected error in queue worker")

        # Only wait if we didn't process anything
        if not processed:
            _task_available.wait()
            if stop_event.is_set():
                break
            _task_available.clear()
    logger.info("Queue worker stopped")


def start_worker(base_dir: str) -> tuple[threading.Thread, threading.Event]:
    stop_event = threading.Event()
    thread = threading.Thread(
        target=_run,
        args=(base_dir, stop_event),
        daemon=True,
        name="noteweaver-queue-worker",
    )
    thread.start()
    return thread, stop_event
