import pytest

from prof4nities.models import Word


@pytest.fixture
def word_fixture():
    return Word("example", obfuscate=False)


@pytest.fixture
def bad_word_fixture():
    return Word("badword", obfuscate=True)


def test_word_str_equality(word_fixture):
    assert word_fixture == "example"


def test_word_obfuscation_equality(bad_word_fixture):
    assert bad_word_fixture == "badword"
    assert str(bad_word_fixture) == "*******"


def test_init_empty_raises():
    with pytest.raises(ValueError):
        Word("")


def test_obfuscate_and_str_behavior():
    w = Word("secret")
    assert w.obfuscate() == "******"
    assert str(w) == "secret"

    w.obfuscate_flag = True
    assert str(w) == "******"


def test_to_dict_and_repr():
    w = Word("a", obfuscate=True)
    assert w.to_dict() == {"text": "a", "obfuscate": True}
    assert repr(Word("hi")) == "Word('hi')"


def test_equality_and_hashing():
    w1 = Word("test")
    w2 = Word("test", obfuscate=True)
    assert w1 == w2
    assert w1 == "test"
    assert w2 == "test"
    assert hash(w1) == hash(w2)

    s = {w1, w2}
    assert len(s) == 1  # same text -> same hash/identity for set membership


def test_ordering_and_inequality():
    a = Word("a")
    b = Word("b")

    assert a < b
    assert a <= "a"
    assert b > "a"
    assert b >= "b"
    assert not (a != "a")  # __ne__ is logical inverse of __eq__


def test_concatenation_dunder_methods():
    w1 = Word("hello", obfuscate=True)
    w2 = Word("world", obfuscate=False)

    combined = w1.__ladd__(w2)
    assert isinstance(combined, Word)
    assert combined.text == "helloworld"
    assert combined.obfuscate_flag is True  # True or False -> True

    combined_str = w1.__ladd__("!")
    assert combined_str.text == "hello!"
    assert combined_str.obfuscate_flag is True

    prefixed = w1.__radd__("pre-")
    assert prefixed.text == "pre-hello"
    assert prefixed.obfuscate_flag is True

    # unsupported types return NotImplemented from dunder methods
    assert w1.__ladd__(123) is NotImplemented
    assert w1.__radd__(123) is NotImplemented


def test_sequence_protocol_and_iteration():
    w = Word("hello")
    assert len(w) == 5
    assert "ell" in w
    assert list(iter(w)) == list("hello")
    assert w[1] == "e"
    assert w[1:4] == "ell"
