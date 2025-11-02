from unittest.mock import PropertyMock

import pytest

from prof4nities import Wordlist


@pytest.fixture
def wordlist_instance(tmp_path):
    wl = Wordlist(language="en", cache_kwargs={"directory": tmp_path})
    return wl


def test_fetch_wordlist(mocker, wordlist_instance: Wordlist):
    wl = wordlist_instance

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = "badword1\nbadword2\nbadword3"

    mocker.patch("httpx.get", return_value=mock_response)
    mocker.patch.object(
        type(wl._cache), "exists", new_callable=PropertyMock, return_value=False
    )

    words = wl.fetch_wordlist()
    assert words == ["badword1", "badword2", "badword3"]


def test_fetch_wordlist_failure(mocker, wordlist_instance: Wordlist):
    wl = wordlist_instance
    language = wl.language

    mock_response = mocker.Mock()
    mock_response.status_code = 404

    mocker.patch("httpx.get", return_value=mock_response)
    mocker.patch.object(
        type(wl._cache), "exists", new_callable=PropertyMock, return_value=False
    )

    with pytest.raises(
        ValueError, match=f"Failed to fetch wordlist for language {language}"
    ):
        wl.fetch_wordlist()
