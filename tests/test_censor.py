from unittest.mock import patch

import pytest

from prof4nities import Censor
from prof4nities.models import Word, Character, Characters


@pytest.fixture
def censor_instance():
    return Censor(language="en")


def test_filter_word_profane(censor_instance: Censor):
    word = "fuck"
    result: Word = censor_instance.censor_word(word)
    assert result == word
    assert result.obfuscate_flag is True


def test_filter_word_non_profane(censor_instance: Censor):
    word = "hello"
    result: Word = censor_instance.censor_word(word)
    assert result == word
    assert result.obfuscate_flag is False


def test_filter_list(censor_instance: Censor):
    words = ["fuck", "hello", "vag"]
    results = censor_instance.censor_list(words)
    assert len(results) == 3
    assert results[0].obfuscate_flag is True
    assert results[1].obfuscate_flag is False
    assert results[2].obfuscate_flag is True


def test_call_with_string(censor_instance: Censor):
    text = "vag fuck hi"
    result = censor_instance(text, separator=" ")
    assert result == "*** **** hi"


def test_call_with_list(censor_instance: Censor):
    words = ["vag", "fuck", "hi"]
    result = censor_instance(words, separator=" ")
    assert result == "*** **** hi"


@pytest.mark.parametrize(
    "text",
    [("fvck"), ("fuc k"), ("f*u*c*k")],
)
def test_filter_word_edge_cases(text, censor_instance: Censor):
    result = censor_instance(text, stringify=False)

    assert isinstance(result, list), f"Expected list, got {type(result)}"
    assert all(isinstance(word, Word) for word in result), (
        "Expected all elements to be Word objects"
    )
    assert len(result) == 1
    assert result[0].obfuscate_flag, f"Expected '{text}' to be obfuscated"


def test_unstringify(censor_instance: Censor):
    badword = "fvck"
    text = "hello word " + badword

    result = censor_instance(text, stringify=False)

    assert isinstance(result, list), f"Expected list object, got {type(result)}"
    assert all(isinstance(word, Word) for word in result), (
        "Expected all elements to be Word objects"
    )
    assert result[-1].obfuscate_flag, f"Expected '{badword}' to be obfuscated"


def test_stringify_with_list(censor_instance: Censor):
    words = ["fuck", "hello", "vag"]
    censored_words = censor_instance(words, stringify=False)

    assert isinstance(censored_words, list), (
        f"Expected list, got {type(censored_words)}"
    )
    assert all(isinstance(word, Word) for word in censored_words), (
        "Expected all elements to be Word objects"
    )
    assert censored_words[0].obfuscate_flag, f"Expected '{words[0]}' to be obfuscated"
    assert not censored_words[1].obfuscate_flag, f"Expected '{words[1]}' to be clean"
    assert censored_words[2].obfuscate_flag, f"Expected '{words[2]}' to be obfuscated"


def test_no_stringify_with_string(censor_instance: Censor):
    text = "fuck hello vag"
    result = censor_instance(text, stringify=False)
    assert isinstance(result, list)
    assert all(isinstance(word, Word) for word in result), (
        "Expected all elements to be Word objects"
    )


def test_remove_punctuation(censor_instance: Censor):
    text = "fuck, hello! vag?"
    result = censor_instance.remove_punctuation(text)

    assert isinstance(result, str), f"Expected string, got {type(result)}"
    assert result == "fuck hello vag"


def test_check_profanity_in_text(censor_instance: Censor):
    text = "fuck hello vag"
    result = censor_instance.check_profanity_in_text(text)
    assert result

def test_censor_text_by_letters(censor_instance):
    text = "fuc k hello"

    # Prepare the mock return value for find_substring
    # We simulate that the profane word "fuck" was found spanning indices 0-4
    fake_found_letters = [
        Character(letter='f', index=0),
        Character(letter='u', index=1),
        Character(letter='c', index=2),
        Character(letter='k', index=4)
    ]

    # Patch Characters.find_substring to return our fake result
    with patch.object(Characters, 'find_substring', return_value=fake_found_letters):
        result = censor_instance.censor_text_by_characters(text)

    assert result == "***** hello"
