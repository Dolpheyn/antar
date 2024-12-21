# Pyright LSP Analysis and Mitigation Plan

## Overview
This document tracks the analysis and mitigation of Pyright LSP warnings across the project.

## Workspace Setup
- Date: 2024-12-21
- Context: Long-running type checking and code quality improvement task

## Analysis Phases
1. Collect Pyright LSP Warnings
2. Categorize Warnings
3. Develop Mitigation Strategies
4. Implement Fixes
5. Verify Improvements

## Current Status
- Initial analysis in progress
- Waiting for specific Pyright LSP output

## Notes
- Focus on type hints and type consistency
- Minimize runtime type checking overhead
- Maintain code readability

### Potential Improvement Areas
- Type annotations
- Type narrowing
- Protocol/Interface definitions
- Generics usage

## Detailed Warnings Analysis

### Common Issues
1. **Console Import Warnings** (reportAttributeAccessIssue)
   - Affected files:
     - 00.py
     - scripts/core/__init__.py
     - scripts/docs/build.py
     - scripts/docs/clean.py
     - scripts/docs/render.py
     - scripts/docs/serve.py
     - scripts/docs/setup.py
     - scripts/docs/visual.py
   - **Mitigation**: Ensure proper import of `console` from `rich.console`

2. **Function Attribute Assignment Errors** (reportFunctionMemberAccess)
   - Affected files:
     - scripts/commands/base.py
     - scripts/core/command.py
   - Errors with `command_name` and `help_text` attributes
   - **Mitigation**: Use a decorator or type hint to allow dynamic attribute assignment

3. **Argument Type Incompatibility** (reportArgumentType)
   - File: scripts/commands/base.py
   - Specific issue with `check_call` argument types
   - **Mitigation**: Carefully type the arguments for subprocess calls

4. **Optional Subscript Errors** (reportOptionalSubscript)
   - File: scripts/docs/visual.py
   - Multiple lines with potential `None` subscripting
   - **Mitigation**: Add proper type checking and handling

5. **Missing Arguments** (reportCallIssue)
   - File: scripts/docs/build.py
   - Missing `config` parameter in a function call
   - **Mitigation**: Provide the required configuration argument

### Proposed Solution Strategy
1. Create type stubs or use `typing.Protocol` for dynamic attributes
2. Enhance type annotations across affected files
3. Add runtime type checking where necessary
4. Use `Optional` and `Union` types more precisely
5. Implement proper error handling

### Action Plan
- [ ] Update console imports
- [ ] Create type-safe command decorator
- [ ] Refactor subprocess call arguments
- [ ] Add type guards for optional subscripting
- [ ] Complete missing function arguments

## Detailed Mitigation Approach

### 1. Command Decorator Type Safety
```python
from typing import Callable, TypeVar, Any

T = TypeVar('T', bound=Callable[..., Any])

def register_command(name: str, help_text: str = "") -> Callable[[T], T]:
    def decorator(func: T) -> T:
        # Use __setattr__ to bypass type checking
        object.__setattr__(func, 'command_name', name)
        object.__setattr__(func, 'help_text', help_text)
        return func
    return decorator
```

### 2. Console Import Standardization
```python
from rich.console import Console
console = Console()
```

### 3. Subprocess Call Type Handling
```python
from typing import Union, List, Optional
import subprocess
import sys

def run_command(
    command: Union[str, List[str]], 
    cwd: Optional[str] = None
) -> None:
    try:
        # Ensure consistent type
        cmd = command if isinstance(command, list) else [command]
        subprocess.check_call(cmd, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        sys.exit(1)
```

### 4. Optional Subscript Handling
```python
from typing import Optional, Dict, Any

def safe_get(d: Optional[Dict[str, Any]], key: str, default: Any = None) -> Any:
    return d.get(key, default) if d is not None else default
```

## Detailed Mitigation Approach: Technical Deep Dive

### 1. Command Decorator Type Safety: Dynamic Attribute Challenge
**Technical Context:**
Python's function objects are typically immutable by default. When using decorators to dynamically add attributes like `command_name` and `help_text`, Pyright raises type safety concerns because these attributes are not part of the function's original type definition.

**Current Implementation Problem:**
```python
def register_command(name: str, help_text: str = "") -> Callable:
    def decorator(func: Callable) -> Callable:
        # This line triggers Pyright's reportFunctionMemberAccess
        func.command_name = name  # ❌ Type error
        func.help_text = help_text  # ❌ Type error
        return func
    return decorator
```

**Proposed Mitigation Strategies:**
1. **Bypass Type Checking with `__setattr__`**
   ```python
   def register_command(name: str, help_text: str = "") -> Callable[[T], T]:
       def decorator(func: T) -> T:
           # Directly use object's __setattr__ to bypass type restrictions
           object.__setattr__(func, 'command_name', name)
           object.__setattr__(func, 'help_text', help_text)
           return func
       return decorator
   ```

