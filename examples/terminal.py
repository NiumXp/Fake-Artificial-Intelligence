from os import system
from time import sleep
from random import choice

from fakeAI import Grid, CellType

NULL, WALL = CellType.NULL, CellType.WALL
my_map = [
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
    [WALL, NULL, WALL, NULL, NULL, WALL, NULL, NULL, WALL],
    [WALL, NULL, WALL, WALL, NULL, WALL, NULL, WALL, WALL],
    [WALL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, WALL],
    [WALL, WALL, WALL, NULL, WALL, NULL, WALL, NULL, WALL],
    [WALL, NULL, NULL, NULL, WALL, NULL, WALL, WALL, WALL],
    [WALL, NULL, WALL, NULL, NULL, NULL, WALL, NULL, WALL],
    [WALL, NULL, NULL, NULL, WALL, NULL, NULL, NULL, WALL],
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
]

grid = Grid.from_list(my_map)
grid.characters = (' ', '#', 'O', '\033[1;31mX\033[0m')
monster = grid.spawn_monster(1, 1)

while True:
    system("cls")
    
    neighbors = monster.neighbors
    print(neighbors)
    move_functions = monster.move_functions

    print(grid)

    directions = []
    for i, v in enumerate(neighbors):
        if v == CellType.NULL:
            directions.append(move_functions[i])
    print(directions)
    direction = choice(directions)

    direction()

    sleep(1/4)
