from __future__ import annotations

import warnings

warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality")

from typing import Annotated, Optional

import httpx
import typer
from rich.prompt import IntPrompt, Prompt

from noteweaver.cli import client
from noteweaver.cli.display import (
    console,
    print_error,
    print_success,
    print_task_action,
    print_task_table,
)
from noteweaver.models import TaskType

app = typer.Typer(
    name="nweaver", help="NoteWeaver CLI — manage your note processing queue."
)
task_app = typer.Typer(help="Manage tasks.")
queue_app = typer.Typer(help="Manage the processing queue.")
app.add_typer(task_app, name="task")
app.add_typer(queue_app, name="queue")


def _handle_request(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except httpx.ConnectError:
        print_error("Cannot connect to the server. Is nweaver-server running?")
        raise typer.Exit(1)
    except httpx.HTTPStatusError as e:
        detail = e.response.json().get("detail", str(e))
        print_error(detail)
        raise typer.Exit(1)


# ── Task commands ──────────────────────────────────────────────


@task_app.command("create")
def task_create(
    task_type: Annotated[
        Optional[str], typer.Option("--task", help="Task type: research, refine")
    ] = None,
    path: Annotated[
        Optional[str], typer.Option("--path", help="Path to the note file")
    ] = None,
    priority: Annotated[
        int, typer.Option("--prio", help="Priority (higher = more urgent)")
    ] = 1,
) -> None:
    """Create a new task. Runs interactively if --task and --path are omitted."""
    if task_type is None:
        task_type = Prompt.ask(
            "What do you want to do?",
            choices=[t.value for t in TaskType],
            default=TaskType.REFINE.value,
        )
    if path is None:
        path = Prompt.ask("Which file?")

    result = _handle_request(client.create_task, task_type, path, priority)
    print_task_action("CREATE", result)


@task_app.command("list")
def task_list() -> None:
    """List all tasks."""
    tasks = _handle_request(client.list_tasks)
    print_task_table(tasks)


@task_app.command("show")
def task_show(
    task_id: Annotated[int, typer.Argument(help="Task ID")],
) -> None:
    """Show details of a single task."""
    task = _handle_request(client.get_task, task_id)
    print_task_table([task], title=f"Task {task_id}")


@task_app.command("edit")
def task_edit(
    task_id: Annotated[int, typer.Argument(help="Task ID")],
    task_type: Annotated[
        Optional[str], typer.Option("--task", help="New task type")
    ] = None,
    path: Annotated[Optional[str], typer.Option("--path", help="New file path")] = None,
    priority: Annotated[
        Optional[int], typer.Option("--prio", help="New priority")
    ] = None,
) -> None:
    """Edit an existing task."""
    old = _handle_request(client.get_task, task_id)
    result = _handle_request(
        client.update_task, task_id, task_type=task_type, path=path, priority=priority
    )
    changes = []
    if task_type and old["task_type"] != result["task_type"]:
        changes.append(f"Task: {old['task_type']} → {result['task_type']}")
    if path and old["path"] != result["path"]:
        changes.append(f"Path: {old['path']} → {result['path']}")
    if priority is not None and old["priority"] != result["priority"]:
        changes.append(f"Prio: {old['priority']} → {result['priority']}")
    print_task_action("EDIT", result, extra=", ".join(changes) if changes else "")


@task_app.command("delete")
def task_delete(
    task_id: Annotated[int, typer.Argument(help="Task ID")],
) -> None:
    """Delete a task."""
    result = _handle_request(client.delete_task, task_id)
    print_task_action("DELETE", result)


# ── Queue commands ─────────────────────────────────────────────


@queue_app.command("show")
def queue_show() -> None:
    """Show queued and in-progress tasks."""
    tasks = _handle_request(client.get_queue)
    print_task_table(tasks, title="Queue")


@queue_app.command("empty")
def queue_empty() -> None:
    """Remove all queued and in-progress tasks."""
    result = _handle_request(client.empty_queue)
    removed = result["removed"]
    if removed == 0:
        print_success("[Q-EMPTY] The queue is already empty.")
    else:
        print_success(f"[Q-EMPTY] Removed {removed} task(s). The queue is empty now.")


if __name__ == "__main__":
    app()
