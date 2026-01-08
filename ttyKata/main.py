import argparse
import datetime
import os
import subprocess
import sys
import tempfile

import toml
from prompt_toolkit import prompt as tk_prompt
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

editor = os.environ.get("EDITOR", "nvim")
console = Console()

# Language registry: language → {extension, cmd, [compile, run]}
# compile/run support {input} and {output} placeholders for file paths
LANGUAGE_REGISTRY = {
    # Interpreted languages
    "python": {"ext": ".py", "cmd": "python3", "commentstr": "#"},
    "python2": {"ext": ".py", "cmd": "python2", "commentstr": "#"},
    "javascript": {"ext": ".js", "cmd": "node", "commentstr": "//"},
    "typescript": {"ext": ".ts", "cmd": "ts-node", "commentstr": "//"},
    "bash": {"ext": ".sh", "cmd": "bash", "commentstr": "#"},
    "ruby": {"ext": ".rb", "cmd": "ruby", "commentstr": "#"},
    # Compiled languages
    "c": {
        "ext": ".c",
        "compile": "gcc {input} -o {output}",
        "run": "{output}",
        "commentstr": "//",
    },
    "cpp": {
        "ext": ".cpp",
        "compile": "g++ {input} -o {output}",
        "run": "{output}",
        "commentstr": "//",
    },
    "go": {
        "ext": ".go",
        "compile": "go build -o {output} {input}",
        "run": "{output}",
        "commentstr": "//",
    },
    "rust": {
        "ext": ".rs",
        "compile": "rustc {input} -o {output}",
        "run": "{output}",
        "commentstr": "//",
    },
    "java": {
        "ext": ".java",
        "compile": "javac {input}",
        "run": "java -cp {output_dir} {class_name}",
        "commentstr": "//",
    },
}


def prompt(question, answers, default=None):
    """Prompt with simple number input"""
    if len(answers) == 0:
        return tk_prompt(f"[?] {question}: ")

    console.print(f"\n[bold cyan]{question}[/bold cyan]")
    for idx, answer in enumerate(answers):
        marker = " [bold green]✓[/bold green]" if idx == default else ""
        console.print(f"  {idx}: {answer}{marker}")

    while True:
        try:
            default_str = f" [{default}]" if default is not None else ""
            choice = tk_prompt(f"[?] Enter number{default_str}: ")

            # Use default if input is empty
            if choice == "" and default is not None:
                return default

            idx = int(choice)
            if 0 <= idx < len(answers):
                return idx
            else:
                console.print(
                    f"[yellow]Please enter a number between 0 and {len(answers) - 1}[/yellow]"
                )
        except ValueError:
            console.print("[yellow]Please enter a valid number[/yellow]")
        except KeyboardInterrupt:
            raise


def get_problems(path):
    with open(path, "r") as f:
        problems = toml.load(f)
    return problems


def get_problem_description(problems, number):
    return problems[number]["description"]


def get_language_config(language):
    """Get language configuration from registry"""
    if language not in LANGUAGE_REGISTRY:
        console.print(f"[red]Error: Language '{language}' not supported[/red]")
        sys.exit(1)
    return LANGUAGE_REGISTRY[language]


def start_kata(problems):
    """Select a problem to solve"""
    res = prompt(
        "Which problem do you want to try",
        [problem["name"] for problem in problems["problems"]],
    )
    res = int(res)
    current_problem = problems["problems"][res]
    description = get_problem_description(problems["problems"], res)
    language = current_problem.get("language", "python")

    console.clear()

    # Show problem with nice formatting
    console.print(
        Panel(
            description,
            title=f"[bold cyan]Problem Description ({language})[/bold cyan]",
            border_style="cyan",
        )
    )

    ready = prompt("Are you ready?", ["yes", "no"], default=0)
    if ready == 1:
        ready = prompt("Sure?", ["yes", "no"], default=0)
        if ready == 1:
            console.print("[yellow]Cancelled![/yellow]")
            return start_kata(problems)
    return res


def start_problem(problem):
    """Start solving the problem"""
    inputs = problem["inputs"]
    outputs = problem["outputs"]
    description = problem["description"]
    language = problem.get("language", "python")
    lang_config = get_language_config(language)
    suffix = lang_config["ext"]
    is_compiled = "compile" in lang_config

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False, mode="w+") as f:
        f.write(lang_config.commentstr + description)
        source_path = f.name

        console.print(f"[cyan]Opening editor: {source_path}[/cyan]")
        start_time = datetime.datetime.now()
        console.set_alt_screen(False)
        subprocess.run([editor, source_path], check=True)
        console.set_alt_screen(True)
        end_time = datetime.datetime.now()

        # Compile if needed
        binary_path = None
        if is_compiled:
            binary_path = source_path.rsplit(".", 1)[0]  # Remove extension
            compile_cmd = lang_config["compile"].format(
                input=source_path, output=binary_path
            )
            console.print(f"[cyan]Compiling: {compile_cmd}[/cyan]")
            result = subprocess.run(
                compile_cmd, shell=True, capture_output=True, text=True
            )
            if result.returncode != 0:
                console.print(f"[red]Compilation failed:[/red]\n{result.stderr}")
                return

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

            # Build command for this language
            if is_compiled:
                run_cmd = lang_config["run"].format(
                    output=binary_path,
                    output_dir=os.path.dirname(binary_path),
                    class_name=os.path.splitext(os.path.basename(source_path))[0],
                )
                cmd_list = run_cmd.split()
            else:
                cmd_list = [lang_config["cmd"], source_path]

            result = subprocess.run(
                cmd_list,
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

    console.set_alt_screen(True)
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
            start_problem(current)

            again = prompt("\nSolve another problem?", ["yes", "no"], default=1)
            if again == 1:
                console.set_alt_screen(False)
                break
        except KeyboardInterrupt:
            console.set_alt_screen(False)
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except Exception:
            console.set_alt_screen(False)
            console.print("\n[red]Unexpected failure![/red]")
            break


if __name__ == "__main__":
    main()
