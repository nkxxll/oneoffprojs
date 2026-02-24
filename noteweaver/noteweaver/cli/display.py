from __future__ import annotations

from rich.console import Console
from rich.table import Table

console = Console()

STATUS_COLORS = {
    "QUEUED": "yellow",
    "IN_PROGRESS": "cyan",
    "DONE": "green",
    "FAILED": "red",
}


def print_task_action(action: str, task: dict, extra: str = "") -> None:
    color = {"CREATE": "green", "DELETE": "red", "EDIT": "blue"}.get(action, "white")
    status_color = STATUS_COLORS.get(task.get("status", ""), "white")
    msg = (
        f"[bold {color}][{action}][/] "
        f"ID: {task['id']}  "
        f"Task: {task['task_type']}  "
        f"Path: {task['path']}  "
        f"Prio: {task['priority']}  "
        f"Status: [{status_color}]{task.get('status', '')}[/]"
    )
    if extra:
        msg += f"  {extra}"
    console.print(msg)


def print_task_table(tasks: list[dict], title: str = "Tasks") -> None:
    if not tasks:
        console.print(f"[dim]No tasks to show.[/]")
        return
    table = Table(title=title, show_lines=False)
    table.add_column("ID", style="bold", justify="right")
    table.add_column("Task", style="magenta")
    table.add_column("Path")
    table.add_column("Prio", justify="right")
    table.add_column("Status")
    table.add_column("Created")

    for t in tasks:
        status = t["status"]
        color = STATUS_COLORS.get(status, "white")
        table.add_row(
            str(t["id"]),
            t["task_type"],
            t["path"],
            str(t["priority"]),
            f"[{color}]{status}[/]",
            t.get("created_at", "")[:19],
        )
    console.print(table)


def print_error(msg: str) -> None:
    console.print(f"[bold red]Error:[/] {msg}")


def print_success(msg: str) -> None:
    console.print(f"[bold green]{msg}[/]")
