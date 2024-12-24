# Docs CI Error: Poetry Lock File Mismatch

## Problem
- Poetry installation failed due to lock file inconsistency
- `pyproject.toml` changed significantly since `poetry.lock` was last generated

## Root Cause
The `poetry.lock` file is out of sync with the current `pyproject.toml` dependencies.

## Solution
1. Regenerate the Poetry lock file:
```bash
poetry lock [--no-update]
```

## Detailed Diagnosis
- Ensure all dependencies are correctly specified in `pyproject.toml`
- Verify no conflicting or outdated package versions
- Regenerate lock file to match current project configuration

## Verification Steps
1. Run `poetry lock` command
2. Commit updated `poetry.lock`
3. Rerun CI pipeline

## Potential Impacts
- Ensures consistent dependency resolution
- Prevents installation failures
- Maintains reproducible build environment

## Recommended Actions
- Update lock file
- Review dependency specifications
- Test local installation before committing

## Error Log

```
Run poetry install --no-interaction --no-root
Creating virtualenv antar in /__w/antar/antar/.venv
Installing dependencies from lock file

pyproject.toml changed significantly since poetry.lock was last generated. Run `poetry lock [--no-update]` to fix the lock file.
Error: Process completed with exit code 1.
```