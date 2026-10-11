from enum import StrEnum
import shutil
import re


ANSI_ESCAPE = re.compile(r"\033\[[0-9;?]*[A-Za-z]")

# commands
HOME = "\033[H"
CLEAR = "\033[2J"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
RESET_COLOR = "\033[0m"

# special characters
CIRCLE = "\u25cf"  # ●
BIG_CIRCLE = "\u2b24"  # ⬤
# grid
HORIZONTAL = "\u2500"   # ─
VERTICAL = "\u2502"  # │
DOWN_RIGHT = "\u250c"  # ┌
DOWN_LEFT = "\u2510"  # ┐
UP_RIGHT = "\u2514"  # ┌
UP_LEFT = "\u2518"  # ┐
VERTICAL_HORIZONTAL = "\u253c"  # ┼
VERTICAL_LEFT = "\u2524"  # ┤
VERTICAL_RIGHT = "\u251c"  # ├
HORIZONTAL_UP = "\u2534"  # ┴
HORIZONTAL_DOWN = "\u252c"  # ┬


class Color(StrEnum):
    RED = "\033[31m"
    BLUE = "\033[34m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    ORANGE = "\033[38;5;166m"


# helpers
def print_centered(msg: str, row_offset: int = 0, column_offset: int = 0) -> None:
    columns, rows = shutil.get_terminal_size()
    row = rows // 2 + row_offset
    column = max((columns - _visible_len(msg)) // 2 + 1, 1) + column_offset
    print(f"\033[{row};{column}H{msg}", end="", flush=True)


def _visible_len(msg: str) -> int:
    return len(ANSI_ESCAPE.sub("", msg))


def clear() -> None:
    print(CLEAR, end="", flush=True)


def home() -> None:
    print(HOME, end="", flush=True)


def hide_cursor() -> None:
    print(HIDE_CURSOR, end="", flush=True)


def show_cursor() -> None:
    print(SHOW_CURSOR, end="", flush=True)
