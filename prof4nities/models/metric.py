from abc import ABC, abstractmethod
from typing import Union

import numpy as np
from rapidfuzz import fuzz

from ..models import Word


class StringMetric(ABC):
    def __init__(
        self,
        str1: Union[str, Word],
        str2: Union[str, Word],
        threshold: Union[int, float],
    ) -> None:
        self.str1 = str1
        self.str2 = str2
        self._threshold = threshold

    @abstractmethod
    def compute(self) -> Union[int, float]:
        pass

    @property
    @abstractmethod
    def passes_threshold(self) -> bool:
        """
        If both strings are a match based on the metric's threshold,
        then return True, else False.
        """
        pass


class LevenshteinDistance(StringMetric):
    def __init__(
        self, str1: Union[str, Word], str2: Union[str, Word], threshold: int = 2
    ) -> None:
        super().__init__(str1, str2, threshold)

    def compute(self) -> int:
        # References for algorithm:
        # - https://www.youtube.com/watch?v=eneSE4vVAOs
        # - https://www.geeksforgeeks.org/dsa/damerau-levenshtein-distance/
        # - https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
        # - https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance

        len_str1 = len(self.str1) + 1
        len_str2 = len(self.str2) + 1

        dp = np.zeros((len_str1, len_str2), dtype=int)

        for i in range(len_str1):
            dp[i][0] = i
        for j in range(len_str2):
            dp[0][j] = j

        for i in range(1, len_str1):
            for j in range(1, len_str2):
                if self.str1[i - 1] == self.str2[j - 1]:
                    # copy the value from the top-left diagonal
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],  # Deletion
                        dp[i][j - 1],  # Insertion
                        dp[i - 1][j - 1],  # Substitution
                    )

        return dp[-1][-1].item()

    @property
    def passes_threshold(self) -> bool:
        return self.compute() <= self._threshold


class FuzzyRatio(StringMetric):
    def __init__(
        self, str1: Union[str, Word], str2: Union[str, Word], threshold: float = 80.0
    ) -> None:
        super().__init__(str1, str2, threshold)

    def compute(self) -> float:
        return fuzz.ratio(self.str1, self.str2)

    @property
    def passes_threshold(self) -> bool:
        return self.compute() >= self._threshold
