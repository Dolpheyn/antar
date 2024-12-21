"""Visual testing toolkit for documentation."""

import asyncio
import subprocess
import sys
import typer
from pathlib import Path
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Page
from scripts.core.cli import console


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
        """Test navigation menu functionality."""
        await page.goto(self.base_url)
        await page.wait_for_selector(".md-nav--primary")

        nav = await page.query_selector(".md-nav--primary")
        nav_list = await page.query_selector(".md-nav--primary .md-nav__list")

        if not nav or not nav_list:
            return {"error": "Navigation elements not found"}

        nav_box = await nav.bounding_box()
        list_box = await nav_list.bounding_box()

        scroll_height = await page.evaluate(
            """() => {
                const nav = document.querySelector('.md-nav--primary');
                return nav.scrollHeight - nav.clientHeight;
            }"""
        )

        is_scrollable = await page.evaluate(
            """() => {
                const nav = document.querySelector('.md-nav--primary');
                const style = window.getComputedStyle(nav);
                return style.overflowY === 'auto' ||
                       style.overflowY === 'scroll';
            }"""
        )

        # Capture navigation screenshot
        nav_path = self.output_dir / "navigation.png"
        await page.screenshot(
            path=str(nav_path),
            clip={
                "x": nav_box["x"],
                "y": nav_box["y"],
                "width": nav_box["width"],
                "height": nav_box["height"],
            },
        )

        return {
            "container_height": nav_box["height"],
            "list_height": list_box["height"],
            "scroll_height": scroll_height,
            "is_scrollable": is_scrollable,
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

    if results["list_height"] > results["container_height"]:
        overflowAmount = results["list_height"] - results["container_height"]
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
