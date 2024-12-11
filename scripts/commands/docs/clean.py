"""Clean command for the documentation site."""
from typing import Optional, List
import shutil
from pathlib import Path

from .base import register_docs_command

@register_docs_command("clean", "Clean built documentation")
def clean(args: Optional[List[str]] = None) -> None:
    """Clean built documentation."""
    build_dir = Path("site")
    if build_dir.exists():
        shutil.rmtree(build_dir)
        print(f"Cleaned {build_dir}")

if __name__ == "__main__":
    clean()
