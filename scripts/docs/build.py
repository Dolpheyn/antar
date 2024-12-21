"""Documentation build command."""

import typer
from typing import Optional, Any
from pathlib import Path
from scripts.core.console import console
from .clean import clean


def validate_output_path(path: Optional[str]) -> Path:
    """
    Validate and convert output path to Path, with sensible defaults.

    Args:
        path: Optional output path string

    Returns:
        Validated Path object for documentation output

    Raises:
        typer.BadParameter: If path is invalid
    """
    if path is None:
        return Path("site")

    try:
        output_dir = Path(path).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    except (TypeError, ValueError) as e:
        raise typer.BadParameter(f"Invalid output path: {e}")


def build(
    clean_first: bool = typer.Option(
        False, "--clean", help="Clean build directory first"
    ),
    output_dir: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Custom output directory for documentation"
    ),
    config_file: Optional[str] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to custom MkDocs configuration file"
    )
) -> None:
    """Build the documentation site with enhanced configuration options.

    Args:
        clean_first: Whether to clean the build directory first.
        output_dir: Optional custom output directory.
        config_file: Optional path to custom MkDocs configuration file.
    """
    try:
        # Validate and prepare output directory
        site_dir = validate_output_path(output_dir)

        # Clean build directory if requested
        if clean_first:
            with console.status("[bold yellow]Cleaning previous build..."):
                clean()

        with console.status("[bold green]Building documentation..."):
            # Import mkdocs dynamically to handle potential import errors
            try:
                from mkdocs.commands.build import build as mkdocs_build
            except ImportError as import_err:
                console.print(f"[red]MkDocs import error: {import_err}[/red]")
                raise typer.Exit(1)

            # Prepare MkDocs configuration
            config_kwargs: dict[str, Any] = {}

            # Add custom config file if provided
            if config_file:
                config_kwargs['config_file'] = config_file

            # Add custom site directory
            config_kwargs['site_dir'] = str(site_dir)

            # Build documentation
            try:
                mkdocs_build(**config_kwargs)
                console.print(
                    f"[green]Documentation built successfully in "
                    f"{site_dir}![/green]"
                )
            except Exception as build_err:
                console.print(f"[red]MkDocs build error: {build_err}[/red]")
                raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {str(e)}")
        raise typer.Exit(1)


if __name__ == "__main__":
    typer.run(build)
