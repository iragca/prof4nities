<h1 align="center">prof4nities</h1>

A small Python library to detect and optionally censor profane or inappropriate words using language-specific wordlists, Levenshtein distance, and fuzzy string matching.

## Installation

To install using [pip](https://pypi.org/project/pip/), run:

```bash
pip install prof4nities
```

## Quick example

```python
from prof4nities import Censor

censor = Censor(language="en")

# assuming "badword" is in the wordlist
print(censor("badword in a sentence"))
# >>> ******* in a sentence

print(censor(["badword", "in", "a", "sentence"]))
# >>> ******* in a sentence

print(censor(["badword", "in", "a", "sentence"], stringify=False))
# >>> [Word('badword'), Word('in'), Word('a'), Word('sentence')]
```

The `Censor` class loads a language-specific `Wordlist` (default `en`) and exposes a callable interface. See `prof4nities/filter.py` for implementation details.

## Configuration via environment variables

`prof4nities` reads a couple of runtime thresholds from environment variables (defined in `prof4nities/config.py`). Export them before running your code to change behavior:

```bash
export LEVENSHTEIN_THRESHOLD=0.75
export FUZZY_RATIO_THRESHOLD=0.85
```

Defaults are:

- `LEVENSHTEIN_THRESHOLD=0.8`
- `FUZZY_RATIO_THRESHOLD=0.8`

## Persistent cache

Two kinds of persisted data are used by the library to avoid repeated downloads:

- WordNet corpora: `Censor` downloads the NLTK WordNet corpus on first use and stores it in the platform cache directory returned by `prof4nities.config.Directories.CACHE_DIR`.
- Wordlists: fetched profanity wordlists are cached under the same application cache in the `wordlists/` subdirectory (e.g. `<cache_dir>/wordlists/en.txt`). The `Wordlist` manager will use a cached copy when present and otherwise fetch from the upstream source and write a best-effort cache copy.

The exact cache location depends on the platform (see the `platformdirs` package). To inspect or override the cache location at runtime you can set the typical platform environment variables (for example on Linux set `XDG_CACHE_HOME`) or read the path via the `prof4nities.config.Directories.CACHE_DIR` value in code.

## Development

### Setting up

Install [uv](https://docs.astral.sh/uv/) using pip.
```bash
pip install uv
```
Other installation methods are documented [here](https://docs.astral.sh/uv/getting-started/installation/).


### Structure

```bash
prof4nities/
├── censor.py          # Core Censor behavior and docstring examples
├── config.py          # Environment-driven settings
└── manager/
    └── wordlist.py    # Wordlist fetching and processing
```

### Testing

[Pytest](https://docs.pytest.org/en/stable/) is used for testing. To run unit tests, run:

```bash
uv run pytest tests/
```

To make your own test, make a file prefixed with `test_` and put it inside the `tests/` directory and should be arranged accordingly.

Then within the file simply import the functionality to test

```python
import pytest

from prof4nities import Censor


# Test cases should be prefixed with `test_`
def test_censor():
    ...
    assert True is True
    ...
```
