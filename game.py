import os
import time
from typing import Iterator

from commander import exec_command
from congratulation import Congratulation
from console import Console
from field import Field
from exceptions import BombDetonation, RuleViolation, QuitGame


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
                except RuleViolation as e:
                    print(e)
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

        Congratulation(elapsed_time).print(self.console)
