## Purpose

Short, actionable guidance for AI coding agents working on the prof4nities codebase. Focus on the code structure, key files, conventions, and concrete examples so an agent can make safe, high-value edits quickly.

## Big picture

- This is a small Python library package named `prof4nities` (see `pyproject.toml`).
- Responsibilities are split across a small package:
  - `prof4nities/manager/` — higher-level domain managers (e.g., `wordlist.py` holds the Wordlist class).
  - `prof4nities/` top-level modules — light helpers and config (`config.py`, `filter.py`, `enums.py`).
  - `prof4nities/utils/` — small utility functions (type checks, env checks, path/file helpers).
- Tests live under `tests/` mirroring the package layout (`tests/manager/test_wordlist.py`).

The project uses `httpx` for HTTP interactions (see `prof4nities/manager/wordlist.py`) and standard test tooling (pytest).

## Key files to reference (examples)

- `prof4nities/manager/wordlist.py` — demonstrates network calls with `httpx`, object lifecycle (fetching at **init**), and small data processing helpers (`process_wordlist`). Use this as the canonical example when adding similar manager classes.
- `prof4nities/filter.py` — (if editing filtering behavior) follow existing function signatures and unit-test style.
- `prof4nities/utils/` — helper functions live here; prefer moving small cross-cutting logic into `utils` rather than duplicating.
- `tests/` — agent should add or update unit tests alongside functional changes. Look at `tests/manager/test_wordlist.py` for patterns (pytest + pytest-mock used).

## Project-specific conventions and patterns

- Docstrings: Python files should use NumPy-style docstrings (see `.github/instructions/numpy.instructions.md`). Keep parameter and return sections consistent.

### NumPy-style docstring template (use this)

Use NumPy-style docstrings for public functions and classes. Keep them short and include types for parameters and returns. Example patterns used in this repo:

```python
def fetch_wordlist(language: str) -> list[str]:
  """Fetch a wordlist for `language`.

  Parameters
  ----------
  language : str
    ISO language code (e.g. 'en').

  Returns
  -------
  list[str]
    Sorted, deduplicated list of words from the upstream source.

  Raises
  ------
  ValueError
    If the upstream response status is not 200.
  """


class Wordlist:
  """Container for a language wordlist.

  Parameters
  ----------
  language : str, optional
    ISO language code, by default 'en'.
  """
```

- Tests: tests use pytest and `pytest-mock` for mocking (see `tests/manager/test_wordlist.py`). Prefer mocking external calls (e.g., `httpx.get`) rather than hitting the network.
- Dependencies: listed in `pyproject.toml`. The codebase assumes Python >= 3.14 and uses modern typing (e.g., `list[str]`). Keep type hints consistent.
- Small, explicit APIs: Many objects implement dunder methods (e.g., `__len__`, `__iter__`, `__contains__` in `Wordlist`). Preserve these behaviors when refactoring.
- Immutable config: `Wordlist.SOURCE_URL` constant shows how external endpoints are stored — use module/class constants for external URLs or settings.

## How to run (developer workflows)

- Run tests:

  - Run all tests: `pytest`
  - Run a single test file: `pytest tests/manager/test_wordlist.py -q`

- Linting/formatting (dev dependencies in `pyproject.toml`): prefer `ruff`/`black`/`flake8` in CI; run locally as needed.

- Fast local checks: mock network calls in tests (see `mocker.patch("httpx.get", ...)` usage in tests).

## Integration & external dependencies

- Network I/O: `prof4nities/manager/wordlist.py` calls `httpx.get` directly and raises a `ValueError` on non-200 responses. When adding code that performs network calls, follow this pattern: keep network calls easy to mock and raise clear, testable exceptions on failures.
- Environment/config: small `config.py` module is present for cross-cutting settings — prefer reading/writing through `config.py` rather than sprinkling env access.

## Examples of acceptable edits

- Adding a new manager class should mirror `Wordlist`: fetch or compute data in clearly named methods, keep heavy work out of the constructor when possible, and provide dunder helpers if the object is sequence-like.
- When extending network logic, add unit tests that patch `httpx.get` and assert both success and failure branches (see `tests/manager/test_wordlist.py`).

## Safety & testing guidance for agents

- Avoid real network calls in tests — always mock `httpx` or other HTTP libraries.
- Keep changes small and isolated. Add a focused unit test with each behavioral change.

## Where to look when uncertain

- `pyproject.toml` — dependency and tooling hints (pytest, ruff, black).
- `README.md` — small usage notes.
- `tests/` — canonical examples of how features are exercised.

## After making changes

1. Run the unit tests you touched (pytest path/to/test). 2. Run linting/type checks if you changed interfaces. 3. Keep docstrings in NumPy style.

---

If any section is unclear or you want more examples (e.g., filter implementation patterns, tests for utils), tell me which area and I'll expand the file with concrete snippets.
