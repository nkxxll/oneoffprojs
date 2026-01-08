import argparse
import datetime
import os
import subprocess
import sys
import tempfile

import toml
from prompt_toolkit import prompt as tk_prompt
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, Window
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.widgets import Frame
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

editor = os.environ.get("EDITOR", "nvim")
console = Console()


def prompt(question, answers):
    """Interactive prompt with hjkl navigation"""
    if len(answers) == 0:
        return tk_prompt(f"[?] {question}: ")

    selected = [0]  # Use list to allow modification in nested function
    
    kb = KeyBindings()
    
    @kb.add('h')
    @kb.add('k')
    def _(event):
        selected[0] = (selected[0] - 1) % len(answers)
        _render()
    
    @kb.add('j')
    @kb.add('l')
    def _(event):
        selected[0] = (selected[0] + 1) % len(answers)
        _render()
    
    @kb.add('enter')
    @kb.add('c-c')
    def _(event):
        if event.data == '\r':  # Enter key
            event.app.exit(result=selected[0])
        else:  # Ctrl+C
            raise KeyboardInterrupt
    
    # Also allow number keys
    for i in range(len(answers)):
        @kb.add(str(i))
        def _(event, num=i):
            selected[0] = num
            _render()
    
    def _render():
        console.clear()
        console.print(f"\n[bold cyan]{question}[/bold cyan]")
        for idx, answer in enumerate(answers):
            marker = "▶ " if idx == selected[0] else "  "
            style = "bold cyan" if idx == selected[0] else ""
            console.print(f"{marker}{idx}: {answer}", style=style)
        console.print("\n[dim](hjkl/arrows/numbers to navigate, Enter to select)[/dim]")
    
    _render()
    
    app = Application(key_bindings=kb)
    try:
        result = app.run()
        return result if result is not None else selected[0]
    except KeyboardInterrupt:
        raise


def get_problems(path):
    with open(path, "r") as f:
        problems = toml.load(f)
    return problems


def get_problem_description(problems, number):
    return problems[number]["description"]


def start_kata(problems):
    """Select a problem to solve"""
    res = prompt(
        "Which problem do you want to try",
        [problem["name"] for problem in problems["problems"]],
    )
    res = int(res)
    description = get_problem_description(problems["problems"], res)
    
    # Show problem with nice formatting
    console.print(
        Panel(
            description,
            title="[bold cyan]Problem Description[/bold cyan]",
            border_style="cyan",
        )
    )

    ready = prompt("Are you ready?", ["yes", "no"])
    if ready == 1:
        ready = prompt("Sure?", ["yes", "no"])
        if ready == 1:
            console.print("[yellow]Cancelled![/yellow]")
            return start_kata(problems)
    return res


def start_problem(problem, inputs, outputs):
    """Start solving the problem"""
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w+") as f:
        path = f.name

        console.print(f"[cyan]Opening editor: {path}[/cyan]")
        start_time = datetime.datetime.now()
        subprocess.run([editor, path], check=True)
        end_time = datetime.datetime.now()

        # Create results table
        table = Table(title="Test Results", show_header=True, header_style="bold cyan")
        table.add_column("Test", style="cyan")
        table.add_column("Result", justify="left")

        passed = 0
        for index, (input_path, output_path) in enumerate(zip(inputs, outputs)):
            input_data = ""
            expected_output = ""
            with open(input_path, "r") as inp, open(output_path) as out:
                input_data = inp.read()
                expected_output = out.read()

            result = subprocess.run(
                [sys.executable, path],
                input=input_data,
                text=True,
                capture_output=True,
            )

            actual_output = result.stdout
            success = actual_output == expected_output
            if success:
                passed += 1
                table.add_row(f"Test {index + 1}", "[green]✓ Passed[/green]")
            else:
                table.add_row(
                    f"Test {index + 1}",
                    f"[red]✗ Failed[/red]\n[dim]Expected:[/dim] {expected_output[:50]}...\n[dim]Got:[/dim] {actual_output[:50]}...",
                )

        console.print(table)
        duration = end_time - start_time
        
        # Summary
        total = len(inputs)
        percentage = (passed / total * 100) if total > 0 else 0
        summary_color = "green" if passed == total else "yellow"
        console.print(
            f"\n[{summary_color}]Passed {passed}/{total} tests ({percentage:.0f}%) - Time: {duration}[/{summary_color}]"
        )


def main():
    parser = argparse.ArgumentParser(prog="ttykata")
    parser.add_argument("path", type=str, help="Path to problems TOML file")
    args = parser.parse_args()

    if args.path is None or not os.path.exists(args.path):
        console.print("[red]Error: You must provide a valid path to a TOML file![/red]")
        sys.exit(1)

    problems = get_problems(args.path)
    
    console.print(
        Panel(
            f"[bold]ttyKata[/bold] - {len(problems['problems'])} problems available",
            border_style="cyan",
        )
    )

    while True:
        try:
            problem_id = start_kata(problems)
            current = problems["problems"][problem_id]
            inputs = current["inputs"]
            outputs = current["outputs"]
            start_problem(current, inputs, outputs)
            
            again = prompt("\nSolve another problem?", ["yes", "no"])
            if again == 1:
                break
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break


if __name__ == "__main__":
    main()
