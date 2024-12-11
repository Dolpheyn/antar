#!/usr/bin/env python
"""
Command-line interface for project management.

This is the main entry point for all project management commands. It provides
a clean interface to various tools and utilities organized by domain:

- docs: Documentation management (build, serve, test)
- [future domains will be added here]

Examples:
    # Start documentation server
    $ python 00.py docs serve

    # Build documentation
    $ python 00.py docs build

    # Show available commands
    $ python 00.py docs --help
"""
import typer
from scripts.core.cli import create_app, console
from scripts.docs import (
    build,
    serve,
    clean,
    render_diagrams,
    setup,
    visual
)

# Create main app
app = create_app(
    name="Project CLI",
    help_text="Project management tools",
)

# Create documentation app
docs = create_app(
    name="Documentation",
    help_text="Documentation management tools",
)

# Register documentation commands
docs.command()(serve)
docs.command()(build)
docs.command()(clean)
docs.command(name="render")(render_diagrams)
docs.command(name="setup")(setup)
docs.command(name="visual")(visual)

# Add documentation commands to main app
app.add_typer(docs, name="docs")

if __name__ == "__main__":
    app()
