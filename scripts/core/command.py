"""Command registry and management."""
import subprocess
import sys
from typing import Dict, Callable, Optional, List

# Registry to store all commands
_commands: Dict[str, Callable] = {}

def register_command(name: str, help_text: str = "") -> Callable:
    """Register a command in the global registry."""
    def decorator(func: Callable) -> Callable:
        _commands[name] = func
        func.command_name = name
        func.help_text = help_text
        return func
    return decorator

def get_command(name: str) -> Optional[Callable]:
    """Get a command by name."""
    return _commands.get(name)

def get_all_commands() -> Dict[str, Callable]:
    """Get all registered commands."""
    return _commands.copy()

def run_command(name: str, args: Optional[List[str]] = None) -> None:
    """Run a command by name."""
    command = get_command(name)
    if command:
        command(args)
    else:
        raise ValueError(f"Unknown command: {name}")

def run_python_module(module: str, *args: str) -> None:
    """Run a Python module with arguments."""
    try:
        subprocess.check_call([sys.executable, "-m", module] + list(args))
    except subprocess.CalledProcessError as e:
        print(f"Error running module {module} with args {args}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)
