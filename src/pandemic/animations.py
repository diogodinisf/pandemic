import shutil
from time import sleep

from pandemic.terminal_helper import  hide_cursor, show_cursor, home, clear, Color, BIG_CIRCLE, RESET_COLOR


def loading_screen(*, repetions: int = 1) -> None:
    wait = 0.15
    columns, rows = shutil.get_terminal_size()
    row = rows // 2
    total_width = len(Color)
    start_column = max((columns - total_width) // 2 + 1, 1)

    hide_cursor()
    clear()

    for repetion in range(repetions):
        for index, color in enumerate(Color):
            column = start_column + index
            print(f"\033[{row};{column}H{color}{BIG_CIRCLE}", end="", flush=True)
            sleep(wait)

        for index in range(len(Color)):
            column = start_column + index
            print(f"\033[{row};{column}H ", end="", flush=True)
            sleep(wait)

        if repetion == repetions - 1:
            break

        for index, color in reversed(list(enumerate(Color))):
            column = start_column + index
            print(f"\033[{row};{column}H{color}{BIG_CIRCLE}", end="", flush=True)
            sleep(wait)

        for index in reversed(range(len(Color))):
            column = start_column + index
            print(f"\033[{row};{column}H ", end="", flush=True)
            sleep(wait)

    print(RESET_COLOR, end="", flush=True)
    show_cursor()
    home()
    clear()
