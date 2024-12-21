"""Base command functionality."""

import subprocess
import sys
from typing import Callable, Optional, Sequence, Union, Any, Protocol, overload
from typing_extensions import Unpack, TypedDict
from core import console


class CommandFunction(Protocol):
    """Protocol defining a command function with dynamic attributes."""

    command_name: str
    help_text: str

    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


class RunCommandKwargs(TypedDict, total=False):
    """Keyword arguments for run_command."""

    cwd: Optional[str]
    shell: bool
    capture_output: bool
    text: bool


@overload
def run_command(
    command: str, **kwargs: Unpack[RunCommandKwargs]
) -> subprocess.CompletedProcess: ...


@overload
def run_command(
    command: Sequence[str], **kwargs: Unpack[RunCommandKwargs]
) -> subprocess.CompletedProcess: ...


def run_command(
    command: Union[str, Sequence[str]], **kwargs: Unpack[RunCommandKwargs]
) -> subprocess.CompletedProcess:
    """
    Run a command with improved type safety and error handling.

    Args:
        command: Command to execute (string or sequence of strings)
        **kwargs: Additional subprocess run arguments

    Returns:
        Completed process with execution details

    Raises:
        subprocess.CalledProcessError: If command execution fails
    """
    try:
        return subprocess.run(command, check=True, **kwargs)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Command execution failed: {e}[/red]")
        raise


def register_command(
    name: str, help_text: str = ""
) -> Callable[[Callable], CommandFunction]:
    """
    Decorator to register a command with type-safe attribute assignment.

    Args:
        name: Name of the command
        help_text: Description of the command

    Returns:
        A decorator that adds command metadata to the function
    """

    def decorator(func: Callable) -> CommandFunction:
        # Use __setattr__ to bypass type checking
        object.__setattr__(func, "command_name", name)
        object.__setattr__(func, "help_text", help_text)
        return func  # type: ignore

    return decorator


def run_python_module(module: str, *args: str) -> subprocess.CompletedProcess:
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
        return subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running module {module} with args {args}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        sys.exit(1)
