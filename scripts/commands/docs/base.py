"""Base functionality for documentation commands."""
from typing import Callable
from ...core.command import register_command

def register_docs_command(name: str, help_text: str = "") -> Callable:
    """Register a command under the docs group."""
    return register_command(f"docs {name}", help_text)
