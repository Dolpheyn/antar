"""Visual testing toolkit for documentation."""

import asyncio
import subprocess
import sys
import typer
from pathlib import Path
from typing import (
    Optional, 
    Dict, 
    Any, 
    Union,
    Protocol,
    runtime_checkable
)
from typing_extensions import TypeGuard
from playwright.async_api import async_playwright, Page
from scripts.core.console import console


def safe_get(
    d: Optional[Union[Dict[str, Any], Any]], 
    key: str, 
    default: Any = None
) -> Any:
    """
    Safely retrieve a value from a dictionary-like object, handling None and different object types.
    
    Args:
        d: Optional dictionary or object with .get() method
        key: Key to look up
        default: Default value if key is not found or object is None
    
    Returns:
        Value associated with key or default
    """
    # If d is None, return default
    if d is None:
        return default
    
    # If d is a dictionary, use standard dict.get()
    if isinstance(d, dict):
        return d.get(key, default)
    
    # If d has a .get() method (like Playwright's bounding_box()), use it
    if hasattr(d, 'get') and callable(d.get):
        return d.get(key, default)
    
    # If no matching method found, return default
    return default


def safe_evaluate(page: Page, script: str, default: Any = None) -> Any:
    """
    Safely evaluate a JavaScript script on a page.
    
    Args:
        page: Playwright Page object
        script: JavaScript script to evaluate
        default: Default value if evaluation fails
    
    Returns:
        Result of script evaluation or default
    """
    try:
        return page.evaluate(script)
    except Exception:
        return default


class VisualTester:
    """Visual testing toolkit for documentation."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.output_dir = Path(".cascade/visual-test")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.server_process = None

    async def setup(self) -> None:
        """Set up the testing environment."""
        console.print("[Visual Test] Building documentation site...")
        subprocess.check_call([sys.executable, "-m", "mkdocs", "build"])

        console.print("\n[Visual Test] Starting local server...")
        self.server_process = subprocess.Popen(
            [sys.executable, "-m", "http.server", "8000"],
            cwd="site",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    async def teardown(self) -> None:
        """Clean up the testing environment."""
        if self.server_process:
            console.print("\n[Visual Test] Shutting down server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()

    async def capture_page(self, page: Page, path: str, name: str) -> None:
        """Capture a full page screenshot."""
        url = f"{self.base_url}/{path}"
        try:
            await page.goto(url)
            await page.wait_for_load_state("networkidle")

            output_path = self.output_dir / f"{name}.png"
            await page.screenshot(path=str(output_path))
            console.print(f"✅ Captured {url} -> {output_path}")
        except Exception as e:
            console.print(f"❌ Error capturing {url}: {e}")

    async def test_navigation(self, page: Page) -> Dict[str, Any]:
        """
        Test navigation menu functionality with robust type handling.
        
        Args:
            page: Playwright Page object for testing
        
        Returns:
            Dictionary of navigation test results
        """
        await page.goto(self.base_url)
        await page.wait_for_selector(".md-nav--primary")

        nav = await page.query_selector(".md-nav--primary")
        nav_list = await page.query_selector(".md-nav--primary .md-nav__list")

        # Defensive checks with safe access
        nav_box = await nav.bounding_box() if nav else None
        list_box = await nav_list.bounding_box() if nav_list else None

        # Safe evaluation of JavaScript
        scroll_height = safe_evaluate(
            page, 
            """() => {
                const nav = document.querySelector('.md-nav--primary');
                return nav ? nav.scrollHeight - nav.clientHeight : 0;
            }"""
        )

        is_scrollable = safe_evaluate(
            page, 
            """() => {
                const nav = document.querySelector('.md-nav--primary');
                if (!nav) return false;
                const style = window.getComputedStyle(nav);
                return style.overflowY === 'auto' ||
                       style.overflowY === 'scroll';
            }"""
        )

        # Capture navigation screenshot with safe access
        nav_path = self.output_dir / "navigation.png"
        if nav and nav_box:
            await page.screenshot(
                path=str(nav_path),
                clip={
                    "x": safe_get(nav_box, "x", 0),
                    "y": safe_get(nav_box, "y", 0),
                    "width": safe_get(nav_box, "width", 0),
                    "height": safe_get(nav_box, "height", 0),
                },
            )
        else:
            console.print("⚠️ Could not capture navigation screenshot")
            nav_path = None

        return {
            "container_height": safe_get(nav_box, "height", 0),
            "list_height": safe_get(list_box, "height", 0),
            "scroll_height": scroll_height or 0,
            "is_scrollable": is_scrollable or False,
            "screenshot": nav_path,
        }


async def print_nav_results(results: Dict[str, Any]) -> None:
    """Print navigation test results."""
    console.print("\n📊 Navigation Menu Test Results:")
    console.print("-" * 40)
    console.print(f"Container height: {results['container_height']}px")
    console.print(f"List height: {results['list_height']}px")
    console.print(f"Scroll height: {results['scroll_height']}px")
    console.print(
        f"Scrolling enabled: {'✅' if results['is_scrollable'] else '❌'}")

    if results['list_height'] > results['container_height']:
        overflowAmount = results['list_height'] - results['container_height']
        console.print("\n⚠️  Issue: List is taller than container")
        console.print(f"Overflow: {overflowAmount}px")

    console.print(f"\n📸 Navigation screenshot: {results['screenshot']}")


VISUAL_HELP = """
Component to test ('nav' for navigation, 'pages' for full pages)
"""


def visual(
    output_dir: Path = typer.Option(
        Path(".cascade/visual-test"),
        "--output-dir",
        "-o",
        help="Output directory for screenshots",
    ),
    width: int = typer.Option(1280, "--width", help="Viewport width"),
    height: int = typer.Option(720, "--height", help="Viewport height"),
    component: Optional[str] = typer.Option(
        None,
        "--component",
        "-c",
        help=VISUAL_HELP,
    ),
) -> None:
    """Run visual tests on documentation.

    Args:
        output_dir: Directory to save screenshots.
        width: Viewport width for testing.
        height: Viewport height for testing.
        component: Specific component to test.
    """
    try:

        async def run_tests():
            tester = VisualTester()
            await tester.setup()

            try:
                async with async_playwright() as p:
                    browser = await p.chromium.launch()
                    page = await browser.new_page(
                        viewport={"width": width, "height": height}
                    )

                    if component in (None, "nav"):
                        nav_results = await tester.test_navigation(page)
                        await print_nav_results(nav_results)

                    if component in (None, "pages"):
                        console.print("\n📄 Capturing Pages:")
                        console.print("-" * 40)
                        pages = [
                            ("index.html", "home"),
                            (
                                "story-idea/delivery-aggregator/index.html",
                                "story",
                            ),
                            (
                                "story-idea/delivery-aggregator/"
                                "feature-concept.html",
                                "features",
                            ),
                            ("user-personas/index.html", "personas"),
                        ]
                        for path, name in pages:
                            await tester.capture_page(page, path, name)

                    await browser.close()
            finally:
                await tester.teardown()

            console.print("\n✨ Visual tests completed!")
            console.print(f"📁 Results saved in: {tester.output_dir}/")

        asyncio.run(run_tests())
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)
