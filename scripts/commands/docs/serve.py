"""Serve command for the documentation site."""
from typing import Optional, List
import subprocess
import sys

from .base import register_docs_command

@register_docs_command("serve", "Start the documentation development server")
def serve(args: Optional[List[str]] = None) -> None:
    """Start the development server."""
    try:
        subprocess.check_call([
            sys.executable, "-m", "mkdocs", "serve",
            "--dev-addr", "127.0.0.1:8000",  # Explicit host and port
            "--watch", "docs",  # Watch docs directory
            "--watch", "mkdocs.yml",  # Watch config file
            "--livereload"  # Enable live reload
        ])
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        print("Make sure all dependencies are installed with: python manage.py docs setup")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")

if __name__ == "__main__":
    serve()
