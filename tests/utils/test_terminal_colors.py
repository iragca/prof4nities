import pytest

from src.utils import terminal_colors


@pytest.mark.parametrize(
    "text, color, expected",
    [
        ("Hello, World!", "red", "\033[31mHello, World!\033[0m"),
        ("Hello, World!", "green", "\033[32mHello, World!\033[0m"),
        ("Hello, World!", "blue", "\033[34mHello, World!\033[0m"),
        (3.14, "red", TypeError),
    ],
)
def test_terminal_colors(text, color, expected):
    if type(expected) is type and issubclass(expected, Exception):
        with pytest.raises(expected):
            terminal_colors.color_text(text, color)
        return

    result = terminal_colors.color_text(text, color)
    assert result == expected
