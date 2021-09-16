import itertools as it
import random
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
            raise CellOutOfRange("Клетки с данной координатой не существует.")

    return new_func


class Field:
    """Поле."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._field = self._create_field()

    def __iter__(self) -> Iterator[List[Cell]]:
        return iter(self._field)

    def _create_field(self) -> List[List[Cell]]:
        """Создание пустого поля."""
        return [
            [Cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def set_bombs(self, bombs_count: int):
        """Расстановка бомб.

        Расстановка бомб и обновление значений у их соседних клеток.
        """
        cells_count = self.width * self.height
        if bombs_count > cells_count:
            raise ValueError("Слишком много бомб!")

        cells_positions = it.product(
            range(self.width),
            range(self.height),
            repeat=1,
        )
        bombs_positions = random.sample(tuple(cells_positions), k=bombs_count)

        for (bomb_x, bomb_y) in bombs_positions:
            cell = self._get_cell(bomb_x, bomb_y)
            cell.set_bomb()

            for neighbor_cell in self._get_all_neighbors(bomb_x, bomb_y):
                neighbor_cell.increment_value()

    def _get_cell(self, cell_x: int, cell_y: int) -> Cell:
        """Получение клетки по её координатам."""
        return self._field[cell_y][cell_x]

    def _get_all_neighbors_positions(
        self, cell_x: int, cell_y: int
    ) -> Iterator[Tuple[int, int]]:
        """Получение позиций всех соседей клетки.

        Получение позиций соседей по сторонам и диагоналям.
        """
        for (x_offset, y_offset) in it.product((-1, 0, 1), repeat=2):
            if x_offset == y_offset == 0:
                continue

            x = cell_x + x_offset
            y = cell_y + y_offset
            if x not in range(self.width) or y not in range(self.height):
                continue

            yield (x, y)

    def _get_all_neighbors(self, cell_x: int, cell_y: int) -> Iterator[Cell]:
        """Получение всех соседей клетки.

        Получение всех действительных соседей по сторонам и диагоналям.
        """
        neighbors_positions = self._get_all_neighbors_positions(cell_x, cell_y)
        for (neighbor_x, neighbor_y) in neighbors_positions:
            yield self._get_cell(neighbor_x, neighbor_y)

    @handle_out_of_range
    def open_cell(self, cell_x: int, cell_y: int):
        """Открыть клетку."""
        cell = self._get_cell(cell_x, cell_y)
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
        neighbors_positions = self._get_all_neighbors_positions(cell_x, cell_y)
        for (x, y) in neighbors_positions:
            cell = self._get_cell(x, y)
            if cell.is_open:
                continue

            cell.set_open()
            if cell.is_empty:
                self._open_empty_cell_neighbors(x, y)

    def _open_valued_cell_neighbors(self, cell_x: int, cell_y: int):
        """Открытие соседей численной клетки.

        Если рядом с численной клеткой поставлено достаточное
        количество флагов, то открываем все соседние, не помеченные флагом,
        клетки. Иначе бросаем исключение.
        """
        flags_count = 0
        for neighbor_cell in self._get_all_neighbors(cell_x, cell_y):
            if neighbor_cell.is_flagged:
                flags_count += 1

        cell = self._get_cell(cell_x, cell_y)
        if flags_count != cell.value:
            raise NotEnoughFlags("Недостаточно флагов для открытия соседей!")

        neighbors_positions = self._get_all_neighbors_positions(cell_x, cell_y)
        for (neighbor_x, neighbor_y) in neighbors_positions:
            neighbor_cell = self._get_cell(neighbor_x, neighbor_y)
            if not neighbor_cell.is_flagged and not neighbor_cell.is_open:
                self.open_cell(neighbor_x, neighbor_y)

    @handle_out_of_range
    def set_flag(self, cell_x: int, cell_y: int):
        """Пометить клетку флагом."""
        cell = self._get_cell(cell_x, cell_y)
        cell.set_flagged()

    @handle_out_of_range
    def remove_flag(self, cell_x: int, cell_y: int):
        """Убрать пометку флага с клетки."""
        cell = self._get_cell(cell_x, cell_y)
        cell.remove_flag()

    def is_win(self) -> bool:
        """Пройдена ли игра."""
        return all(
            cell.is_open or cell.is_flagged
            for row in self
            for cell in row
        )
