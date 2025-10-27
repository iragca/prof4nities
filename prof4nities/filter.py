from typing import Union

from .models import Word


class Filter:
    def __init__(self, language: str = "en") -> None:
        self.language = language

    def filter_list(self, words: list[str]) -> list[Word]:
        return [self.filter_word(word) for word in words]

    def filter_word(self, word: str) -> Word:
        return Word(word, obfuscate=False)

    def __call__(self, text: Union[list[str], str]) -> Union[list[Word], Word]:
        if isinstance(text, list):
            return self.filter_list(text)
        elif isinstance(text, str):
            return self.filter_word(text)
        else:
            raise TypeError("Input must be a list of strings or a single string.")
