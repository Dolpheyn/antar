"""Documentation setup command."""

import typer
from scripts.core.console import console
import subprocess
import sys


def setup(
    skip_browsers: bool = typer.Option(
        False, "--skip-browsers", help="Skip installing Playwright browsers"
    )
) -> None:
    """Set up documentation dependencies.

    Args:
        skip_browsers: Whether to skip installing Playwright browsers.
    """
    try:
        with console.status(
            "[bold green]Setting up documentation environment...",
        ):
            # Install Playwright browsers
            if not skip_browsers:
                console.print(
                    "[green]Installing Playwright browsers...[/green]")
                subprocess.check_call(
                    [sys.executable, "-m", "playwright", "install"])
                console.print(
                    "[green]",
                    "Playwright browsers installed successfully!",
                    "[/green]",
                )
            else:
                console.print(
                    "[yellow]Skipping Playwright browser installation[/yellow]"
                )

            console.print(
                "[green]Documentation setup completed successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)


if __name__ == "__main__":
    typer.run(setup)
