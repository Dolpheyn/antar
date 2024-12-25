#!/usr/bin/env python
"""
Command-line interface for project management.

This is the main entry point for all project management commands. It provides
a clean interface to various tools and utilities organized by domain:

- docs: Documentation management (build, serve, test)
- [future domains will be added here]

Examples:
    # Start documentation server
    $ python 00.py docs serve

    # Build documentation
    $ python 00.py docs build

    # Show available commands
    $ python 00.py docs --help
"""
# TIP: Run 'chmod +x 00.py' to make this script directly executable
# This allows you to run './00.py' instead of 'python 00.py'
import typer
from scripts.core.cli import create_app
from scripts.app.init import init_app
from scripts.app.docs import docs_app
import os
import sys
import stat

def give_tip_if_script_not_executable():
    """Check if the script is executable and print a tip if not."""
    script_path = os.path.abspath(__file__)
    
    # Check file permissions
    st = os.stat(script_path)
    is_executable = st.st_mode & stat.S_IXUSR
    
    if not is_executable:
        print("\n" + "🚀 " + " TIP FROM TECHOPS ".center(50, "=") + " 🚀")
        print("\nThis script can be more convenient to use by making it executable!")
        print("\n" + "Quick Command:")
        print(f"$ \033[92mchmod +x {script_path}\033[0m\n")
        print("\n" + "🌟 Benefits:")
        print("- Direct execution ('./00.py')")
        print( "- Faster CLI workflow")
        print( "- Native command-line behavior")
        print("\n" + "=" * 60 + "\n")

# Create main app
app = create_app(
    name="Antar techops",
    help_text="Project management tools",
)

# Add the docs_app to the main app
app.add_typer(docs_app)

# Add the init_app to the main app
app.add_typer(init_app)

# Check executability before running the app
give_tip_if_script_not_executable()

if __name__ == "__main__":
    app()