2. **Protocol-Based Type Hinting**
   ```python
   from typing import Protocol, Callable

   class CommandFunction(Protocol):
       command_name: str
       help_text: str
       def __call__(self, *args, **kwargs): ...

   def register_command(name: str, help_text: str = "") -> Callable[[Callable], CommandFunction]:
       # Implementation that satisfies the CommandFunction protocol
   ```

**Rationale:**
- `__setattr__` provides a runtime mechanism to add attributes
- Protocol-based typing offers compile-time type safety
- Allows dynamic attribute assignment while maintaining type information

### 2. Console Import Standardization: Dependency Management
**Technical Context:**
Inconsistent console imports across multiple files indicate a potential architectural inconsistency in dependency management.

**Current Problem:**
- Multiple files importing `console` differently
- No centralized console configuration
- Potential for circular imports

**Proposed Solution:**
```python
# scripts/core/console.py
from rich.console import Console

# Singleton-like global console instance
console = Console(
    color_system="auto",  # Adaptive color support
    force_terminal=False,  # Respect environment settings
    width=120,  # Consistent output width
)

# Usage in other modules
from scripts.core.console import console
```

**Benefits:**
- Centralized console configuration
- Consistent styling across all scripts
- Easier mocking for testing
- Reduced import complexity

### 3. Subprocess Call Type Handling: Safety and Flexibility
**Technical Context:**
The current implementation lacks robust type handling for subprocess calls, leading to potential runtime errors and type inconsistencies.

**Current Problem:**
```python
def run_command(command: str, cwd: Optional[str] = None) -> None:
    subprocess.check_call(command, shell=True, cwd=cwd)  # ❌ Unsafe shell=True
```

**Proposed Robust Implementation:**
```python
from typing import Union, List, Optional, Sequence
import subprocess
import shlex
import sys

def run_command(
    command: Union[str, Sequence[str]], 
    cwd: Optional[str] = None, 
    shell: bool = False
) -> subprocess.CompletedProcess:
    """
    Safely execute shell commands with comprehensive type handling.
    
    Args:
        command: Command to execute (string or list of strings)
        cwd: Working directory for command execution
        shell: Whether to use shell (defaults to False for security)
    
    Returns:
        Completed process with execution details
    """
    try:
        # Convert string to list, respecting shell quoting
        cmd = shlex.split(command) if isinstance(command, str) else list(command)
        
        return subprocess.run(
            cmd, 
            cwd=cwd, 
            shell=shell, 
            check=True,  # Raise CalledProcessError on non-zero exit
            capture_output=True,  # Capture stdout/stderr
            text=True  # Return string instead of bytes
        )
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        sys.exit(1)
```

**Advanced Type Safety Features:**
- Supports both string and list command inputs
- Uses `shlex.split()` for secure string parsing
- Captures and logs command output
- Provides rich error information
- Defaults to non-shell execution for security

### 4. Optional Subscript Handling: Defensive Programming
**Technical Context:**
Optional subscripting often indicates potential `None` values that can cause runtime errors.

**Proposed Safe Access Pattern:**
```python
from typing import Optional, Dict, Any, TypeVar

T = TypeVar('T')

def safe_get(
    container: Optional[Dict[str, T]], 
    key: str, 
    default: Optional[T] = None
) -> Optional[T]:
    """
    Safely retrieve dictionary values with optional fallback.
    
    Args:
        container: Potentially None dictionary
        key: Dictionary key to retrieve
        default: Default value if key not found or container is None
    
    Returns:
        Value associated with key or default
    """
    return container.get(key, default) if container is not None else default

# Usage example
result = safe_get(maybe_dict, 'key', default=[])
```

**Benefits:**
- Eliminates `None` subscript errors
- Provides default value handling
- Works with generic types
- Improves code readability and safety

### Overarching Type Safety Philosophy
1. **Defensive Design**: Anticipate and handle potential `None` or unexpected types
2. **Explicit Type Hints**: Use `Optional`, `Union`, and `Protocol`
3. **Runtime Validation**: Add type checking where compile-time checks are insufficient
4. **Centralized Configuration**: Create utility modules for shared concerns

### Next Concrete Steps
1. Implement centralized `console.py`
2. Refactor command decorators
3. Update subprocess utility functions
4. Add safe access utility functions
5. Run comprehensive type checking

## Next Steps
1. Implement type stubs
2. Run comprehensive type checking
3. Refactor code with new type safety measures
4. Verify reduction in Pyright warnings

## Progress Tracking
- [x] Initial analysis
- [ ] Type stub creation
- [ ] Code refactoring
- [ ] Final type checking verification
