"""Documentation server command."""
import typer
from typing import Optional, List
from scripts.core.cli import console

def serve(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind to"),
    dev_addr: str = typer.Option(None, "--dev-addr", help="Development server address (host:port)"),
):
    """Start the documentation development server."""
    try:
        with console.status("[bold green]Starting documentation server..."):
            # Build command arguments
            args = [
                "--dev-addr", dev_addr or f"{host}:{port}",
                "--watch", "docs",
                "--watch", "mkdocs.yml",
                "--livereload"
            ]
            
            # Import mkdocs and run server
            from mkdocs.commands.serve import serve as mkdocs_serve
            mkdocs_serve(args)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)
