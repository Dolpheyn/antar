#!/usr/bin/env python
"""
Command-line interface for project management.
"""
import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from typing import Optional
from pathlib import Path

from scripts.commands import (
    serve,
    build,
    clean,
    render_diagrams,
    setup,
    test_visual
)

# Create Typer app instances
app = typer.Typer(
    help="Project management CLI",
    no_args_is_help=True,
    add_completion=False,
)
docs_app = typer.Typer(help="Documentation management commands", no_args_is_help=True)
app.add_typer(docs_app, name="docs")

# Create Rich console
console = Console()

def version_callback(value: bool):
    """Show version information."""
    if value:
        console.print("Project CLI v1.0.0")
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
    """Project management CLI."""
    pass

@docs_app.command("serve")
def docs_serve(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind to"),
    dev_addr: str = typer.Option(None, "--dev-addr", help="Development server address (host:port)"),
):
    """Start the documentation development server."""
    try:
        with console.status("[bold green]Starting documentation server..."):
            serve([
                "--dev-addr", dev_addr or f"{host}:{port}",
                "--watch", "docs",
                "--watch", "mkdocs.yml",
                "--livereload"
            ])
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)

@docs_app.command("build")
def docs_build(
    clean_first: bool = typer.Option(False, "--clean", help="Clean build directory first"),
):
    """Build the documentation site."""
    try:
        if clean_first:
            with console.status("[bold yellow]Cleaning previous build..."):
                clean()
        
        with console.status("[bold green]Building documentation..."):
            build()
            console.print("[green]Documentation built successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)

@docs_app.command("clean")
def docs_clean():
    """Clean built documentation."""
    try:
        with console.status("[bold yellow]Cleaning documentation build..."):
            clean()
            console.print("[green]Documentation cleaned successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)

@docs_app.command("render")
def docs_render(
    output_dir: Path = typer.Option(
        Path("docs/diagrams"),
        "--output-dir",
        "-o",
        help="Output directory for rendered diagrams",
    ),
):
    """Render all Mermaid diagrams."""
    try:
        with console.status("[bold green]Rendering diagrams..."):
            render_diagrams()
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)

@docs_app.command("setup")
def docs_setup(
    skip_browsers: bool = typer.Option(
        False,
        "--skip-browsers",
        help="Skip installing Playwright browsers",
    ),
):
    """Set up documentation dependencies."""
    try:
        with console.status("[bold green]Setting up documentation environment..."):
            setup(["--skip-browsers"] if skip_browsers else None)
            console.print("[green]Documentation setup completed successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)

@docs_app.command("test-visual")
def docs_test_visual(
    output_dir: Path = typer.Option(
        Path(".cascade/visual-test"),
        "--output-dir",
        "-o",
        help="Output directory for screenshots",
    ),
    width: int = typer.Option(1280, "--width", help="Viewport width"),
    height: int = typer.Option(720, "--height", help="Viewport height"),
):
    """Run visual tests on documentation."""
    try:
        with console.status("[bold green]Running visual tests..."):
            test_visual([
                "--output-dir", str(output_dir),
                "--width", str(width),
                "--height", str(height)
            ])
            console.print("[green]Visual tests completed successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)

@docs_app.command("info")
def docs_info():
    """Show documentation tools information."""
    table = Table(title="Documentation Tools")
    table.add_column("Tool", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Description")

    # Add rows
    table.add_row(
        "MkDocs",
        "✓",
        "Documentation static site generator"
    )
    table.add_row(
        "Material Theme",
        "✓",
        "Beautiful documentation theme"
    )
    table.add_row(
        "Mermaid",
        "✓",
        "Diagram generation from markdown"
    )
    table.add_row(
        "Playwright",
        "✓",
        "Visual testing framework"
    )

    console.print(table)

if __name__ == "__main__":
    app()
