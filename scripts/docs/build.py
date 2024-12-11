"""Documentation build command."""
import typer
from scripts.core.cli import console
from .clean import clean as clean_docs

def build(
    clean_first: bool = typer.Option(False, "--clean", help="Clean build directory first"),
):
    """Build the documentation site."""
    try:
        if clean_first:
            with console.status("[bold yellow]Cleaning previous build..."):
                clean_docs()
        
        with console.status("[bold green]Building documentation..."):
            # Import mkdocs and build site
            from mkdocs.commands.build import build as mkdocs_build
            mkdocs_build()
            console.print("[green]Documentation built successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)
