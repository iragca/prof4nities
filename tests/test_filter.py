import pytest

from prof4nities import Filter
from prof4nities.models import Word


@pytest.fixture
def filter_instance():
    return Filter(language="en")


def test_filter_word_profane(filter_instance: Filter):
    word = "nigga"
    result: Word = filter_instance.filter_word(word)
    assert result == word
    assert result.obfuscate_flag is True


def test_filter_word_non_profane(filter_instance: Filter):
    word = "hello"
    result: Word = filter_instance.filter_word(word)
    assert result == word
    assert result.obfuscate_flag is False


def test_filter_list(filter_instance: Filter):
    words = ["nigga", "hello", "vag"]
    results = filter_instance.filter_list(words)
    assert len(results) == 3
    assert results[0].obfuscate_flag is True
    assert results[1].obfuscate_flag is False
    assert results[2].obfuscate_flag is True


def test_call_with_string(filter_instance: Filter):
    text = "vag nigga hi"
    result = filter_instance(text, separator=" ")
    assert result == "*** ***** hi"


def test_call_with_list(filter_instance: Filter):
    words = ["vag", "nigga", "hi"]
    result = filter_instance(words, separator=" ")
    assert result == "*** ***** hi"


def test_filter_word_with_variants(filter_instance: Filter):
    text = "nigg4"

    result = filter_instance(text)

    assert result == "*" * len(text)


def test_unstringify(filter_instance: Filter):
    badword = "nigg4"
    text = "hello word " + badword

    result = filter_instance(text, stringify=False)

    assert isinstance(result, list), f"Expected list object, got {type(result)}"
    assert all(isinstance(word, Word) for word in result), (
        "Expected all elements to be Word objects"
    )
    assert result[-1].obfuscate_flag, f"Expected '{badword}' to be obfuscated"
