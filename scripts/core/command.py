"""Command registry and management."""

import subprocess
import sys
from typing import (
    Dict, 
    Callable, 
    Optional, 
    List, 
    Union, 
    Any, 
    Sequence, 
    Protocol
)

# Registry to store all commands
_commands: Dict[str, 'CommandFunction'] = {}


class CommandFunction(Protocol):
    """Protocol defining a command function with dynamic attributes."""
    command_name: str
    help_text: str
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


def register_command(name: str, help_text: str = "") -> Callable[[Callable], CommandFunction]:
    """
    Register a command in the global registry with type-safe attribute assignment.
    
    Args:
        name: Name of the command
        help_text: Description of the command
    
    Returns:
        A decorator that adds command metadata to the function
    """
    def decorator(func: Callable) -> CommandFunction:
        # Use __setattr__ to bypass type checking
        object.__setattr__(func, 'command_name', name)
        object.__setattr__(func, 'help_text', help_text)
        
        # Add to global registry
        _commands[name] = func  # type: ignore
        
        return func  # type: ignore
    
    return decorator


def get_command(name: str) -> Optional[CommandFunction]:
    """
    Get a command by name.
    
    Args:
        name: Name of the command to retrieve
    
    Returns:
        The command function or None if not found
    """
    return _commands.get(name)


def get_all_commands() -> Dict[str, CommandFunction]:
    """
    Get all registered commands.
    
    Returns:
        A copy of the commands registry
    """
    return _commands.copy()


def run_command(
    name: str, 
    args: Optional[Union[List[str], Sequence[str]]] = None
) -> Optional[Any]:
    """
    Run a command by name.
    
    Args:
        name: Name of the command to run
        args: Optional arguments to pass to the command
    
    Returns:
        Result of the command execution
    
    Raises:
        ValueError: If the command is not found
    """
    command = get_command(name)
    if command:
        return command(args) if args is not None else command()
    else:
        raise ValueError(f"Unknown command: {name}")


def run_python_module(
    module: str, 
    *args: str
) -> subprocess.CompletedProcess:
    """
    Run a Python module with arguments and improved type safety.
    
    Args:
        module: Python module to run
        args: Additional arguments to pass to the module
    
    Returns:
        Completed process with execution details
    
    Raises:
        subprocess.CalledProcessError: If module execution fails
    """
    try:
        cmd = [sys.executable, "-m", module] + list(args)
        return subprocess.run(
            cmd, 
            check=True, 
            capture_output=True, 
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running module {module} with args {args}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        sys.exit(1)
