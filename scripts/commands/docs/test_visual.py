"""Visual testing command for documentation."""
from typing import Optional, List
import os
import subprocess
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

from .base import register_docs_command

def ensure_dir(path: Path) -> None:
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)

def capture_page(page, url: str, output_path: Path) -> None:
    """Capture a page screenshot."""
    try:
        page.goto(url)
        page.wait_for_load_state("networkidle")
        page.screenshot(path=str(output_path))
        print(f"Captured {url} -> {output_path}")
    except Exception as e:
        print(f"Error capturing {url}: {e}")

@register_docs_command("test-visual", "Run visual tests on documentation")
def test_visual(args: Optional[List[str]] = None) -> None:
    """Run visual tests on the documentation site."""
    print("[Visual Test] Building documentation site...")
    subprocess.check_call([sys.executable, "-m", "mkdocs", "build"])
    
    print("\n[Visual Test] Starting local server...")
    server_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8000"],
        cwd="site",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        output_dir = Path(".cascade/visual-test")
        ensure_dir(output_dir)
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            
            # Capture main pages
            pages = [
                "index.html",
                "story-idea/index.html",
                "feature-concept/index.html",
                "technical-specifications/index.html"
            ]
            
            for page_path in pages:
                url = f"http://localhost:8000/{page_path}"
                output_path = output_dir / f"{page_path.replace('/', '_')}.png"
                capture_page(page, url, output_path)
            
            browser.close()
    finally:
        print("\n[Visual Test] Shutting down server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
    
    print("\n[Visual Test] Done! Screenshots saved in .cascade/visual-test/")
    print("You can now check the rendered pages and diagrams.")

if __name__ == "__main__":
    test_visual()
