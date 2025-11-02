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
        """
        Compute the string metric between the two input strings.
        """
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
    """
    Compute the normalized Levenshtein distance (edit distance) and similarity score
    between two strings.

    The Levenshtein distance is defined as the minimum number of single-character
    edits (insertions, deletions, or substitutions) required to change one string
    into another. This implementation also provides a normalized similarity score
    between 0 and 1, where 1 indicates identical strings.

    Parameters
    ----------
    str1 : str or Word
        The first input string.
    str2 : str or Word
        The second input string.
    threshold : float, optional, default=0.80
        Minimum similarity score required for the strings to be considered similar.

    References
    ----------
    .. [1] YouTube: "Dynamic Programming - Edit Distance (Levenshtein Distance)"
           https://www.youtube.com/watch?v=eneSE4vVAOs
    .. [2] GeeksforGeeks: "Damerau–Levenshtein distance"
           https://www.geeksforgeeks.org/dsa/damerau-levenshtein-distance/
    .. [3] Wikipedia: "Levenshtein distance"
           https://en.wikipedia.org/wiki/Levenshtein_distance
    """

    def __init__(
        self, str1: Union[str, Word], str2: Union[str, Word], threshold: float = 0.80
    ) -> None:
        super().__init__(str1, str2, threshold)

    def compute(self) -> float:
        """
        Compute the normalized Levenshtein similarity score between two strings.

        This method calculates the raw Levenshtein distance using the
        :meth:`distance` static method, then normalizes it to a similarity score
        between 0 and 1.

        Returns
        -------
        float
            A similarity score between 0 and 1, where:

            - 1.0 indicates identical strings
            - 0.0 indicates maximum dissimilarity

        See Also
        --------
        distance : Compute the raw Levenshtein distance between two strings.
        _similarity_score : Convert a distance value to a normalized similarity score.
        """
        return self._similarity_score(
            self._distance(self.str1, self.str2), len(self.str1), len(self.str2)
        )

    @staticmethod
    def _distance(str1: Union[str, Word], str2: Union[str, Word]) -> int:
        """
        Compute the Levenshtein edit distance between two strings.

        The Levenshtein distance is defined as the minimum number of single-character
        edits (insertions, deletions, or substitutions) required to change one string
        into another. This implementation uses dynamic programming to compute the
        optimal edit distance.

        Parameters
        ----------
        str1 : str or Word
            The first input string.
        str2 : str or Word
            The second input string.

        Returns
        -------
        int
            The minimum number of edits required to transform `str1` into `str2`.

        Notes
        -----
        The algorithm constructs a 2D dynamic programming (DP) matrix of shape
        ``(len(str1) + 1, len(str2) + 1)``, where ``dp[i, j]`` represents the edit
        distance between the first ``i`` characters of `str1` and the first ``j``
        characters of `str2`.

        The recurrence relation is:

        .. math::
            dp[i, j] =
                \\begin{cases}
                    dp[i-1, j-1], & \\text{if } str1[i-1] = str2[j-1] \\\\
                    1 + \\min(dp[i-1, j], dp[i, j-1], dp[i-1, j-1]), & \\text{otherwise}
                \\end{cases}

        The final Levenshtein distance is stored in ``dp[-1, -1]``.

        Examples
        --------
        >>> LevenshteinDistance.distance("kitten", "sitting")
        3
        >>> LevenshteinDistance.distance("flaw", "lawn")
        2
        """
        len_str1 = len(str1) + 1
        len_str2 = len(str2) + 1

        dp = np.zeros((len_str1, len_str2), dtype=int)

        for i in range(len_str1):
            dp[i][0] = i
        for j in range(len_str2):
            dp[0][j] = j

        for i in range(1, len_str1):
            for j in range(1, len_str2):
                if str1[i - 1] == str2[j - 1]:
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
        """
        Check whether the similarity score exceeds the predefined threshold.

        Returns
        -------
        bool
            True if the computed similarity score is greater than or equal to
            the threshold, otherwise False.
        """
        return self.compute() >= self._threshold

    @staticmethod
    def _normalize_distance(
        distance: int | float, len_str1: int, len_str2: int
    ) -> float:
        """
        Normalize the raw Levenshtein distance to a [0, 1] range.

        Parameters
        ----------
        distance : int or float
            The raw Levenshtein distance between two strings.
        len_str1 : int
            Length of the first string.
        len_str2 : int
            Length of the second string.

        Returns
        -------
        float
            Normalized distance between 0 and 1, where 0 means identical strings
            and 1 means maximum dissimilarity.

        Notes
        -----
        The normalization is performed by dividing the distance by the maximum
        of the two string lengths:

        .. math::
            \\text{normalized_distance} = \\frac{distance}{\\max(len(str1), len(str2))}
        """
        max_len = max(len_str1, len_str2)
        if max_len == 0:
            return 0.0
        return distance / max_len

    def _similarity_score(
        self, distance: int | float, len_str1: int, len_str2: int
    ) -> float:
        """
        Convert a Levenshtein distance to a normalized similarity score.

        Parameters
        ----------
        distance : int or float
            The raw Levenshtein distance between the two strings.
        len_str1 : int
            Length of the first string.
        len_str2 : int
            Length of the second string.

        Returns
        -------
        float
            Similarity score between 0 and 1, where 1 means identical strings
            and 0 means completely different strings.

        Examples
        --------
        >>> LevenshteinDistance.similarity_score(0, 5, 5)
        1.0
        >>> LevenshteinDistance.similarity_score(3, 6, 6)
        0.5
        """
        normalized_distance = self._normalize_distance(distance, len_str1, len_str2)
        return 1.0 - normalized_distance


class FuzzyRatio(StringMetric):
    def __init__(
        self, str1: Union[str, Word], str2: Union[str, Word], threshold: float = 0.80
    ) -> None:
        super().__init__(str1, str2, threshold)

    def compute(self) -> float:
        return fuzz.ratio(self.str1, self.str2) / 100.0

    @property
    def passes_threshold(self) -> bool:
        return self.compute() >= self._threshold
