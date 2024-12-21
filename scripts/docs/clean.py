"""Documentation clean command."""

import typer
import shutil
from pathlib import Path
from scripts.core.cli import console


def clean() -> None:
    """Clean built documentation."""

    try:
        with console.status("[bold yellow]Cleaning documentation build..."):
            # Remove site directory
            site_dir = Path("site")
            if site_dir.exists():
                shutil.rmtree(site_dir)
            console.print("[green]Documentation cleaned successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)
