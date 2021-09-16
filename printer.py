import string

from cell import Cell
from field import Field


letters = string.digits[1:] + string.ascii_lowercase


def print_field(field: Field):
    """Вывести поле в консоль."""
    print(" " * 4 + " ".join(f"{letters[i]:<3}" for i in range(field.width)))
    for i, row in enumerate(field):
        letter = f"{letters[i]:<2}"
        print(letter, " ".join(_str_cell(cell) for cell in row))


def _str_cell(cell: Cell) -> str:
    """Строковое представление клетки.

    Данной строкой клетка будет выводится на экран.
    """
    if cell.is_open:
        if cell.is_empty:
            return "   "
        elif cell.value:
            return f" {cell.value} "
    elif cell.is_flagged:
        return "[F]"
    else:
        return "[ ]"
