from typing import TextIO


class Congratulation:
    """Поздравление о завершении игры."""

    def __init__(self, seconds: int):
        self.seconds = seconds

    def print(self, out: TextIO):
        """Печать поздравления."""
        if 11 <= self.seconds <= 19 or self.seconds % 10 in (0, 5, 6, 7, 8, 9):
            template = f"Поздравляем, вы прошли игру за {self.seconds} секунд!"
        elif self.seconds % 10 in (2, 3, 4):
            template = f"Поздравляем, вы прошли игру за {self.seconds} секунды!"
        elif self.seconds % 10 == 1:
            template = f"Поздравляем, вы прошли игру за {self.seconds} секунду!"
        out.write(f"{template}\n")
