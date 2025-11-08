from typing import Union

class Character:
    def __init__(self, letter: str, index: int):
        self.letter = letter
        self.index = index

    def __repr__(self) -> str:
        return f"Letter({self.letter!r}, {self.index!r})"

    def __hash__(self) -> int:
        return hash((self.letter, self.index))

    def __eq__(self, other) -> bool:
        if isinstance(other, Character):
            return self.letter == other.letter and self.index == other.index

        if isinstance(other, str) and len(other) == 1:
            return self.letter == other

        return False

    @property
    def is_alpha(self) -> bool:
        return self.letter.isalpha()

    @property
    def is_digit(self) -> bool:
        return self.letter.isdigit()

    @property
    def is_space(self) -> bool:
        return self.letter.isspace()


class Characters(list):
    def __init__(self, data):
        if isinstance(data, str):
            # Automatically create Character objects from each char in the string
            data = [Character(letter=c, index=i) for i, c in enumerate(data)]
        elif all(isinstance(x, Character) for x in data):
            # Already Character objects — do nothing
            pass
        else:
            raise TypeError(
                "Characters must be initialized with a string or a list of Character objects."
            )
        super().__init__(data)

    def __repr__(self):
        joined = "".join(letter.letter for letter in self)
        return f"Characters({joined!r})"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, (Characters, str)):
            return False

        if len(self) != len(value):
            return False

        for i in range(len(self)):
            if self[i] != value[i]:
                return False

        return True

    def find_substring(self, substring: str) -> Union[list[Character], None]:
        if not isinstance(substring, str):
            return None

        start = 0
        result = []

        while start < len(self):
            # Check if the substring matches the current position
            if (
                "".join(
                    letter.letter for letter in self[start : start + len(substring)]
                )
                == substring
            ):
                result.extend(self[start : start + len(substring)])
                start += len(substring)
            else:
                start += 1

        return result if result else None
