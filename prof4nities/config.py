import os
from enum import Enum

from platformdirs import user_cache_dir


class Directories(Enum):
    """Settings class to hold directory paths."""

    CACHE_DIR = user_cache_dir(appname="prof4nities", appauthor="iragca")


class Environment(Enum):
    """Settings class to hold environment variables."""

    LEVENSHTEIN_THRESHOLD = float(os.getenv("LEVENSHTEIN_THRESHOLD", "0.8"))
    FUZZY_RATIO_THRESHOLD = float(os.getenv("FUZZY_RATIO_THRESHOLD", "0.8"))
