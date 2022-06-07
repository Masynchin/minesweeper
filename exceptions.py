class QuitGame(Exception):
    """Игрок вышел из игры с помощью команды."""


class BombDetonation(Exception):
    """Маслина поймана!"""


class RuleViolation(Exception):
    """Нарушение правил игры."""


class CellOutOfRange(RuleViolation):
    """Клетки с данной координатой не существует."""


class NotEnoughFlags(RuleViolation):
    """Открытие численной клетки, рядом с которой недостаточно флагов."""
