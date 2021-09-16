class BombDetonation(Exception):
    """Маслина поймана!"""


class CellOutOfRange(Exception):
    """Клетки с данной координатой не существует."""


class QuitGame(Exception):
    """Игрок вышел из игры с помощью команды."""


class NotEnoughFlags(Exception):
    """Открытие численной клетки, рядом с которой недостаточно флагов."""
