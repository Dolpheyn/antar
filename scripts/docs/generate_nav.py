from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Any
import re


@dataclass
class NavItem:
    """Represents a navigation item in the mkdocs structure."""

    title: str
    path: Optional[str] = None
    children: Optional[List["NavItem"]] = None

    def to_yaml_str(self, indent: int = 0) -> str:
        """
        Convert NavItem to a YAML-compatible string representation.

        Args:
            indent: Current indentation level

        Returns:
            YAML-compatible string representation
        """
        indent_str = " " * indent

        # If it's a simple file
        if not self.children and self.path:
            return f"{indent_str}- {self.title}: {self.path}"

        # If it's a directory with children
        if self.children:
            result = [f"{indent_str}- {self.title}:"]
            for child in self.children:
                result.append(child.to_yaml_str(indent + 2))
            return "\n".join(result)

        # Fallback to title if no path or children
        return f"{indent_str}- {self.title}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert NavItem to a dictionary for YAML serialization.

        Returns:
            Dictionary representation of the NavItem
        """
        if self.children:
            return {
                self.title: [
                    child.to_dict() if isinstance(child, NavItem) else child
                    for child in self.children
                ]
            }
        return {self.title: self.path} if self.path else self.title

    @classmethod
    def from_path(cls, file_path: Path, base_path: Path) -> "NavItem":
        """
        Create a NavItem from a file path.

        Args:
            file_path: Path to the markdown file
            base_path: Base directory for calculating relative path

        Returns:
            NavItem representing the file
        """
        return cls(
            title=cls._humanize_title(file_path.stem),
            path=str(file_path.relative_to(base_path)),
        )

    @staticmethod
    def _humanize_title(filename: str) -> str:
        """
        Convert filename to a human-readable title.

        Args:
            filename: Raw filename

        Returns:
            Formatted title in title case
        """
        filename = filename.strip().lower()
        # check if filename is date YYYY-MM-DD
        if re.match(r"^\d{4}-\d{2}-\d{2}$", filename):
            return filename
        # filename has no spaces or dashes
        if " " not in filename and "-" not in filename:
            return filename.title()

        # replace 'ci-cd' with 'CI/CD'
        known_transformations = {
            "ci-cd": "CI/CD",
        }
        for k, v in known_transformations.items():
            if k in filename:
                filename = filename.replace(k, v)

        # Replace hyphens and underscores, then title case
        words = filename.replace("-", " ").replace("_", " ").split()
        words = [word.strip() for word in words]

        # Special cases for common abbreviations and short words
        special_cases = {
            "api": "API",
            "id": "ID",
            "ui": "UI",
            "url": "URL",
            "http": "HTTP",
            "https": "HTTPS",
            "ai": "AI",
        }

        result = []
        for word in words:
            if word in special_cases:
                result.append(special_cases[word])
                continue
            result.append(word.title())
        return " ".join(result)


def is_markdown_file(path: Path) -> bool:
    """
    Check if a path is a markdown file.

    Args:
        path: Path to check

    Returns:
        True if the path is a markdown file, False otherwise
    """
    return path.suffix.lower() in {".md", ".markdown"}


def find_markdown_files(directory: Path) -> List[Path]:
    """
    Recursively find all markdown files in a directory.

    Args:
        directory: Directory to search

    Returns:
        List of markdown file paths
    """
    mdfiles = [path for path in directory.rglob("*") if is_markdown_file(path)]
    return sorted(mdfiles)


def generate_nav_structure(docs_path: Path) -> List[NavItem]:
    """
    Generate a navigation structure for mkdocs.

    Args:
        docs_path: Path to the documentation directory

    Returns:
        Nested list of navigation items
    """

    def build_nav_for_directory(directory: Path) -> Optional[List[NavItem]]:
        """
        Build navigation structure for a specific directory.

        Args:
            directory: Directory to process

        Returns:
            List of navigation items or None if no markdown files
        """
        # Find markdown files directly in this directory
        direct_files = [
            NavItem.from_path(file_path, docs_path)
            for file_path in find_markdown_files(directory)
            if file_path.parent == directory
        ]

        # Find subdirectories with markdown files
        subdirectory_navs = [
            NavItem(
                title=NavItem._humanize_title(subdir.name),
                children=build_nav_for_directory(subdir),
            )
            for subdir in sorted(directory.iterdir())
            if subdir.is_dir() and find_markdown_files(subdir)
        ]

        # Combine direct files and subdirectory navigation
        combined_nav = direct_files + subdirectory_navs

        return combined_nav if combined_nav else None

    # Generate the full navigation structure
    return build_nav_for_directory(docs_path) or []


def update_mkdocs_nav(
    nav_structure: List[NavItem],
    config_path: Path = Path("mkdocs.yml"),
    output_path: Optional[Path] = None,
) -> None:
    """
    Update the nav section of
    an existing mkdocs.yml file
    using string manipulation.

    Args:
        nav_structure: Generated navigation structure
        config_path: Path to the existing mkdocs.yml
        output_path: Optional path to write the updated config.
                     If None, overwrites the original file.
    """
    # Use output_path or default to config_path if not specified
    output_path = output_path or config_path

    try:
        # Read the entire file content
        with config_path.open("r") as config_file:
            content = config_file.read()

        # Generate nav section as YAML string
        nav_yaml_str = "\n".join(item.to_yaml_str() for item in nav_structure)

        # Replace nav section using regex
        updated_content = re.sub(
            r"(nav:).*?(\n\w+:|$)",
            r"\1\n" + nav_yaml_str + r"\2",
            content,
            flags=re.DOTALL,
        )

        # Write back to file
        with output_path.open("w") as config_file:
            config_file.write(updated_content)

        print(f"Successfully updated mkdocs navigation at {output_path}")

    except Exception as error:
        print(f"Error updating navigation: {error}")


def generate_nav(
    docs_path: Path = Path("docs"),
    config_path: Path = Path("mkdocs.yml"),
    output_path: Optional[Path] = None,
) -> None:
    """
    Main function to generate and update mkdocs navigation.

    Args:
        docs_path: Path to documentation directory
        config_path: Path to existing mkdocs configuration
        output_path: Optional path to write updated configuration
    """
    try:
        nav_structure = generate_nav_structure(docs_path)
        update_mkdocs_nav(nav_structure, config_path, output_path)
    except Exception as error:
        print(f"Error in main process: {error}")


if __name__ == "__main__":
    generate_nav()
