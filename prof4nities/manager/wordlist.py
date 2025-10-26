from typing import Union

import httpx

from prof4nities.enums import Language


class Wordlist:
    SOURCE_URL = "https://raw.githubusercontent.com/censor-text/profanity-list/refs/heads/main/list/"

    def __init__(self, language: Union[Language, str] = Language.ENGLISH) -> None:
        self.language = language.value if isinstance(language, Language) else language
        self.wordlist = self.fetch_wordlist()

    @property
    def wordlist_url(self) -> str:
        return f"{self.SOURCE_URL}{self.language}.txt"

    def fetch_wordlist(self) -> list[str]:
        """
        Fetch the remote wordlist for this manager's language, validate the response,
        and return the processed list of words.

        This method performs an HTTP GET to the URL stored on self.wordlist_url. If the
        request succeeds (HTTP 200) the response body is split into lines and those raw
        lines are handed to self.process_wordlist(...) to produce the final list that is
        returned.

        Returns:
            list[str]: The processed list of words.

        Raises:
            ValueError: If the HTTP response status code is not 200.
            httpx.RequestError: If the underlying HTTP request fails (propagated from httpx.get).

        Notes:
            - This method performs network I/O and may block; consider running it in an
              appropriate context for your application (e.g. background thread or async
              runner if adapted).
            - The exact normalization/filtering applied to the wordlist is defined by
              self.process_wordlist.
        """
        response = httpx.get(self.wordlist_url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch wordlist for language {self.language}")
        words = response.text.splitlines()

        return self.process_wordlist(words)

    @staticmethod
    def process_wordlist(words: list[str]) -> list[str]:
        """Normalize and deduplicate a list of words.

        Strip leading/trailing whitespace from each input string, convert to lowercase,
        and ignore empty or whitespace-only entries. The result is deduplicated and
        returned as a new list sorted in ascending lexicographical order.

        Parameters
        ----------
        words : list[str]
            List of strings to process.

        Returns
        -------
        list[str]
            Sorted list of unique, normalized words.

        Examples
        --------
        >>> process_wordlist([' Apple ', 'banana', 'apple', '', '  '])
        ['apple', 'banana']
        """
        return sorted(set(word.strip().lower() for word in words if word.strip()))

    def __len__(self) -> int:
        return len(self.wordlist)

    def __iter__(self):
        for word in self.wordlist:
            yield word

    def __getitem__(self, index: int) -> str:
        return self.wordlist[index]

    def __contains__(self, word: str) -> bool:
        return word.lower() in self.wordlist

    def __repr__(self) -> str:
        return f"Wordlist(language='{self.language}')"

    __str__ = __repr__
