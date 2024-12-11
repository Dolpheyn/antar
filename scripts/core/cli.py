"""Core CLI utilities and components."""
import typer
from rich.console import Console
from rich.table import Table
from typing import Optional, Callable

# Create shared console instance
console = Console()

def create_app(
    name: str,
    help_text: str,
    version: str = "1.0.0"
) -> typer.Typer:
    """Create a new Typer app with standard configuration.
    
    Args:
        name: Name of the app
        help_text: Help text for the app
        version: Version string
        
    Returns:
        Configured Typer app
    """
    app = typer.Typer(
        help=help_text,
        no_args_is_help=True,
        add_completion=False,
    )
    
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
        ),
    ):
        """Base callback with version option."""
        pass
    
    return app

def create_command_table(commands: dict) -> Table:
    """Create a Rich table displaying available commands.
    
    Args:
        commands: Dictionary of command name to help text
        
    Returns:
        Rich table for display
    """
    table = Table(title="Available Commands")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="green")
    
    for name, help_text in sorted(commands.items()):
        table.add_row(name, help_text)
    
    return table
