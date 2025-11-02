from prof4nities.models import FuzzyRatio, LevenshteinDistance, Word


def test_levenshtein_distance():
    str1 = "kitten"
    str2 = "sitting"
    distance_metric = LevenshteinDistance(str1, str2, threshold=0.80)
    distance = distance_metric.compute()
    assert isinstance(distance, int)
    assert distance_metric.passes_threshold is False, f"Expected False but got True for distance {distance} with threshold 0.80"

    distance_metric_threshold = LevenshteinDistance(str1, str2, threshold=0.20)
    distance = distance_metric_threshold.compute()
    assert isinstance(distance, int)
    assert distance_metric_threshold.passes_threshold is True, f"Expected True but got False for distance {distance} with threshold 0.20"


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
    assert isinstance(distance, int)
    assert word_obj2.passes_threshold is True
