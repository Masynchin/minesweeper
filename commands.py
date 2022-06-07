from typing import Iterator


class Commands(Iterator[str]):
    """Команды игрока."""

    def __init__(self):
        self.phrase = "\n> Введите координаты клетки: "

    def __iter__(self) -> Iterator[str]:
        while True:
            yield input(self.phrase)
