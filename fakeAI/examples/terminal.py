from os import system
from time import sleep
from random import choice

from fakeAI import Grid, CellType

NULL, WALL, EXIT = CellType.NULL, CellType.WALL, CellType.EXIT
my_map = [
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
    [WALL, NULL, WALL, NULL, NULL, WALL, NULL, NULL, WALL],
    [WALL, NULL, WALL, WALL, NULL, WALL, NULL, WALL, WALL],
    [WALL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, WALL],
    [WALL, WALL, WALL, NULL, WALL, NULL, WALL, NULL, WALL],
    [WALL, NULL, NULL, NULL, WALL, NULL, WALL, WALL, WALL],
    [WALL, NULL, WALL, NULL, NULL, NULL, WALL, NULL, WALL],
    [WALL, NULL, NULL, NULL, WALL, NULL, NULL, NULL, WALL],
    [WALL, EXIT, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
]


class MyGrid(Grid):
    def render(self, line: list):
        transformed_line = [self.char(cell) for cell in line]

        wall_color, end = "\033[1;31m", "\033[0m"

        if CellType.EXIT not in line and CellType.MONSTER not in line:
            line = [wall_color + ' '.join(transformed_line) + end]
        else:
            if CellType.MONSTER in line:
                monster_pos = line.index(CellType.MONSTER)

                leftf = "{}{}{}".format(wall_color, ' '.join(transformed_line[:monster_pos]), end)
                rightf = "{}{}".format(wall_color, ' '.join(transformed_line[monster_pos + 1:]))

                line = [leftf, "\033[1;32m" + self.char(CellType.MONSTER) + end, rightf + end]

            if CellType.EXIT in line:
                exit_pos = line.index(CellType.EXIT)

                leftf = "{}{}{}".format(wall_color, ' '.join(transformed_line[:exit_pos]), end)
                rightf = "{}{}{}".format(wall_color, ' '.join(transformed_line[exit_pos + 1:]), end)

                line = [leftf, "\033[1;33m" + self.char(CellType.EXIT) + end, rightf]

        return ' '.join(line)


grid = MyGrid.from_list(my_map)
grid.characters = (' ', '#', 'O', 'X')

monster = grid.spawn_monster(1, 1)

move_functions = monster.move_functions

monster_in_maze = True
while monster_in_maze:
    system("cls")
    print(grid)

    neighbors = monster.neighbors

    try:
        pos = neighbors.index(CellType.EXIT)
    except ValueError:
        directions = [move_functions[i]
                    for i, v in enumerate(neighbors)
                    if v == CellType.NULL]

        direction = choice(directions)
    else:
        direction = move_functions[pos]
        monster_in_maze = False

    direction()

    sleep(1/6)

print("O monstrinho encontrou a saída!")
