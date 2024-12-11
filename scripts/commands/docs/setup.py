"""Setup command for documentation dependencies."""
from typing import Optional, List
import subprocess
import sys

from .base import register_docs_command

@register_docs_command("setup", "Set up documentation dependencies")
def setup(args: Optional[List[str]] = None) -> None:
    """Set up documentation dependencies."""
    print("[Setup] Setting up documentation environment...")
    
    requirements = [
        "mkdocs-material",
        "mkdocs-mermaid2-plugin",
        "mkdocs-git-revision-date-plugin",
        "mkdocs-git-authors-plugin",
        "mkdocs-minify-plugin",
        "mkdocs-awesome-pages-plugin",
        "mkdocs-include-markdown-plugin",
        "playwright"
    ]
    
    print("[Setup] Installing dependencies...")
    for req in requirements:
        print(f"Installing {req}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", req])
    
    print("\n[Setup] Installing Playwright browsers...")
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    
    print("\n[Setup] Setup complete!")
    print("- Documentation is using Material theme with enhanced features")
    print("- Mermaid diagrams are supported in markdown")
    print("- Playwright is installed for visual testing")

if __name__ == "__main__":
    setup()
