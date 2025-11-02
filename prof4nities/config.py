import os
from enum import Enum


class Environment(Enum):
    """Settings class to hold environment variables."""

    LEVENSHTEIN_THRESHOLD = float(os.getenv("LEVENSHTEIN_THRESHOLD", "0.8"))
    FUZZY_RATIO_THRESHOLD = float(os.getenv("FUZZY_RATIO_THRESHOLD", "0.8"))
