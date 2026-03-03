import re
from functools import lru_cache
from typing import Optional, Union

import nltk
from nltk.corpus import wordnet

from .config import Environment
from .enums import Language
from .manager import Wordlist
from .models import FuzzyRatio, Character, Characters, LevenshteinDistance, Word
from .utils import Pipeline, check_types


class Censor:
    """
    Detects and flags profane or inappropriate words in text.

    The `Censor` class provides utilities to identify, evaluate, and optionally
    censor words or lists of words using multiple similarity checks including
    Levenshtein distance and fuzzy string ratios. It can process individual
    words, tokenized lists, or full text strings.

    Parameters
    ----------
    language : str or Language, optional
        The language code or `Language` enum used to select the appropriate
        profanity wordlist. Defaults to "en" (English).

    Attributes
    ----------
    language : str
        The language code used for censorship.
    wordlist : Wordlist
        The loaded profanity or sensitive-word list for the given language.
    """

    def __init__(self, language: Union[str, Language] = "en") -> None:
        self.language = language.value if isinstance(language, Language) else language
        self.wordlist = Wordlist(language=self.language)
        nltk.download("wordnet")

    def censor_list(self, words: list[str], separator: str = " ") -> list[Word]:
        """
        Evaluate a list of words for profanity or inappropriate content.

        Parameters
        ----------
        words : list of str
            A list of words to be evaluated.

        Returns
        -------
        list of Word
            A list of `Word` objects where each entry contains the original word
            and a boolean flag indicating whether it is profane.

        Raises
        ------
        TypeError
            If `words` is not a list of strings.
        """
        if not isinstance(words, list):
            raise TypeError("Input must be a list of strings.")

        return [self.censor_word(word) for word in words]

    @check_types
    def censor_word(self, word: str) -> Word:
        """
        Evaluate a single word for profanity or inappropriate content.

        Uses multiple strategies to determine if a word is profane:
        direct lookup in the profanity wordlist, WordNet validation,
        Levenshtein distance, and fuzzy ratio similarity metrics.

        Parameters
        ----------
        word : str
            The input word to check.

        Returns
        -------
        Word
            A `Word` object indicating whether the word is profane.

        Raises
        ------
        TypeError
            If `word` is not a string.
        """
        if not isinstance(word, str):
            raise TypeError("Input must be a string.")

        if word.lower() in self.wordlist:
            return Word(word, True)

        if wordnet.synsets(word):
            return Word(word, False)

        for profane_word in self.wordlist:
            compared_word = self.normalize_text(self.remove_punctuation(word.lower()))
            distance = LevenshteinDistance(
                str1=compared_word,
                str2=profane_word,
                threshold=Environment.LEVENSHTEIN_THRESHOLD.value,
            )

            fuzzy_ratio = FuzzyRatio(
                str1=compared_word,
                str2=profane_word,
                threshold=Environment.FUZZY_RATIO_THRESHOLD.value,
            )

            if distance.passes_threshold or fuzzy_ratio.passes_threshold:
                return Word(word, True)

        return Word(word, False)

    def __call__(
        self,
        text: Union[list[str], str],
        separator: Optional[str] = " ",
        stringify: bool = True,
    ) -> str | list[Word]:
        """
        Process text or a list of words for censorship.

        This method serves as a callable interface for the class,
        allowing instances of `Censor` to be used like functions.

        Parameters
        ----------
        text : str or list of str
            The input text or list of words to evaluate.
        separator : str or None, optional
            The word separator used for tokenization. Defaults to a space (" ").
            If `text` is a list, this parameter must be provided.
            If `text` is a single word, this can be `None`.
        stringify : bool, optional
            Whether to return a single censored string (`True`) or a list of
            `Word` objects (`False`). Defaults to `True`.

        Returns
        -------
        str or list of Word
            If `stringify` is True, returns a censored string representation of
            the input text. Otherwise, returns a list of `Word` objects.

        Raises
        ------
        ValueError
            If invalid input parameter combinations are provided.
        """
        if isinstance(text, list):
            words = self.censor_list(text)
            return (
                self.stringify(tuple(words), separator or " ") if stringify else words
            )

        if isinstance(text, str):
            if separator is None:
                return self.censor_text_by_characters(text)

            tokens = self.tokenizer(text, separator=separator or " ")
            words = self.censor_list(tokens)
            return (
                self.stringify(tuple(words), separator or " ") if stringify else words
            )

        raise ValueError(
            "Invalid input: 'text' must be either a string or a list of strings."
        )

    @staticmethod
    @lru_cache(maxsize=None)
    def stringify(words: Union[tuple[Word], Word], separator: str = " ") -> str:
        """
        Convert a list or tuple of `Word` objects into a single string.

        Parameters
        ----------
        words : tuple of Word or Word
            A single `Word` instance or tuple of `Word` instances to stringify.
        separator : str, optional
            The string used to join multiple words. Defaults to a space (" ").

        Returns
        -------
        str
            A string representation of the censored or clean text.
        """
        if isinstance(words, tuple):
            return separator.join(str(word) for word in words)
        return str(words)

    @staticmethod
    @lru_cache(maxsize=None)
    def tokenizer(text: str, separator: str = " ") -> list[str]:
        """
        Tokenize text into a list of words using a simple pipeline.

        Parameters
        ----------
        text : str
            The input text to be tokenized.
        separator : str, optional
            The delimiter used to split text into tokens. Defaults to a space (" ").

        Returns
        -------
        list of str
            A list of tokens extracted from the input text.
        """
        pipeline = Pipeline(
            [
                str.strip,
                lambda x: x.split(separator),
            ]
        )
        return pipeline(text)

    def remove_punctuation(self, text: str) -> str:
        """
        Remove punctuation from the input text.

        Parameters
        ----------
        text : str
            The input text from which to remove punctuation.

        Returns
        -------
        str
            The text with punctuation removed.
        """
        return re.sub(r"[^\w\s]", "", text)

    def check_profanity_in_text(self, text: str) -> bool:
        """
        Check if any profane words from the wordlist are present in the text.

        Parameters
        ----------
        text : str
            The input text to check for profane words.
        wordlist : Wordlist
            The profanity wordlist to check against.

        Returns
        -------
        bool
            True if any profane words are found, False otherwise.
        """
        for profane_word in self.wordlist:
            pattern = r"\b" + re.escape(profane_word) + r"\b"
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def censor_text_by_characters(self, text: str) -> str:
        """
        Detect and censor profane words even when split by spaces or symbols.
        """
        letters = [Character(letter=c, index=i) for i, c in enumerate(text)]
        no_spaces = Characters([letter for letter in letters if not letter.is_space])

        # Convert text into a list so we can mutate characters
        censored_chars = list(text)

        for profane_word in self.wordlist:
            found_letters = no_spaces.find_substring(profane_word)
            if not found_letters:
                continue

            start_index = found_letters[0].index
            end_index = found_letters[-1].index

            for i in range(start_index, end_index + 1):
                censored_chars[i] = "*"

        return "".join(censored_chars)

    def normalize_text(self, text: str) -> str:
        """
        fuuuck -> fuck, looool -> lol
        """
        return re.sub(r'(.)\1+', r'\1', text, flags=re.IGNORECASE)

