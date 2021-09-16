from exceptions import QuitGame
from typing import Tuple

from field import Field
from printer import letters


def exec_command(command: str, field: Field):
    """Исполнение команды, введённой игроком."""
    if command.lower() in ("в", "e"):
        raise QuitGame("Выход")

    cell_x, cell_y, command_type = _parse_command(command)
    if not command_type:
        field.open_cell(cell_x, cell_y)
    elif command_type in ("ф", "f"):
        field.set_flag(cell_x, cell_y)
    elif command_type in ("о", "c"):
        field.remove_flag(cell_x, cell_y)


def _parse_command(command: str) -> Tuple[int, int, str]:
    """Разбор команды, введённой игрок."""
    cell_y, cell_x, *command_type = command.split()
    command_type = "".join(command_type).lower()

    # координаты клеток могут быть как цифрами, так и буквами,
    # которые записаны в printer.letters. Чтобы получить численные
    # координаты клетки, нужно взять индекс данных координат в printer.letters
    cell_x = letters.index(cell_x)
    cell_y = letters.index(cell_y)

    return cell_x, cell_y, command_type
