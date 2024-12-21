"""Base command functionality."""

import subprocess
import sys
from typing import List, Optional, Callable


def register_command(name: str, help_text: str = "") -> Callable:
    """Decorator to register a command."""

    def decorator(func: Callable) -> Callable:
        func.command_name = name
        func.help_text = help_text
        return func

    return decorator


def run_command(command: str, cwd: Optional[str] = None) -> None:
    """Run a command and handle errors."""
    try:
        subprocess.check_call(command, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)


def run_python_module(module: str, *args: List[str]) -> None:
    """Run a Python module with arguments."""
    try:
        cmd = [sys.executable, "-m", module] + list(args)
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(f"Error running module {module} with args {args}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)
