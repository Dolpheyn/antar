"""Centralized console configuration for the project."""

from rich.console import Console

# Singleton-like console instance with consistent configuration
console = Console(
    color_system="auto",      # Adaptive color support
    force_terminal=False,     # Respect environment settings
    width=120,                # Consistent output width
    highlight=True,           # Enable syntax highlighting
    soft_wrap=True,           # Soft wrapping for long lines
)

# Optional: Add custom print methods if needed

def highlight(message: str) -> str:
    """Highlight a code block using Rich."""
    console.print(f"[bold green]{message}")


def print_success(message: str):
    """Print a success message."""
    console.print(f"[bold green]✓[/] {message}")


def print_error(message: str):
    """Print an error message."""
    console.print(f"[bold red]✗[/] {message}")


def print_warning(message: str):
    """Print a warning message."""
    console.print(f"[bold yellow]⚠[/] {message}")
