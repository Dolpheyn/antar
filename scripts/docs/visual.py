import asyncio
import subprocess
import typer
from pathlib import Path
from typing import (
    List,
    Tuple,
    Optional,
    Dict,
    Callable,
    Any,
)
from enum import Enum, auto
from playwright.async_api import async_playwright
from scripts.core.console import console
import yaml
import os

from dataclasses import dataclass, field


class CaptureStatus(Enum):
    """Enum representing the status of a page capture attempt."""

    PENDING = auto()
    SUCCESS = auto()
    TIMEOUT = auto()
    NETWORK_ERROR = auto()
    BROWSER_ERROR = auto()
    FILE_NOT_FOUND = auto()
    FAILED = auto()


@dataclass
class CaptureResult:
    """Detailed result of a page capture attempt."""

    page_name: str
    page_path: str
    status: CaptureStatus = CaptureStatus.PENDING
    screenshot_path: Optional[str] = None
    error_message: Optional[str] = None
    attempt_count: int = 0
    capture_duration: float = 0.0


@dataclass
class VisualTestReport:
    """Comprehensive report of visual testing process."""

    total_pages: int = 0
    successful_captures: int = 0
    failed_captures: int = 0
    capture_results: List[CaptureResult] = field(default_factory=list)
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    def add_result(self, result: CaptureResult):
        """Add a capture result to the report."""
        self.capture_results.append(result)
        if result.status == CaptureStatus.SUCCESS:
            self.successful_captures += 1
        else:
            self.failed_captures += 1

    def generate_summary(self) -> Dict[str, Any]:
        """Generate a summary of the test report."""
        return {
            "total_pages": self.total_pages,
            "successful_captures": self.successful_captures,
            "failed_captures": self.failed_captures,
            "success_rate": (
                self.successful_captures / self.total_pages * 100
                if self.total_pages > 0
                else 0
            ),
            "failed_pages": [
                result.page_name
                for result in self.capture_results
                if result.status != CaptureStatus.SUCCESS
            ],
        }


