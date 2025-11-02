import pytest

from prof4nities.models import FuzzyRatio, LevenshteinDistance, Word


def test_levenshtein_distance():
    str1 = "kitten"
    str2 = "sitting"
    distance_metric = LevenshteinDistance(str1, str2, threshold=0.80)
    distance = distance_metric.compute()
    assert isinstance(distance, float)
    assert distance_metric.passes_threshold is False, (
        f"Expected False but got True for distance {distance} with threshold 0.80"
    )

    distance_metric_threshold = LevenshteinDistance(str1, str2, threshold=0.20)
    distance = distance_metric_threshold.compute()
    assert isinstance(distance, float)
    assert distance_metric_threshold.passes_threshold is True, (
        f"Expected True but got False for distance {distance} with threshold 0.20"
    )


def test_fuzzy_ratio():
    str1 = "kitten"
    str2 = "sitting"
    ratio_metric = FuzzyRatio(str1, str2, threshold=0.90)
    ratio = ratio_metric.compute()
    assert isinstance(ratio, float)
    assert ratio_metric.passes_threshold is False, (
        f"Expected False but got True for ratio {ratio} with threshold 0.90"
    )

    ratio_metric_threshold = FuzzyRatio(str1, str2, threshold=0.5)
    ratio = ratio_metric_threshold.compute()
    assert ratio_metric_threshold.passes_threshold is True, (
        f"Expected True but got False for ratio {ratio} with threshold 0.5"
    )


def test_metric_with_word_objects():
    word1 = Word("hello")
    word2 = Word("hallo")
    word_obj1 = FuzzyRatio(word1, word2, threshold=0.8)
    ratio = word_obj1.compute()
    assert isinstance(ratio, float)
    assert word_obj1.passes_threshold is True

    word_obj2 = LevenshteinDistance(word1, word2, threshold=0.20)
    distance = word_obj2.compute()
    assert isinstance(distance, float)
    assert word_obj2.passes_threshold is True


def test_levenshtein_distance_identical_strings():
    str1 = "example"
    str2 = "example"
    distance_metric = LevenshteinDistance(str1, str2, threshold=0.0)
    distance = distance_metric.compute()
    assert distance == 1
    assert distance_metric.passes_threshold is True


def test_fuzzy_ratio_identical_strings():
    str1 = "example"
    str2 = "example"
    ratio_metric = FuzzyRatio(str1, str2, threshold=1.0)
    ratio = ratio_metric.compute()
    assert ratio == 1.0
    assert ratio_metric.passes_threshold is True


def test_levenshtein_distance_empty_strings():
    str1 = ""
    str2 = ""
    distance_metric = LevenshteinDistance(str1, str2, threshold=0.0)
    distance = distance_metric.compute()
    assert distance == 1.0
    assert distance_metric.passes_threshold is True


def test_fuzzy_ratio_empty_strings():
    str1 = ""
    str2 = ""
    ratio_metric = FuzzyRatio(str1, str2, threshold=1.0)
    ratio = ratio_metric.compute()
    assert ratio == 1.0
    assert ratio_metric.passes_threshold is True


def test_levenshtein_normalized_distance():
    str1 = "flaw"
    str2 = "lawn"
    distance_metric = LevenshteinDistance(str1, str2, threshold=0.5)
    distance = distance_metric.compute()
    normalized_distance = distance / max(len(str1), len(str2))
    assert isinstance(normalized_distance, float)
    assert distance_metric.passes_threshold is (normalized_distance <= 0.5)


@pytest.mark.parametrize(
    "str1, str2, expected_distance",
    [
        ("kitten", "sitting", 3),
        ("flaw", "lawn", 2),
        ("intention", "execution", 5),
        ("", "", 0),
        ("a", "", 1),
        ("", "a", 1),
    ],
)
def test_levenshtein_distance_method(str1, str2, expected_distance):
    distance = LevenshteinDistance._distance(str1, str2)
    assert isinstance(distance, int)
    assert distance == expected_distance


@pytest.mark.parametrize(
    "str1, str2, distance, expected_ratio",
    [
        ("kitten", "sitting", 4, 0.571428571),
        ("flaw", "lawn", 3, 0.75),
        ("intention", "execution", 5, 0.555555556),
        ("", "", 0, 0.0),
        ("a", "", 1, 1.0),
        ("", "a", 1, 1.0),
    ],
)
def test_levenshtein_normalize_distance_method(str1, str2, distance, expected_ratio):
    len_str1 = len(str1)
    len_str2 = len(str2)

    normalized_distance = LevenshteinDistance._normalize_distance(
        distance, len_str1, len_str2
    )
    assert isinstance(normalized_distance, float)
    assert normalized_distance == pytest.approx(expected_ratio, rel=1e-6)


@pytest.mark.parametrize(
    "str1, str2, distance, expected_similarity",
    [
        ("kitten", "sitting", 4, 0.428571429),
        ("flaw", "lawn", 3, 0.25),
        ("intention", "execution", 5, 0.444444444),
        ("", "", 0, 1.0),
        ("a", "", 1, 0.0),
        ("", "a", 1, 0.0),
    ],
)
def test_levenshtein_similarity_score(str1, str2, distance, expected_similarity):
    distance_metric = LevenshteinDistance(str1, str2, threshold=0.5)

    similarity = distance_metric._similarity_score(distance, len(str1), len(str2))

    assert isinstance(similarity, float)
    assert similarity == pytest.approx(expected_similarity, rel=1e-6)
