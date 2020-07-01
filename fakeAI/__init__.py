from enum import IntEnum
from typing import Tuple
from collections.abc import Sequence

numbers = (0, 1, 2, 3)

DEFAULT_CHARS = numbers


class CellType(IntEnum):
    NULL, WALL, MONSTER, EXIT = numbers


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
        h, w = self._map.height - 1, self._map.width - 1

        left  = self._map.cell(y, (x - 1) if x > 0 else x if x > w else w)
        top   = self._map.cell((y - 1) if y > 0 else y if y > h else h, x)
        right = self._map.cell(y, (x + 1) if x < w else 0 if x > 0 else w)
        down  = self._map.cell((y + 1) if y < h else 0 if y > 0 else y, x)

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
    __slots__ = ("_inner", "_chars", "_w", "_h", "_function")

    def __init__(self, ls: list=None, *, characters: tuple=DEFAULT_CHARS):
        self._chars = characters

        if ls:
            w = len(ls[0])
            h = len(ls)

            for line in ls:
                if len(line) == w:
                    for item in line:
                        if type(item) is not CellType:
                            raise TypeError("items of lines need to be CellType")
                else:
                    raise IndexError("lines need to has some width")
        else:
            w = h = 10
            ls = self.null_list(w, h)

        self._w, self._h = (w, h)
        self._inner = ls

        self._function = lambda x, y, type: None

    @property
    def width(self) -> int:
        return self._w

    @property
    def height(self) -> int:
        return self._h

    @property
    def characters(self) -> tuple:
        return self._chars

    @characters.setter
    def characters(self, new_value):
        if isinstance(new_value, Sequence):
            if len(new_value) == 4:
                self._chars = new_value
            else:
                raise IndexError("sequence need has exactly 4 items")
        else:
            raise TypeError("tuple expected")

    @staticmethod
    def null_list(self, width: int, height: int) -> list:
        return [
            [CellType.NULL for _ in range(width)]
            for _ in range(height)
        ]

    def to_list(self, raw: bool=True) -> list:
        if raw:
            return self._inner
        else:
            return [map(lambda cell: self._chars[cell], line) for line in self._inner]

    @classmethod
    def from_list(cls, list_):
        obj = cls(list_)
        return obj

    def __str__(self):
        grid = self.to_list(raw=False)
        lines = [' '.join(map(str, line)) for line in grid]
        return '\n'.join(lines)

    def spawn_monster(self, x: int, y: int) -> Monster:
        self.change_cell(x, y, CellType.MONSTER)
        return Monster((x, y), self)

    def change_cell(self, column, line, celltype: CellType):
        if celltype in CellType:
            self._inner[column][line] = celltype
        else:
            raise TypeError("'CellType' expected")

    def cell(self, row, column):
        return self._inner[row][column]