class AdvancedVisualTester:
    """Enhanced visual testing toolkit with advanced error handling."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        max_concurrent_captures: int = 5,
        global_timeout: float = 30.0,
        retry_strategy: Optional[Callable[[int], float]] = None,
        viewport_width: int = 1280,
        viewport_height: int = 720,
    ):
        """
        Initialize the advanced visual tester.

        Args:
            base_url: Base URL for documentation site
            max_concurrent_captures: Maximum number of concurrent page captures
            global_timeout: Global timeout for entire capture process
            retry_strategy: Custom retry delay calculation function
            viewport_width: Viewport width
            viewport_height: Viewport height
        """
        self.base_url = base_url
        self.max_concurrent_captures = max_concurrent_captures
        self.global_timeout = global_timeout
        self.retry_strategy = retry_strategy or self._default_retry_strategy
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

        self.output_dir = Path(".cascade/visual-test")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _default_retry_strategy(self, attempt: int) -> float:
        """
        Simple linear retry strategy with minimal delay.

        Args:
            attempt: Current retry attempt number

        Returns:
            Delay in seconds before next retry
        """
        return 1.0  # Constant 1-second delay

    async def create_browser_context(
        self,
        browser,
        viewport: Dict[str, int] = {"width": 1280, "height": 720},
    ):
        """
        Create a robust browser context with enhanced configuration.

        Args:
            browser: Playwright browser instance
            viewport: Viewport dimensions

        Returns:
            Browser context or None if creation fails
        """
        try:
            context = await browser.new_context(
                viewport=viewport,
                accept_downloads=False,
                bypass_csp=True,
            )
            return context
        except Exception as e:
            console.print(f"❌ Browser context creation failed: {e}")
            return None

    async def capture_screenshot_from_mkdocs_build(
        self, page_path: str, page_name: Optional[str] = None
    ) -> CaptureResult:
        """
        Capture a screenshot of a specific page from the MkDocs build.

        Args:
            page_path (str): Relative path to the HTML file
            page_name (Optional[str]): Optional name for the page

        Returns:
            CaptureResult: Result of the screenshot capture attempt
        """
        # Construct absolute file path
        absolute_site_path = os.path.abspath(os.path.join("site", page_path))

        try:
            # Create a new browser context and page
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    viewport={
                        "width": self.viewport_width,
                        "height": self.viewport_height,
                    }
                )
                page = await context.new_page()

                # Navigate to the page using absolute file path
                await page.goto(
                    f"file://{absolute_site_path}",
                    wait_until="load",
                )

                # Ensure output directory exists
                output_dir = Path(".cascade/visual-test") / \
                    os.path.dirname(page_path)
                output_dir.mkdir(parents=True, exist_ok=True)

                # Generate screenshot filename
                screenshot_filename = output_dir / \
                    f"{os.path.basename(page_path)}.png"

                # Capture screenshot
                await page.screenshot(
                    path=str(screenshot_filename),
                    full_page=True,
                    timeout=30000,
                )

                # Close browser context
                await context.close()

                # Return successful capture result
                return CaptureResult(
                    page_path=page_path,
                    page_name=page_name or page_path,
                    screenshot_path=str(screenshot_filename),
                    status=CaptureStatus.SUCCESS,
                )

        except Exception as e:
            # Log and return failure result
            console.print(f"❌ Failed to capture {page_path}: {str(e)}")
            return CaptureResult(
                page_path=page_path,
                page_name=page_name or page_path,
                screenshot_path=None,
                status=CaptureStatus.FAILED,
                error_message=str(e),
            )

    def _normalize_page_path(self, page_path: str) -> str:
        """
        Convert source path to MkDocs generated HTML path.

        Handles various input scenarios:
        - Markdown files (.md)
        - HTML files (.html)
        - Paths with or without extensions
        - Directory and file paths

        Args:
            page_path (str): Original page path

        Returns:
            str: Normalized HTML file path relative to site directory
        """
        # Remove leading site/ or docs/ if present
        page_path = page_path.replace("site/", "").replace("docs/", "")

        # Handle .md to .html conversion if needed
        if page_path.endswith(".md"):
            page_path = page_path[:-3] + ".html"
        elif not page_path.endswith(".html"):
            page_path += ".html"

        # Ensure index.html for directory-like paths
        if page_path.endswith("/"):
            page_path += "index.html"

        return page_path

    async def capture_site_screenshots(
        self,
        site_directory: str = "site/",
        output_directory: str = ".cascade/visual-test",
        max_concurrent: int = 10,
        exclude_dirs: Optional[List[str]] = None,
    ) -> List[CaptureResult]:
        """
        Capture screenshots for all HTML files in the site directory.

        Implements parallel processing with semaphore-based concurrency.

        Args:
            site_directory (str): Root directory to start screenshot capture
            output_directory (str): Directory to save screenshots
            max_concurrent (int): Maximum concurrent browser instances
            exclude_dirs (List[str]): Directories to exclude from processing

        Returns:
            List[CaptureResult]: Capture results for all processed HTML files
        """
        # Ensure output directory exists
        os.makedirs(output_directory, exist_ok=True)

        # Default exclusion list
        if exclude_dirs is None:
            exclude_dirs = ["assets", ".git", ".cascade", "search"]

        # Ensure absolute path for site directory
        site_directory = os.path.abspath(site_directory)

        html_files = []
        for root, _, files in os.walk(site_directory):
            for file in files:
                if file.endswith(".html"):
                    full_path = os.path.abspath(os.path.join(root, file))
                    relative_path = os.path.relpath(full_path, site_directory)

                    # Skip excluded directories
                    if any(ex_dir in relative_path for ex_dir in exclude_dirs):
                        console.print(f"⏩ Skipping: {relative_path}")
                        continue

                    html_files.append((full_path, relative_path))

        # Semaphore to limit concurrent captures
        semaphore = asyncio.Semaphore(max_concurrent)

        async def capture_screenshot(
            full_path: str, relative_path: str
        ) -> CaptureResult:
            """
            Capture a single screenshot with error handling.

            Args:
                full_path (str): Full path to HTML file
                relative_path (str): Relative path from site directory

            Returns:
                CaptureResult: Capture result for the screenshot
            """
            async with semaphore:
                result = CaptureResult(
                    page_name=relative_path, page_path=relative_path)
                start_time = asyncio.get_event_loop().time()

                try:
                    # Use Playwright for rendering
                    async with async_playwright() as p:
                        browser = await p.chromium.launch(headless=True)
                        context = await browser.new_context(
                            viewport={"width": 1280, "height": 720}
                        )
                        page = await context.new_page()

                        # Load file directly from filesystem
                        # using absolute file path
                        await page.goto(f"file://{full_path}")

                        # Generate output path preserving directory structure
                        output_filename = relative_path.replace(
                            "/",
                            "_",
                        ).replace(".html", ".png")
                        output_path = os.path.join(
                            output_directory, output_filename)

                        # Ensure output directory exists
                        os.makedirs(os.path.dirname(
                            output_path), exist_ok=True)

                        # Capture screenshot
                        await page.screenshot(
                            path=output_path, full_page=True, timeout=30000
                        )

                        await browser.close()

                        # Populate capture result
                        result.status = CaptureStatus.SUCCESS
                        result.screenshot_path = output_path
                        result.capture_duration = (
                            asyncio.get_event_loop().time() - start_time
                        )

                        console.print(
                            f"✅ Captured: {relative_path} → {output_filename}"
                        )
                        return result

                except Exception as e:
                    console.print(f"❌ Failed to capture {relative_path}: {e}")
                    result.status = CaptureStatus.BROWSER_ERROR
                    result.error_message = str(e)
                    return result

        # Create tasks for all HTML files
        tasks = [
            capture_screenshot(full_path, relative_path)
            for full_path, relative_path in html_files
        ]

        # Run all tasks concurrently and collect results
        results = await asyncio.gather(*tasks)

        # Filter out any failed captures
        successful_captures = [
            r for r in results if r.status == CaptureStatus.SUCCESS]

        console.print(f"📸 Total Screenshots: {len(successful_captures)}")

        return successful_captures

    async def run_visual_tests(
        self,
        site_directory: str = "site/",
    ) -> VisualTestReport:
        """
        Execute visual tests with configurable strategy.

        Supports multiple testing approaches:
        - Full site screenshot capture
        - Specific page testing

        Args:
            strategy (VisualTestStrategy): Chosen testing strategy
            pages (Optional[List[Tuple[str, str]]]): Specific pages to test
            site_directory (str): Directory to scan for HTML files

        Returns:
            VisualTestReport: Comprehensive visual test report
        """
        # Record start time
        start_time = asyncio.get_event_loop().time()
        # Capture screenshots for entire site
        screenshots = await self.capture_site_screenshots(site_directory)

        # Prepare report
        report = await self._prepare_visual_test_report(
            start_time, asyncio.get_event_loop().time(), len(screenshots)
        )

        # Add results to report
        for screenshot in screenshots:
            report.add_result(screenshot)

        return report

    async def _prepare_visual_test_report(
        self, start_time: float, end_time: float, total_pages: int
    ) -> VisualTestReport:
        """
        Create a standardized visual test report.

        Args:
            start_time (float): Test start timestamp
            end_time (float): Test end timestamp
            total_pages (int): Total number of pages processed

        Returns:
            VisualTestReport: Configured test report
        """
        report = VisualTestReport(total_pages=total_pages)
        report.start_time = start_time
        report.end_time = end_time
        return report

    async def _process_specific_pages(
        self,
        pages: List[Tuple[str, str]],
    ) -> List[CaptureResult]:
        """
        Process specific pages for visual testing.

        Args:
            pages (List[Tuple[str, str]]): List of (page_path, page_name)

        Returns:
            List[CaptureResult]: Captured page results
        """

        # Use semaphore to limit concurrent captures
        sem = asyncio.Semaphore(self.max_concurrent_captures)

        async def capture_with_semaphore(page_path, page_name):
            async with sem:
                return await self.capture_screenshot_from_mkdocs_build(
                    page_path, page_name
                )

        # Concurrent page captures
        capture_tasks = [capture_with_semaphore(
            path, name) for path, name in pages]

        return await asyncio.gather(*capture_tasks)


async def run_tests(
    output_dir: Path = typer.Option(
        Path(".cascade/visual-test"),
        help="Output directory for screenshots",
    ),
    width: int = typer.Option(1280, help="Viewport width"),
    height: int = typer.Option(720, help="Viewport height"),
    reuse_build: bool = typer.Option(
        False, help="Skip rebuilding documentation"),
):
    """
    Run advanced visual tests on documentation.

    Supports multiple testing strategies with backward compatibility.
    """
    # Ensure MkDocs build is up to date unless reuse is specified
    if not reuse_build:
        subprocess.run(["mkdocs", "build"], check=True)

    # Initialize visual tester
    visual_tester = AdvancedVisualTester(
        max_concurrent_captures=10,
        global_timeout=30.0,
        viewport_width=width,
        viewport_height=height,
    )

    # Run visual tests
    report = await visual_tester.run_visual_tests(site_directory="site/")

    # Generate and print report summary
    report.generate_summary()


def visual(
    output_dir: Path = typer.Option(
        Path(".cascade/visual-test"),
        help="Output directory for screenshots",
    ),
    width: int = typer.Option(1280, help="Viewport width"),
    height: int = typer.Option(720, help="Viewport height"),
    reuse_build: bool = typer.Option(
        False, help="Skip rebuilding documentation"),
):
    """Run advanced visual tests on documentation."""
    asyncio.run(
        run_tests(
            output_dir=output_dir,
            width=width,
            height=height,
        )
    )


def custom_yaml_load(file_path):
    """
    Custom YAML loader to handle Python function references.

    Args:
        file_path: Path to the YAML file

    Returns:
        Parsed YAML configuration
    """

    def yaml_constructor(loader, tag, node):
        # Simply return the node value as a string
        return node.value

    # Create a custom YAML loader
    yaml.add_multi_constructor(
        "tag:yaml.org,2002:python/name:", yaml_constructor)

    with open(file_path, "r") as f:
        return yaml.full_load(f)


def parse_mkdocs_nav(
    nav_data: List[Dict[str, Any]], base_path: str = ""
) -> List[Tuple[str, str]]:
    """
    Recursively parse the navigation structure from mkdocs.yml.

    Args:
        nav_data: Navigation data from mkdocs.yml
        base_path: Base path for constructing page paths

    Returns:
        List of tuples containing (page_path, page_name)
    """
    pages = []

    def _extract_pages(item, current_path=""):
        if isinstance(item, str):
            # This is a page
            full_path = os.path.join(
                current_path, item).replace(".md", ".html")
            return [(full_path, os.path.splitext(os.path.basename(item))[0])]

        if isinstance(item, dict):
            # This is a section with a name
            results = []
            for key, value in item.items():
                if isinstance(value, str):
                    # Direct page under a section
                    full_path = os.path.join(current_path, value).replace(
                        ".md", ".html"
                    )
                    results.append((full_path, key))
                elif isinstance(value, list):
                    # Nested section
                    for sub_item in value:
                        results.extend(_extract_pages(sub_item, current_path))
            return results

        if isinstance(item, list):
            # List of items in a section
            results = []
            for sub_item in item:
                results.extend(_extract_pages(sub_item, current_path))
            return results

        return []

    # Process each top-level navigation item
    for nav_item in nav_data:
        pages.extend(_extract_pages(nav_item))

    return pages


if __name__ == "__main__":
    typer.run(visual)
