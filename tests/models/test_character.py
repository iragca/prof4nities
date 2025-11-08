from prof4nities.models import Character, Characters


def test_letter_equality():
    letter_a1 = Character("a", 0)
    letter_a2 = Character("a", 0)
    letter_b = Character("b", 1)

    assert letter_a1 == letter_a2
    assert letter_a1 != letter_b
    assert letter_a1 == "a"
    assert letter_b != "a"


def test_letter_properties():
    letter_a = Character("a", 0)
    letter_1 = Character("1", 1)
    letter_space = Character(" ", 2)

    assert letter_a.is_alpha is True
    assert letter_a.is_digit is False
    assert letter_a.is_space is False

    assert letter_1.is_alpha is False
    assert letter_1.is_digit is True
    assert letter_1.is_space is False

    assert letter_space.is_alpha is False
    assert letter_space.is_digit is False
    assert letter_space.is_space is True


def test_character_list_find_substring():
    text = "example fuck text"
    letters = Characters(text)

    found_letters = letters.find_substring("fuck")
    assert found_letters is not None
    assert len(found_letters) == 4
    assert "".join(letter.letter for letter in found_letters) == "fuck"


def test_character_list_fragmented_word():
    text = "example fuc k text"
    letters = [Character(letter=c, index=i) for i, c in enumerate(text)]
    no_spaces = Characters([letter for letter in letters if not letter.is_space])

    found_letters = no_spaces.find_substring("fuck")
    assert found_letters is not None
    assert len(found_letters) == 4
    assert "".join(letter.letter for letter in found_letters) == "fuck"


def test_character_list_equality():
    text = "example text"
    letters = Characters(text)

    assert letters == "example text"
    assert letters == Characters("example text")
    assert letters != Characters("different text")
