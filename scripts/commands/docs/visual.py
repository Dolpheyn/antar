"""Visual testing toolkit for documentation."""
import asyncio
import subprocess
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from playwright.async_api import async_playwright, Page

from .base import register_docs_command

class VisualTester:
    """Visual testing toolkit for documentation."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.output_dir = Path(".cascade/visual-test")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.server_process = None
    
    async def setup(self) -> None:
        """Set up the testing environment."""
        print("[Visual Test] Building documentation site...")
        subprocess.check_call([sys.executable, "-m", "mkdocs", "build"])
        
        print("\n[Visual Test] Starting local server...")
        self.server_process = subprocess.Popen(
            [sys.executable, "-m", "http.server", "8000"],
            cwd="site",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    async def teardown(self) -> None:
        """Clean up the testing environment."""
        if self.server_process:
            print("\n[Visual Test] Shutting down server...")
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
            print(f"✅ Captured {url} -> {output_path}")
        except Exception as e:
            print(f"❌ Error capturing {url}: {e}")
    
    async def test_navigation(self, page: Page) -> Dict[str, Any]:
        """Test navigation menu functionality."""
        await page.goto(self.base_url)
        await page.wait_for_selector('.md-nav--primary')
        
        nav = await page.query_selector('.md-nav--primary')
        nav_list = await page.query_selector('.md-nav--primary .md-nav__list')
        
        if not nav or not nav_list:
            return {"error": "Navigation elements not found"}
        
        nav_box = await nav.bounding_box()
        list_box = await nav_list.bounding_box()
        
        scroll_height = await page.evaluate('''() => {
            const nav = document.querySelector('.md-nav--primary');
            return nav.scrollHeight - nav.clientHeight;
        }''')
        
        is_scrollable = await page.evaluate('''() => {
            const nav = document.querySelector('.md-nav--primary');
            const style = window.getComputedStyle(nav);
            return style.overflowY === 'auto' || style.overflowY === 'scroll';
        }''')
        
        # Capture navigation screenshot
        nav_path = self.output_dir / "navigation.png"
        await page.screenshot(
            path=str(nav_path),
            clip={
                'x': nav_box['x'],
                'y': nav_box['y'],
                'width': nav_box['width'],
                'height': nav_box['height']
            }
        )
        
        return {
            "container_height": nav_box['height'],
            "list_height": list_box['height'],
            "scroll_height": scroll_height,
            "is_scrollable": is_scrollable,
            "screenshot": nav_path
        }

async def print_nav_results(results: Dict[str, Any]) -> None:
    """Print navigation test results."""
    print("\n📊 Navigation Menu Test Results:")
    print("-" * 40)
    print(f"Container height: {results['container_height']}px")
    print(f"List height: {results['list_height']}px")
    print(f"Scroll height: {results['scroll_height']}px")
    print(f"Scrolling enabled: {'✅' if results['is_scrollable'] else '❌'}")
    
    if results['list_height'] > results['container_height']:
        print("\n⚠️  Issue: List is taller than container")
        print(f"Overflow: {results['list_height'] - results['container_height']}px")
    
    print(f"\n📸 Navigation screenshot: {results['screenshot']}")

@register_docs_command("visual", "Visual testing toolkit for documentation")
async def visual(ctx, component: Optional[str] = None) -> None:
    """Run visual tests on documentation.
    
    Args:
        component: Component to test ('nav' for navigation, 'pages' for full pages,
                 or None for all tests)
    """
    tester = VisualTester()
    await tester.setup()
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={"width": 1280, "height": 720})
            
            if component in (None, "nav"):
                nav_results = await tester.test_navigation(page)
                await print_nav_results(nav_results)
            
            if component in (None, "pages"):
                print("\n📄 Capturing Pages:")
                print("-" * 40)
                pages = [
                    ("index.html", "home"),
                    ("story-idea/delivery-aggregator/index.html", "story"),
                    ("story-idea/delivery-aggregator/feature-concept.html", "features"),
                    ("user-personas/index.html", "personas")
                ]
                for path, name in pages:
                    await tester.capture_page(page, path, name)
            
            await browser.close()
    finally:
        await tester.teardown()
    
    print("\n✨ Visual tests completed!")
    print(f"📁 Results saved in: {tester.output_dir}/")

if __name__ == "__main__":
    asyncio.run(visual(None))
