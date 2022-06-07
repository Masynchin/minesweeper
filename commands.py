from typing import Iterable


class Commands(Iterable[str]):
    """Команды игрока."""

    def __init__(self):
        self.phrase = "\n> Введите координаты клетки: "

    def __iter__(self) -> Iterable[str]:
        while True:
            yield input(self.phrase)
