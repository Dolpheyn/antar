"""Documentation serving command."""

import subprocess
import typer
from scripts.core.console import console


def serve() -> None:
    """Serve documentation locally.
    """
    try:
        with console.status("[bold green]Starting documentation server..."):
            subprocess.check_call(["mkdocs", "serve"])
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error serving documentation:[/red] {e}")
        raise typer.Exit(1)
