import os
import sys
from typing import TextIO


class Console(TextIO):
    """Консоль."""

    def __init__(self, system_name: str):
        self.out = sys.stdout
        self.system_name = system_name

    def write(self, *args, **kwargs) -> int:
        """Вывод текста в консоль."""
        return self.out.write(*args, **kwargs)

    def clear(self):
        """Очистка консоли."""
        if self.system_name == "nt":
            os.system("cls")
        else:
            os.system("clear")
