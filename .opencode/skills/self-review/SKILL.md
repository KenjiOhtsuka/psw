---
name: self-review
description: Review your own code changes before committing, ensuring they meet project conventions, type safety, and test coverage.
---

# Self-Review

Use this after making code changes and before committing. It ensures the changes are correct, consistent, and safe.

## Process

1. **Understand the diff**
   ```bash
   git diff
   ```
   Identify all modified files and the scope of changes.

2. **Run tests**
   ```bash
   python -m pytest
   ```
   All tests must pass. If any fail, fix them before proceeding.

3. **Check against conventions**

   Verify the changes follow:

   - **Project structure**: `src/psw/` layout with `cli.py` as entry point via `psw.cli:main`
   - **Imports**: standard library first, then third-party, then local (`from psw.utils import KeyListener`)
   - **Type hints**: use Python type hints throughout (`def format_time(self, seconds: float) -> str`)
   - **Naming**: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_CASE` for constants
   - **Error handling**: raise `ValueError` for invalid arguments with descriptive messages
   - **Comments**: keep comments minimal or absent — code should be self-documenting
   - **Strings**: use f-strings for formatting; avoid `%` formatting or `.format()`
   - **Platform support**: use `msvcrt` on Windows, `tty`/`select` on Unix for cross-platform features
   - **Timing**: use `time.monotonic()` for elapsed time (not `time.time()`)

4. **Review for common issues**

   - **Error handling**: no silent failures. Validate arguments in `__init__` (e.g., `if precision < 0: raise ValueError(...)`)
   - **Edge cases**: 
     - Stopwatch: handle precision=0, rapid key presses, lap at exact 60s boundary
     - Timer: handle zero duration, negative numbers, missing duration argument
   - **Type safety**: avoid `Any` where practical. Use proper Python types (`float`, `int`, `str`, `list[str]`, `bool`)
   - **Scope creep**: each change should address only its intended purpose
   - **Security**:
     - No hardcoded secrets (tokens, passwords) in source files
     - `.env` files are gitignored; never commit them
     - No `eval()` or `exec()` on user input
     - Key listener input is sanitized (lowercased, single char)
   - **Console output**: use `sys.stdout.write()` for live rendering, `print()` for final output
   - **ANSI escape codes**: `\033[F` (cursor up) and `\033[K` (clear line) used for in-place clock updates
   - **Cross-platform**: `Path` from `pathlib` for paths (not `os.path` directly for new code)
   - **CLI exit codes**: no explicit `sys.exit()` in library code — let exceptions propagate naturally

5. **Packaging checks** (if modifying `pyproject.toml` or `psw.spec`)

   - `pyproject.toml`: version bump follows semver, `[project.scripts]` entry point is correct
   - `psw.spec`: `pathex=['src']` is present, entry point uses `os.path.join`, EXE `console=True`
   - Requirements: check if any new dependency was added without updating `pyproject.toml`

6. **CI/CD checks** (if modifying `.github/workflows/`)

   - Build workflow uses `pyinstaller psw.spec` (not inline flags)
   - Matrix builds for ubuntu/windows/macos
   - Release job is gated to tags (`if: startsWith(github.ref, 'refs/tags/v')`)
   - `persist-credentials: false` on checkout for security

## Checklist

- [ ] Tests pass (`python -m pytest`)
- [ ] Type hints used throughout
- [ ] Error handling covers edge cases (precision < 0, missing args, rapid input)
- [ ] Change is scoped to its intended purpose
- [ ] No unnecessary files modified
- [ ] No hardcoded secrets in source
- [ ] No `eval()` / `exec()` on user input
- [ ] Console output uses correct method (`sys.stdout.write` vs `print`)
- [ ] ANSI escape sequences correct for live clock rendering
- [ ] Platform-specific code has proper guards (`if sys.platform == "win32"`)
- [ ] Commit message uses conventional format (`fix:`, `feat:`, `chore:`, etc.)
