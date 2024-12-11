"""Documentation related commands."""
from .base import register_docs_command
from .serve import serve
from .build import build
from .clean import clean
from .render import render_diagrams
from .setup import setup
from .test_visual import test_visual

__all__ = [
    'register_docs_command',
    'serve',
    'build',
    'clean',
    'render_diagrams',
    'setup',
    'test_visual'
]
