from enum import IntEnum
from typing import Tuple
from collections.abc import Sequence

numbers = (0, 1, 2)

DEFAULT_CHARS = numbers


class CellType(IntEnum):
    NULL, WALL, MONSTER = numbers


class Monster:
    def __init__(self, position: tuple, grid):
        self._x, self._y = position
        self._map = grid

        self.caller = lambda f: None

    @property
    def position(self) -> tuple:
        "Returns the monster position."
        return (self._x, self._y)

    @property
    def neighbors(self) -> Tuple[CellType]:
        x, y = self._x, self._y
        h, w = self._map.width - 1, self._map.height - 1

        left  = self._map.cell((x - 1) if x > 0 else w, y)
        top   = self._map.cell(x, y - (1 if y > 0 else h))
        right = self._map.cell((x + 1) if x < w else w, y)
        down  = self._map.cell(x, (y + 1) if y < 0 else h)

        return [left, top, right, down]

    @property
    def move_functions(self) -> tuple:
        return [self.to_left, self.to_up, self.to_right, self.to_down]

    def move_to(self, x: int, y: int):
        h = self._map.height - 1
        w = self._map.width - 1

        if y < 0:
            y = h

        if x < 0:
            x = w

        if y > h:
            y = 0

        if x > w:
            x = 0

        old_x, old_y = self._x, self._y
        new_x, new_y = self._x, self._y = x, y

        self._map.change_cell(old_y, old_x, CellType.NULL)
        self._map.change_cell(new_y, new_x, CellType.MONSTER)

    def to_left(self):
        self.move_to(self._x - 1, self._y)

    def to_up(self):
        self.move_to(self._x, self._y - 1)

    def to_right(self):
        self.move_to(self._x + 1, self._y)

    def to_down(self):
        self.move_to(self._x, self._y + 1)


class Grid:
    __slots__ = ("_inner", "_chars", "width", "height", "_function")

    def __init__(self, width: int, height: int, *, characters: tuple=DEFAULT_CHARS):
        self.width = width
        self.height = height

        self._chars = characters

        self._inner = [
            [CellType.NULL for _ in range(width)]
            for _ in range(height)
        ]

        self._function = lambda x, y, type: None

    @property
    def characters(self) -> tuple:
        return self._chars

    @characters.setter
    def characters(self, new_value):
        if isinstance(new_value, Sequence):
            if len(new_value) == 3:
                self._chars = new_value
            else:
                raise IndexError("sequence need has exactly 3 items")
        else:
            raise TypeError("tuple expected")

    def to_list(self):
        return self._inner

    def __str__(self):
        return '\n'.join(' '.join(map(str, line)) for line in self.to_list())

    def spawn_monster(self):
        self.change_cell(0, 0, CellType.MONSTER)
        return Monster((0, 0), self)

    def change_cell(self, column, line, celltype: CellType):
        if celltype in CellType:
            self._inner[column][line] = celltype
        else:
            raise TypeError("'CellType' expected")

    def cell(self, column, line):
        return self._inner[column][line]
