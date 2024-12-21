"""Documentation serving command."""

import subprocess
import typer
from scripts.core.cli import console


def serve(
    port: int = typer.Option(8000, "--port", "-p",
                             help="Port to serve documentation"),
    live_reload: bool = typer.Option(
        True,
        "--live-reload/--no-live-reload",
        help="Enable/disable live reload",
    ),
) -> None:
    """Serve documentation locally.

    Args:
        port: Port number to serve documentation.
        live_reload: Whether to enable live reload.
    """
    try:
        with console.status("[bold green]Starting documentation server..."):
            cmd = ["mkdocs", "serve", f"--dev-addr=localhost:{port}"]

            if not live_reload:
                cmd.append("--no-reload")

            subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error serving documentation:[/red] {e}")
        raise typer.Exit(1)
