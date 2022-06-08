from collections import defaultdict
import itertools as it
import random
import string
from typing import Iterator, List, Tuple

from cell import Cell
from exceptions import BombDetonation, CellOutOfRange, NotEnoughFlags


def handle_out_of_range(func):
    """Обработка позиции клетки вне поля.

    Обработка ситуации, когда клетки с введёнными игроком координатами
    не существует. Перехватываем IndexError, и выбрасываем CellOutOfRange.
    """

    def new_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            raise CellOutOfRange("Неверные координаты клетки!")

    return new_func


class Field:
    """Поле."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def __iter__(self) -> Iterator[List[Cell]]:
        return iter(self._field)

    def set_bombs(self, bombs_count: int):
        """Расстановка бомб.

        Расстановка бомб и обновление значений у их соседних клеток.
        """
        cells_count = self.width * self.height
        if bombs_count > cells_count:
            raise ValueError("Слишком много бомб!")

        self._field = RandomField(self.width, self.height, bombs_count)

    def _cell(self, cell_x: int, cell_y: int) -> Cell:
        """Клетка с данными координатами."""
        return self._field[cell_y][cell_x]

    def _neighbors_positions(
        self, cell_x: int, cell_y: int
    ) -> Iterator[Tuple[int, int]]:
        """Позиции всех соседей клетки."""
        for (x_offset, y_offset) in it.product((-1, 0, 1), repeat=2):
            if x_offset == y_offset == 0:
                continue

            x = cell_x + x_offset
            y = cell_y + y_offset
            if x not in range(self.width) or y not in range(self.height):
                continue

            yield (x, y)

    def _neighbors(self, cell_x: int, cell_y: int) -> Iterator[Cell]:
        """Все соседи клетки."""
        positions = self._neighbors_positions(cell_x, cell_y)
        for (x, y) in positions:
            yield self._cell(x, y)

    @handle_out_of_range
    def open_cell(self, cell_x: int, cell_y: int):
        """Открыть клетку."""
        cell = self._cell(cell_x, cell_y)
        if cell.is_bomb:
            raise BombDetonation("Взрыв!")
        elif cell.is_empty:
            cell.set_open()
            self._open_empty_cell_neighbors(cell_x, cell_y)
        elif cell.is_flagged:
            pass
        elif cell.has_value and cell.is_open:
            cell.set_open()
            self._open_valued_cell_neighbors(cell_x, cell_y)
        else:
            cell.set_open()

        cell.remove_flag()

    def _open_empty_cell_neighbors(self, cell_x: int, cell_y: int):
        """Открытие всех соседей пустой клетки.

        Открытиие всех соседних пустых клеток, и их первых не пустых соседей.
        """
        positions = self._neighbors_positions(cell_x, cell_y)
        for (x, y) in positions:
            neighbor = self._cell(x, y)
            if neighbor.is_open:
                continue

            neighbor.set_open()
            if neighbor.is_empty:
                self._open_empty_cell_neighbors(x, y)

    def _open_valued_cell_neighbors(self, cell_x: int, cell_y: int):
        """Открытие соседей численной клетки.

        Если рядом с численной клеткой поставлено достаточное
        количество флагов, то открываем все соседние, не помеченные флагом,
        клетки. Иначе бросаем исключение.
        """
        flags_count = 0
        for neighbor in self._neighbors(cell_x, cell_y):
            if neighbor.is_flagged:
                flags_count += 1

        cell = self._cell(cell_x, cell_y)
        if flags_count != cell.value:
            raise NotEnoughFlags("Недостаточно флагов для открытия соседей!")

        neighbors_positions = self._neighbors_positions(cell_x, cell_y)
        for (neighbor_x, neighbor_y) in neighbors_positions:
            neighbor = self._cell(neighbor_x, neighbor_y)
            if not neighbor.is_flagged and not neighbor.is_open:
                self.open_cell(neighbor_x, neighbor_y)

    @handle_out_of_range
    def set_flag(self, cell_x: int, cell_y: int):
        """Пометить клетку флагом."""
        cell = self._cell(cell_x, cell_y)
        cell.set_flagged()

    @handle_out_of_range
    def remove_flag(self, cell_x: int, cell_y: int):
        """Убрать пометку флага с клетки."""
        cell = self._cell(cell_x, cell_y)
        cell.remove_flag()

    def is_win(self) -> bool:
        """Пройдена ли игра."""
        return all(
            cell.is_open or cell.is_flagged
            for row in self
            for cell in row
        )

    def print(self):
        """Вывод поля в консоль"""
        letters = string.digits[1:] + string.ascii_lowercase
        print(" " * 4 + " ".join(f"{letters[i]:<3}" for i in range(self.width)))
        for i, row in enumerate(self):
            letter = f"{letters[i]:<2}"
            print(letter, " ".join(str(cell) for cell in row))


class RandomField(List[List[Cell]]):
    """Поле с бомбами в случайных местах."""

    def __init__(self, width: int, height: int, bombs_count: int):
        cells_positions = it.product(range(width), range(height), repeat=1)
        bombs_positions = random.sample(tuple(cells_positions), k=bombs_count)

        cells = defaultdict(Cell)
        for (bomb_x, bomb_y) in bombs_positions:
            for (x_offset, y_offset) in it.product((-1, 0, 1), repeat=2):
                x = bomb_x + x_offset
                y = bomb_y + y_offset
                cells[x, y].increment_value()

        for (bomb_x, bomb_y) in bombs_positions:
            cells[bomb_x, bomb_y].set_bomb()

        field = [[cells[x, y] for x in range(width)] for y in range(height)]
        super().__init__(field)
