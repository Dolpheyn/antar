"""Core CLI utilities and components."""

import typer
from rich.console import Console
from typing import Optional


def create_app(
    name: str,
    help_text: str,
    version: str = "1.0.0",
) -> typer.Typer:
    """Create a new Typer app with standard configuration.

    Args:
        name: Name of the app
        help_text: Help text for the app
        version: Version string

    Returns:
        Configured Typer app
    """
    console = Console()
    app = typer.Typer(help=help_text, no_args_is_help=True,
                      add_completion=False)

    def version_callback(value: bool):
        if value:
            console.print(f"{name} v{version}")
            raise typer.Exit()

    @app.callback()
    def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show version information.",
            callback=version_callback,
            is_eager=True,
        )
    ):
        """Base callback with version option."""
        pass

    return app
