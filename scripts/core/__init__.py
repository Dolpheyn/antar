"""Core management functionality."""

from .console import console
from .cli import create_app

__all__ = ["create_app", "console"]
