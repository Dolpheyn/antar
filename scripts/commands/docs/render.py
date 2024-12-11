"""Render command for documentation diagrams."""
from typing import Optional, List
import os
import subprocess
import sys
from pathlib import Path

from .base import register_docs_command

@register_docs_command("render", "Render all Mermaid diagrams")
def render_diagrams(args: Optional[List[str]] = None) -> None:
    """Render all Mermaid diagrams to images."""
    docs_dir = Path("docs")
    rendered_files = []

    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if "```mermaid" in content:
                            # Extract and render each Mermaid diagram
                            output_path = file_path.with_suffix('.mmd.png')
                            try:
                                subprocess.run([
                                    "npx", "@mermaid-js/mermaid-cli",
                                    "-i", str(file_path),
                                    "-o", str(output_path)
                                ], check=True)
                                rendered_files.append(output_path)
                            except subprocess.CalledProcessError as e:
                                print(f"Error rendering diagram in {file_path}: {e}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    if rendered_files:
        print("\nRendered diagrams:")
        for path in rendered_files:
            print(f"- {path}")
    else:
        print("No diagrams were rendered")

if __name__ == "__main__":
    render_diagrams()
