import os
import time
from typing import Iterator

from commander import exec_command
from console import Console
from field import Field
from exceptions import BombDetonation, CellOutOfRange, NotEnoughFlags, QuitGame


class Game:
    """Игра."""

    def __init__(
        self, commands: Iterator[str], field: Field, console: Console
    ):
        self.commands = commands
        self.field = field
        self.console = console

    def run(self):
        """Запуск игры."""
        start_time = time.time()
        while True:
            self.field.print()
            for command in self.commands:
                try:
                    exec_command(command, self.field)
                except QuitGame:
                    self.console.clear()
                    exit(0)
                except CellOutOfRange:
                    print("Неверные координаты клетки!")
                except NotEnoughFlags:
                    print("Недостаточно флагов для открытия соседей!")
                except BombDetonation:
                    print("К сожалению, вы взорвались!")
                    time.sleep(3)
                    exit(0)
                else:
                    break

            self.console.clear()
            if self.field.is_win():
                break

        end_time = time.time()
        elapsed_time = int(end_time - start_time)

        template = get_congratulation_template(elapsed_time)
        print(template.format(elapsed_time=elapsed_time))


def get_congratulation_template(elapsed_time: int) -> str:
    """
    Получение шаблона при победе,
    в зависимости от окончания числа секунд игры.
    """
    if 11 <= elapsed_time <= 19 or elapsed_time % 10 in (0, 5, 6, 7, 8, 9):
        template = "Поздравляем, вы прошли игру за {elapsed_time} секунд!"
    elif elapsed_time % 10 in (2, 3, 4):
        template = "Поздравляем, вы прошли игру за {elapsed_time} секунды!"
    elif elapsed_time % 10 == 1:
        template = "Поздравляем, вы прошли игру за {elapsed_time} секунду!"

    return template
