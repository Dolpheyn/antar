"""Build command for the documentation site."""
from typing import Optional, List
import sys

from .base import register_docs_command
from ...core.command import run_python_module

@register_docs_command("build", "Build the documentation site")
def build(args: Optional[List[str]] = None) -> None:
    """Build the documentation site."""
    run_python_module("mkdocs", "build")

if __name__ == "__main__":
    build()
