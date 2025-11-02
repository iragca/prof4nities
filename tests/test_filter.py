import pytest

from prof4nities import Censor
from prof4nities.models import Word


@pytest.fixture
def filter_instance():
    return Censor(language="en")


def test_filter_word_profane(filter_instance: Censor):
    word = "nigga"
    result: Word = filter_instance.censor_word(word)
    assert result == word
    assert result.obfuscate_flag is True


def test_filter_word_non_profane(filter_instance: Censor):
    word = "hello"
    result: Word = filter_instance.censor_word(word)
    assert result == word
    assert result.obfuscate_flag is False


def test_filter_list(filter_instance: Censor):
    words = ["nigga", "hello", "vag"]
    results = filter_instance.censor_list(words)
    assert len(results) == 3
    assert results[0].obfuscate_flag is True
    assert results[1].obfuscate_flag is False
    assert results[2].obfuscate_flag is True


def test_call_with_string(filter_instance: Censor):
    text = "vag nigga hi"
    result = filter_instance(text, separator=" ")
    assert result == "*** ***** hi"


def test_call_with_list(filter_instance: Censor):
    words = ["vag", "nigga", "hi"]
    result = filter_instance(words, separator=" ")
    assert result == "*** ***** hi"


def test_filter_word_with_variants(filter_instance: Censor):
    text = "nigg4"

    result = filter_instance(text)

    assert result == "*" * len(text)


def test_unstringify(filter_instance: Censor):
    badword = "nigg4"
    text = "hello word " + badword

    result = filter_instance(text, stringify=False)

    assert isinstance(result, list), f"Expected list object, got {type(result)}"
    assert all(isinstance(word, Word) for word in result), (
        "Expected all elements to be Word objects"
    )
    assert result[-1].obfuscate_flag, f"Expected '{badword}' to be obfuscated"

def test_stringify_with_list(filter_instance: Censor):
    words = ["nigga", "hello", "vag"]
    censored_words = filter_instance(words, stringify=False)

    assert isinstance(censored_words, list), f"Expected list, got {type(censored_words)}"
    assert all(isinstance(word, Word) for word in censored_words), (
        "Expected all elements to be Word objects"
    )
    assert censored_words[0].obfuscate_flag, f"Expected '{words[0]}' to be obfuscated"
    assert not censored_words[1].obfuscate_flag, f"Expected '{words[1]}' to be clean"
    assert censored_words[2].obfuscate_flag, f"Expected '{words[2]}' to be obfuscated"


def test_no_stringify_with_string(filter_instance: Censor):
    text = "nigga hello vag"
    result = filter_instance(text, stringify=False)
    assert isinstance(result, list)
    assert all(isinstance(word, Word) for word in result), (
        "Expected all elements to be Word objects"
    )