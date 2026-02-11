from __future__ import annotations

from pathlib import Path
import logging
import typer

from githubkit import GitHub, OAuthDeviceAuthStrategy

from .config import load_config, update_config_value
from .orchestrator import Orchestrator


app = typer.Typer(add_completion=False, help="Research agent (Ollama).", invoke_without_command=True)


@app.command()
def run(
    query: str = typer.Argument(..., help="Research question or task"),
    config: Path = typer.Option(Path("config.toml"), help="Path to config.toml"),
    run_name: str | None = typer.Option(None, help="Override run name"),
    output_dir: Path | None = typer.Option(None, help="Override output directory"),
    skip_github: bool = typer.Option(False, help="Skip GitHub repo fetch; read README only"),
    log_level: str = typer.Option("INFO", help="Log level (DEBUG, INFO, WARNING, ERROR)"),
) -> None:
    logging.basicConfig(level=getattr(logging, log_level.upper(), logging.INFO))
    cfg = load_config(config)
    if output_dir is not None:
        cfg.output_dir = output_dir.expanduser().resolve()
    cfg.skip_github = skip_github

    orchestrator = Orchestrator(cfg)
    run_dir = orchestrator.run(query, run_name=run_name)
    typer.echo(f"Run complete. Output: {run_dir}")


@app.command("auth-github")
def auth_github(
    config: Path = typer.Option(Path("config.toml"), help="Path to config.toml"),
    client_id: str | None = typer.Option(None, help="GitHub OAuth App client ID"),
    scope: list[str] = typer.Option([], "--scope", help="OAuth scopes (repeatable)"),
) -> None:
    cfg = load_config(config)
    resolved_client_id = client_id or cfg.github_client_id
    if not resolved_client_id:
        resolved_client_id = typer.prompt("GitHub OAuth App client ID")

    scopes = scope or ["public_repo"]

    def _on_verification(data: dict) -> None:
        verification_uri = data.get("verification_uri")
        user_code = data.get("user_code")
        typer.echo("")
        typer.echo("GitHub device authorization required.")
        typer.echo(f"Visit: {verification_uri}")
        typer.echo(f"Enter code: {user_code}")
        typer.echo("")

    gh = GitHub()
    auth = OAuthDeviceAuthStrategy(resolved_client_id, _on_verification, scopes=scopes)
    auth.exchange_token(gh)
    token = auth.token

    update_config_value(config, "github_client_id", resolved_client_id)
    update_config_value(config, "github_token", token)

    typer.echo("GitHub OAuth token saved to config.")


@app.callback()
def main_callback(
    query: str | None = typer.Argument(None, help="Research question or task"),
    config: Path = typer.Option(Path("config.toml"), help="Path to config.toml"),
    run_name: str | None = typer.Option(None, help="Override run name"),
    output_dir: Path | None = typer.Option(None, help="Override output directory"),
    skip_github: bool = typer.Option(False, help="Skip GitHub repo fetch; read README only"),
    log_level: str = typer.Option("INFO", help="Log level (DEBUG, INFO, WARNING, ERROR)"),
) -> None:
    if query is None:
        return
    run(
        query=query,
        config=config,
        run_name=run_name,
        output_dir=output_dir,
        skip_github=skip_github,
        log_level=log_level,
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
