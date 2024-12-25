"""Documentation CLI application."""
import typer
import importlib

def safe_import(module_name, function_name):
    """Safely import a function from a module."""
    try:
        module = importlib.import_module(module_name)
        return getattr(module, function_name)
    except (ImportError, AttributeError) as e:
        print(f"Error: Unable to import {function_name} from {module_name}")
        print("Please install documentation dependencies:")
        print("Run: poetry install --no-root --with docs")
        raise typer.Exit(1)

# Create a separate Typer app for docs commands
docs_app = typer.Typer(
    name="docs",
    help="Documentation management tools",
    no_args_is_help=True,
)

@docs_app.command(name="serve")
def docs_serve():
    """Start documentation server."""
    serve = safe_import('scripts.docs', 'serve')
    serve()

@docs_app.command(name="build")
def docs_build():
    """Build documentation."""
    build = safe_import('scripts.docs', 'build')
    build()

@docs_app.command(name="clean")
def docs_clean():
    """Clean documentation artifacts."""
    clean = safe_import('scripts.docs', 'clean')
    clean()

@docs_app.command(name="render")
def docs_render():
    """Render diagrams."""
    render_diagrams = safe_import('scripts.docs', 'render_diagrams')
    render_diagrams()

@docs_app.command(name="setup")
def docs_setup():
    """Setup documentation environment."""
    setup = safe_import('scripts.docs', 'setup')
    setup()

@docs_app.command(name="visual")
def docs_visual():
    """Visualize documentation."""
    visual = safe_import('scripts.docs', 'visual')
    visual()
