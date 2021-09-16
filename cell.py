from dataclasses import dataclass
from typing import Optional


@dataclass
class Cell:
    """Клетка поля."""

    is_bomb: bool = False
    is_flagged: bool = False
    is_open: bool = False
    value: Optional[int] = None

    @property
    def is_empty(self) -> bool:
        """Является ли клетка пустой."""
        return not self.is_bomb and self.value is None

    @property
    def has_value(self) -> bool:
        """Есть ли в клетке число."""
        return self.value is not None

    def set_bomb(self):
        """Сделать клетку бомбой."""
        self.is_bomb = True

    def set_flagged(self):
        """Пометить клетку флагом."""
        self.is_flagged = True

    def remove_flag(self):
        """Убрать пометку флага с клетки."""
        self.is_flagged = False

    def set_open(self):
        """Пометить клетку как открытую."""
        self.is_open = True

    def increment_value(self):
        """Увеличить численное значение клетки."""
        if self.value is None:
            self.value = 0
        self.value += 1
