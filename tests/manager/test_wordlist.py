import pytest

from prof4nities import Wordlist


def test_wordlist_url():
    language = "en"
    wl_en = Wordlist(language=language)
    assert (
        wl_en.wordlist_url
        == f"https://raw.githubusercontent.com/censor-text/profanity-list/refs/heads/main/list/{language}.txt"
    )


def test_fetch_wordlist(mocker):
    language = "en"
    wl = Wordlist(language=language)

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = "badword1\nbadword2\nbadword3"

    mocker.patch("httpx.get", return_value=mock_response)

    words = wl.fetch_wordlist()
    assert words == ["badword1", "badword2", "badword3"]


def test_fetch_wordlist_failure(mocker):
    language = "en"
    wl = Wordlist(language=language)

    mock_response = mocker.Mock()
    mock_response.status_code = 404

    mocker.patch("httpx.get", return_value=mock_response)

    with pytest.raises(ValueError, match=f"Failed to fetch wordlist for language {language}"):
        wl.fetch_wordlist()