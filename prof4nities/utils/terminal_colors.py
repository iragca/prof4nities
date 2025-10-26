from enum import Enum

from .check_type import check_type


class Colors(Enum):
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"


def color_text(text: str, color: Colors | str) -> str:
    """Wrap text in ANSI color codes.

    args:
        text (str): The text to color.
        color (Colors | str): The color to apply.

    returns:
        str: The colored text wrapped in ANSI codes.

    raises:
        TypeError: If the text is not a string or the color is not a Colors enum or string.
    """

    check_type(text, str, "text")
    check_type(color, (Colors, str), "color")

    if isinstance(color, Colors):
        return f"{color.value}{text}{Colors.RESET.value}"

    color_map = {
        "red": Colors.RED,
        "green": Colors.GREEN,
        "yellow": Colors.YELLOW,
        "blue": Colors.BLUE,
        "magenta": Colors.MAGENTA,
        "cyan": Colors.CYAN,
        "white": Colors.WHITE,
    }

    if isinstance(color, str):
        color = color.lower()

        if color not in color_map:
            raise ValueError(f"Color '{color}' is not supported.")

        return f"{color_map[color].value}{text}{Colors.RESET.value}"
