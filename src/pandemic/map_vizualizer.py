from pandemic.terminal_helper import (HORIZONTAL, VERTICAL, DOWN_LEFT, DOWN_RIGHT,
                                      UP_LEFT, UP_RIGHT, VERTICAL_LEFT, VERTICAL_RIGHT,
                                      HORIZONTAL_DOWN, HORIZONTAL_UP, VERTICAL_HORIZONTAL,
                                      BIG_CIRCLE, RESET_COLOR, Color)
from pandemic.types import Cell


def draw_map(map: list[list[Cell]]) -> None:
    width = len(map)
    height = len(map[0])
    
    draw = ""
    draw += _get_top_row(width)

    for row in range(height):
        draw += _get_cells_row(row, map)    

        if row == height - 1:
            break

        draw += _get_middle_row(width)
    
    draw += _get_bottom_row(width)

    print(draw, flush=True)


def _get_top_row(width: int) -> str:
    return f"{DOWN_RIGHT}{HORIZONTAL_DOWN.join([HORIZONTAL * 2] * width)}{DOWN_LEFT}\n"


def _get_middle_row(width: int) -> str:
    return f"{VERTICAL_RIGHT}{VERTICAL_HORIZONTAL.join([HORIZONTAL * 2] * width)}{VERTICAL_LEFT}\n"


def _get_bottom_row(width: int) -> str:
    return f"{UP_RIGHT}{HORIZONTAL_UP.join([HORIZONTAL * 2] * width)}{UP_LEFT}"


def _get_cells_row(row: int, map: int) -> str:
    width = len(map)
    draw = VERTICAL

    for index in range(width):
        cell = map[index][row]
        empty_cell = False

        if cell.alive is False:
            empty_cell = True
        if cell.immune > 0:
            if cell.sick > 0:  
                color = Color.ORANGE
            else:
                color = Color.GREEN
        elif cell.sick > 0:
            color = Color.RED
        elif cell.infected > 0:
            color = Color.YELLOW
        else:
            color = Color.BLUE

        if empty_cell:
            draw += '  '
        else:
            draw += color + BIG_CIRCLE + RESET_COLOR + ' '

        draw += VERTICAL

    return draw + "\n"
