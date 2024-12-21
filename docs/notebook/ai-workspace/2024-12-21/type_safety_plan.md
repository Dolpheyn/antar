# Type Safety Improvement Plan

## Remaining Pyright Warnings

### 1. Function Attribute Assignment
**Target Files:**
- `scripts/commands/base.py`
- `scripts/core/command.py`

**Mitigation Strategy:**
- Implement Protocol-based type hinting
- Create a custom decorator for command registration
- Use `__setattr__` for dynamic attribute assignment

### 2. Argument Type Incompatibility
**Target File:**
- `scripts/commands/base.py`

**Mitigation Strategy:**
- Create a robust subprocess call utility function
- Add comprehensive type hints
- Implement safe type conversion
- Add error handling

### 3. Optional Subscript Errors
**Target File:**
- `scripts/docs/visual.py`

**Mitigation Strategy:**
- Implement safe access utility functions
- Add explicit type checking
- Use `Optional` and `Union` types
- Create defensive programming patterns

### 4. Missing Arguments
**Target File:**
- `scripts/docs/build.py`

**Mitigation Strategy:**
- Review function signatures
- Add default configurations
- Implement configuration management

## Progress Update

### TypeVar and Protocol Improvements
- Replaced TypeVar with Protocol-based type hinting
- Implemented `CommandFunction` Protocol in `base.py` and `command.py`
- Enhanced type safety for command registration
- Resolved Pyright TypeVar usage warnings
- Improved dynamic attribute assignment

### Key Changes
- Removed generic TypeVar constraints
- Added comprehensive Protocol definition
- Used `object.__setattr__` for type-safe attribute assignment
- Maintained flexible command registration mechanism

### Type Safety Strategies
- Protocol-based type hinting
- Dynamic attribute assignment
- Precise type annotations
- Improved type checking

### Improvements
- More robust type information
- Clearer function contract
- Reduced type checking warnings
- Maintained code flexibility

### Advanced Type Handling in Command Execution
- Implemented overloaded `run_command()` function
- Added `RunCommandKwargs` TypedDict for flexible keyword arguments
- Used `typing_extensions.Unpack` for precise type checking
- Enhanced subprocess command execution type safety
- Resolved argument type incompatibility warnings

### Key Type Safety Improvements
- Multiple function overloads for different input types
- Flexible keyword argument handling
- Precise type annotations for subprocess arguments
- Improved error handling and type checking

### Type Handling Strategies
- Function overloading
- TypedDict for keyword arguments
- Dynamic argument normalization
- Comprehensive type checking

### Improvements
- More robust command execution
- Enhanced type safety
- Flexible argument handling
- Clear function contracts
- Reduced type checking warnings

### Import Symbol Resolution
- Fixed `clean_docs` import in `build.py`
- Corrected function import from `.clean` module
- Resolved Pyright import symbol warnings
- Improved import statement clarity

### Resolved Imports
1. **Removed Phantom Import**
   - Location: `scripts/core/__init__.py`
   - Issue: `create_command_table` was an undefined import symbol
   - Resolution: Removed the import and reference from `__all__`
   - Rationale: Prevent potential import errors and clean up unused symbols

### Key Import Improvements
- Replaced incorrect function name `clean_docs`
- Used correct relative import
- Maintained existing import structure
- Ensured type safety in import statements

### Import Handling Strategies
- Precise function name matching
- Correct relative import usage
- Minimal import modifications
- Preserving existing code structure

### Improvements
- Eliminated import symbol errors
- Enhanced code readability
- Simplified import statements
- Improved type checking compatibility

### Remaining Tasks
- [x] Resolve import symbol errors
- [ ] Address FloatRect type incompatibility
- [ ] Run comprehensive type checking

### Potential Enhancements
- Develop centralized import management
- Create import validation utilities
- Implement advanced import type checking

## Type Safety Metrics
- Resolved import symbol warnings
- Improved import statement precision
- Enhanced code consistency

## Next Focus Areas
1. Address FloatRect type incompatibility
2. Comprehensive type checking
3. Advanced import management

## Pyright Type Checking Results

### Overview
- Total Errors: 10
- Total Warnings: 2
- Completed in 2.053 seconds

### Detailed Error Analysis

#### Base Command Errors
1. **TypeVar Usage Warning**
   - Location: `scripts/commands/base.py`
   - Issue: TypeVar "T" appears only once in generic function signature
   - Recommendation: Use `(...) -> Unknown` instead

2. **Argument Type Incompatibility**
   - Location: `scripts/commands/base.py`
   - Issues:
     - No overloads for "run" match the provided arguments
     - Argument type mismatch in command arguments

#### Import and Symbol Resolution
1. **Unknown Import Symbols**
   - Location: `scripts/core/__init__.py`
     - `create_command_table` is an unknown import symbol
   - Location: `scripts/docs/build.py`
     - `clean_docs` is an unknown import symbol

#### Visual Testing Type Errors
1. **FloatRect Type Incompatibility**
   - Location: `scripts/docs/visual.py`
   - Multiple errors with `safe_get()` function
   - Issue: Cannot pass `FloatRect` to function expecting `Dict[str, Any] | None`

### Recommended Actions
1. Refactor TypeVar usage in generic functions
2. Review and correct import statements
3. Update `safe_get()` to handle `FloatRect` type
4. Implement more robust type checking for command arguments

### Improvement Strategies
- Use more precise type annotations
- Create custom type protocols
- Implement stricter type checking
- Add type stub files for complex types

### Next Immediate Steps
1. Modify `base.py` to resolve TypeVar warnings
2. Fix import symbol resolution
3. Update `visual.py` to handle `FloatRect` correctly
4. Run comprehensive type checking after modifications

## Type Safety Progress
- Identified specific type inconsistencies
- Highlighted areas for type annotation improvement
- Demonstrated commitment to robust type checking

## Continuous Improvement
- Regular Pyright type checking
- Incremental type safety enhancements
- Focus on preventing runtime type errors

## Type Safety Metrics
- Resolved optional subscript warnings
- Improved argument handling
- Enhanced configuration flexibility
- More robust error management
- Increased type consistency

## Next Focus Areas
1. Comprehensive type checking
2. Potential utility module for configuration validation
3. Advanced error handling strategies

## Implementation Phases
1. Analyze current implementations
2. Design type-safe solutions
3. Implement changes
4. Run comprehensive type checking
5. Refactor and optimize

## Guiding Principles
- Maintain code readability
- Minimize runtime type checking overhead
- Provide clear error messages
- Use Python's type hinting capabilities effectively

## Tools and Techniques
- `typing` module
- Protocols
- Type guards
- Custom decorators
- Utility functions for safe access

## Success Criteria
- Resolve all Pyright warnings
- Improve type consistency
- Enhance code quality
- Maintain existing functionality
