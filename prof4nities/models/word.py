from typing import TypedDict


class WordDict(TypedDict):
    text: str
    obfuscate: bool


class Word:
    """Word
    ----
    Lightweight value object representing a single word (string) with an optional
    "obfuscation" flag that controls how the word is presented when converted to
    string.

    Behavior
    - Stores the raw text in the `text` attribute (str).
    - Stores the display/obfuscation flag in `obfuscate_flag` (bool).
    - Instantiation with an empty string raises ValueError.
    - When converted to a string (str(word) or print(word)), the result is either
        the original text or an obfuscated version (a string of asterisks of equal
        length) depending on `obfuscate_flag`.
    - The `obfuscate()` method returns the obfuscated representation (asterisks),
        without changing the object's state.
    - `to_dict()` returns a plain mapping with keys "text" and "obfuscate".

    Operations and Protocols
    ------------------------
    - Equality:
            * word == other_word: True when both text are equal.
            * word == "some string": True when word.text == "some string".
    - Hashing:
            * Hash is derived from `text` only, making Word usable as dict keys or set
                members (note: two Words with equal text but different obfuscation flags
                will collide in hash).
    - Ordering:
            * Supports rich comparisons (<, <=, >, >=) with other Words (by text) and
                with plain strings.
    - Concatenation:
            * word + other_word  -> new Word with concatenated text and obfuscation
                flag set to the logical OR of the two flags.
            * word + "suffix"    -> new Word with concatenated text and original flag.
            * "prefix" + word    -> supported (returns a Word).
    - Sequence protocol:
            * len(word) -> length of the underlying text.
            * "sub" in word -> substring membership test against the text.
            * iter(word) -> yields characters of the text.
            * word[i] -> indexing/slicing forwarded to the underlying text.

    Parameters
    ----------
    word : str
            The textual content for the Word. Must be non-empty.
    obfuscate : bool, optional
            If True, the Word will present itself obfuscated (asterisks) when converted
            to a string. Defaults to False.

    Raises
    ------
    ValueError
            If `word` is an empty string.

    >>> w = Word("secret")
    >>> str(w)
    'secret'
    >>> w.obfuscate_flag = True
    >>> str(w)
    >>> w2 = Word("ing")
    >>> (w + w2).text
    'secreting'
    >>> (w == "secret")
    True
    >>> {"s": 1} if w in w2 else {}
    {}
    >>> w.to_dict()
    {"text": "secret", "obfuscate": True}
    """

    def __init__(self, word: str, obfuscate: bool = False) -> None:
        if len(word) == 0:
            raise ValueError("Word cannot be an empty string.")

        self.text = word
        self.obfuscate_flag = obfuscate

    def obfuscate(self) -> str:
        """
        Obfuscate the word by replacing each character in the instance's text with an asterisk.

        Returns
        -------
        str
            A string of asterisks with the same length as `self.text`.

        Examples
        --------
        If the instance's text is "secret", the method returns:

        >>> obj.text = "secret"
        >>> obj.obfuscate()
        '******'
        """
        return "*" * len(self.text)

    def to_dict(self) -> WordDict:
        return {"text": self.text, "obfuscate": self.obfuscate_flag}

    def __str__(self) -> str:
        if self.obfuscate_flag:
            return self.obfuscate()
        return self.text

    def __repr__(self) -> str:
        return f"Word({self.text!r})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Word):
            return self.text == other.text

        if isinstance(other, str):
            return self.text == other

        return False

    def __hash__(self) -> int:
        return hash(self.text)

    def __len__(self) -> int:
        return len(self.text)

    def __contains__(self, item: str) -> bool:
        return item in self.text

    def __lt__(self, other) -> bool:
        if isinstance(other, Word):
            return self.text < other.text
        if isinstance(other, str):
            return self.text < other
        return NotImplemented

    def __le__(self, other) -> bool:
        if isinstance(other, Word):
            return self.text <= other.text
        if isinstance(other, str):
            return self.text <= other
        return NotImplemented

    def __gt__(self, other) -> bool:
        if isinstance(other, Word):
            return self.text > other.text
        if isinstance(other, str):
            return self.text > other
        return NotImplemented

    def __ge__(self, other) -> bool:
        if isinstance(other, Word):
            return self.text >= other.text
        if isinstance(other, str):
            return self.text >= other
        return NotImplemented

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __ladd__(self, other) -> "Word":
        if isinstance(other, Word):
            return Word(
                self.text + other.text, self.obfuscate_flag or other.obfuscate_flag
            )
        if isinstance(other, str):
            return Word(self.text + other, self.obfuscate_flag)
        return NotImplemented

    def __radd__(self, other) -> "Word":
        if isinstance(other, str):
            return Word(other + self.text, self.obfuscate_flag)
        return NotImplemented

    def __iter__(self):
        for char in self.text:
            yield char

    def __getitem__(self, index: int | slice) -> str:
        return self.text[index]
