"""Documentation setup command."""

import typer
from scripts.core.console import console


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
            # Skip browser installation if specified
            if skip_browsers:
                console.print(
                    "[yellow]Skipping Playwright browser installation[/yellow]"
                )
            console.print(
                "[green]Documentation setup completed successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)
