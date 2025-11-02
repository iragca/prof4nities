from functools import lru_cache
from typing import Optional, Union

from nltk.corpus import wordnet

from .config import Environment
from .enums import Language
from .manager import Wordlist
from .models import FuzzyRatio, LevenshteinDistance, Word
from .utils import Pipeline, check_types


class Filter:
    def __init__(self, language: Union[str, Language] = "en") -> None:
        self.language = language.value if isinstance(language, Language) else language
        self.wordlist = Wordlist(language=self.language)

    def filter_list(self, words: list[str]) -> list[Word]:
        if not isinstance(words, list):
            raise TypeError("Input must be a list of strings.")

        return [self.filter_word(word) for word in words]

    @check_types
    def filter_word(self, word: str) -> Word:
        if not isinstance(word, str):
            raise TypeError("Input must be a string.")

        if word.lower() in self.wordlist:
            return Word(word, True)

        if wordnet.synsets(word):
            return Word(word, False)

        for profane_word in self.wordlist:
            distance = LevenshteinDistance(
                str1=word.lower(),
                str2=profane_word,
                threshold=Environment.LEVENSHTEIN_THRESHOLD.value,
            )

            fuzzy_ratio = FuzzyRatio(
                str1=word.lower(),
                str2=profane_word,
                threshold=Environment.FUZZY_RATIO_THRESHOLD.value,
            )

            if distance.passes_threshold or fuzzy_ratio.passes_threshold:
                return Word(word, True)

        return Word(word, False)

    def __call__(
        self, text: Union[list[str], str], separator: Optional[str] = " "
    ) -> str:
        if isinstance(text, list):
            words = self.filter_list(text)
            return self.stringify(tuple(words), separator or " ")

        elif isinstance(text, str):
            if separator is None:
                return str(self.filter_word(text))
            tokens = self.tokenizer(text, separator=separator)
            return self.stringify(tuple(self.filter_list(tokens)), separator)

        raise ValueError(
            "Invalid input parameters. If 'text' is a list, 'separator' must be provided. If 'text' is a string, 'separator' can be None."
        )

    @staticmethod
    @lru_cache(maxsize=None)
    def stringify(words: Union[tuple[Word], Word], separator: str = " ") -> str:
        if isinstance(words, tuple):
            return separator.join(str(word) for word in words)
        return str(words)

    @staticmethod
    @lru_cache(maxsize=None)
    def tokenizer(text: str, separator: str = " ") -> list[str]:
        pipeline = Pipeline(
            [
                str.strip,
                lambda x: x.split(separator),
            ]
        )
        return pipeline(text)
