"""Command management for the project."""
from .base import register_command

# Import docs commands
from .docs import (
    serve,
    build,
    clean,
    render_diagrams,
    setup,
    visual
)

__all__ = [
    'register_command',
    # Docs commands
    'serve',
    'build',
    'clean',
    'render_diagrams',
    'setup',
    'visual'
]
