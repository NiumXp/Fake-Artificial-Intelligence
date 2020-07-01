import pyxel
from random import choice
from time import sleep
from threading import Thread
#from collections import namedtuple
from math import ceil


class Walls:
    __slots__ = ("color", "dimension", "positions")

    def __init__(self, *, color: int=8, dimension: int=5):
        self.color = color
        self.dimension = dimension

        self.positions = []

    def remove(self, y: int, x: int) -> None:
        self.positions.remove((y, x))

    def new(self, *, y: int, x: int) -> None:
        self.positions.append(Position(y=y, x=x))

    def horizontal_line(self, *, y: int, x: int, lenght: int):
        index = 1

        x -= 5

        for _ in range(lenght):
            self.positions.append(Position(y=y, x=x + 5 * index))
            index += 1

    def vertical_line(self, *, y: int, x: int, lenght: int):
        index = 1

        y -= self.dimension

        for _ in range(lenght):
            self.positions.append(Position(y=y + self.dimension * index, x=x))
            index += 1

    def rectangle(self, *, y: int, x: int, width: int, height: int):
        for wx in (x, x + ((width - 1) * self.dimension)):
            self.vertical_line(x=wx, y=y, lenght=height)
        
        for hy in (y, y + ((height - 1) * self.dimension)):
            self.horizontal_line(x=x + self.dimension, y=hy, lenght=width - 2)
        
    def draw(self) -> None:
        for position in self.positions:
            pyxel.rect(
                x=position.x, y=position.y,
                w=self.dimension, h=self.dimension,
                col=self.color
                )

    def __iter__(self):
        return (position for position in self.positions)

    def __getitem__(self, value):
        return self.positions[value]

def opposite(direction: str):
    directions = ["up", "left", "down", "right"]
    if direction == "up":
        return "down"
    elif direction == "left":
        return "right"
    elif direction == "down":
        return "up"
    elif direction == "right":
        return "left"
    else:
        return None


class Monster:
    __slots__ = (
        'y', 'x',
        "direction_choiced",
        "color",
        "velocity",
        "delay",
        "last_y", "last_x", "last_pos_name",
        "_directions")

    def __init__(self, *, y: int, x: int, color: int=11, velocity=5, delay: float=1):      
        self.y = y
        self.x = x

        self.last_y = self.last_x = self.last_pos_name = self.direction_choiced = "..."

        self.color = color

        self.velocity = velocity

        self.delay = delay

        self._directions = {
            "up": self._up,
            "left": self._left,
            "down": self._down,
            "right": self._right
            }

    def _up(self, velocity: int) -> None:
        self.last_y = self.y
        self.y -= velocity

    def _left(self, velocity: int) -> None:
        self.last_x = self.x
        self.x -= velocity

    def _down(self, velocity: int) -> None:
        self.last_y = self.y
        self.y += velocity

    def _right(self, velocity: int)  -> None:
        self.last_x = self.x
        self.x += velocity

    def random_direction(self, walls: Walls) -> str:
        name_positions = [item for item in self._directions.keys()]
        
        free_positions = []
        for position in name_positions:
            if position == "up":
                if (self.y - self.velocity, self.x) not in walls:
                    free_positions.append(position)
            elif position == "left":
                if (self.y, self.x - self.velocity) not in walls:
                    free_positions.append(position)
            elif position == "down":
                if (self.y + self.velocity, self.x) not in walls:
                    free_positions.append(position)
            elif position == "right":
                if (self.y, self.x + self.velocity) not in walls:
                    free_positions.append(position)

        value = opposite(self.last_pos_name)
        if len(free_positions) > 1 and value in free_positions:
            free_positions.remove(value)

        if len(free_positions) != 0:
            self.direction_choiced = choice(free_positions)
        
            return self.direction_choiced

    def start_brain(self, walls: Walls) -> None:
        def timeout():
            while True:
                direction = self.random_direction(walls)
                if direction != None:
                    self.move_to(direction)
                sleep(self.delay)

        thread = Thread(target=timeout, name='MonsterBrain')
        thread.start()

    def place_at(self, *, y: int, x: int):
        self.y = y; self.x = x

    def move_to(self, direction: str) -> None:
        if direction in self._directions.keys():
            function = self._directions[direction]
            
            self.last_pos_name = direction

            function(self.velocity)
        else:
            raise NameError(f"'{direction}' direction not exists")

    def draw(self, dimension: int=5) -> None:
        pyxel.rect(x=self.x, y=self.y, w=dimension, h=dimension, col=self.color)


class Position:
    __slots__ = ('x', 'y')

    def __init__(self, *, y: int, x: int):
        self.y = y
        self.x = x

    def __iter__(self):
        return (item for item in (self.y, self.x))

    def __eq__(self, obj):
        try:
            return tuple(obj) == tuple(self)
        except ValueError:
            return False

    def __str__(self):
        return f"<Position (y={self.y}, x={self.x})>"

monster = Monster(velocity=5, y=60, x=80, color=8, delay=1/4)
                                    #Um quarto de segundo ^
walls = Walls(color=5)

directions = ("up", "left", "down", "right")

pyxel.init(160, 120, fps=120, caption="Fake Artificial Inteligence")

pyxel.mouse(True)

monster.start_brain(walls)

#Mapa
walls.rectangle(y=35, x=10, width=27, height=12)
walls.vertical_line(y=40, x=20, lenght=2)
walls.horizontal_line(y=55, x=15, lenght=2)
walls.vertical_line(y=45, x=30, lenght=3)
walls.horizontal_line(y=50, x=35, lenght=2)
walls.vertical_line(y=40, x=40, lenght=2)
walls.horizontal_line(y=65, x=20, lenght=3)
walls.horizontal_line(y=70, x=15, lenght=2)
walls.vertical_line(y=60, x=40, lenght=2)
walls.vertical_line(y=70, x=30, lenght=2)
walls.new(y=85, x=30)
walls.vertical_line(y=80, x=20, lenght=2)
walls.vertical_line(y=75, x=40, lenght=2)
walls.horizontal_line(y=75, x=45, lenght=2)
walls.new(y=80, x=50)
walls.vertical_line(y=80, x=60, lenght=2)
walls.vertical_line(y=65, x=60, lenght=2)
walls.horizontal_line(y=70, x=65, lenght=3)
walls.vertical_line(y=75, x=70, lenght=2)
walls.new(y=80, x=80)
walls.vertical_line(y=70, x=85, lenght=4)
walls.vertical_line(y=55, x=50, lenght=3)
walls.new(y=55, x=55)
walls.horizontal_line(y=45, x=50, lenght=2)
walls.new(y=40, x=55)
walls.new(y=40, x=65)
walls.horizontal_line(y=50, x=65, lenght=3)
walls.new(y=55, x=65)
walls.new(y=55, x=75)
walls.new(y=65, x=70)
walls.new(y=45, x=75)
walls.vertical_line(y=40, x=95, lenght=4)
walls.new(y=40, x=110)
walls.horizontal_line(y=55, x=105, lenght=4)
walls.new(y=50, x=110)
walls.vertical_line(y=40, x=120, lenght=2)
walls.horizontal_line(y=45, x=130, lenght=2)
walls.horizontal_line(y=55, x=130, lenght=2)
walls.new(y=45, x=100)
walls.vertical_line(y=45, x=85, lenght=3)
walls.new(y=50, x=90)
walls.vertical_line(y=65, x=90, lenght=2)
walls.new(y=80, x=95)
walls.horizontal_line(y=70, x=100, lenght=2)
walls.vertical_line(y=80, x=105, lenght=2)
walls.horizontal_line(y=70, x=115, lenght=5)
walls.new(y=65, x=125)
walls.new(y=65, x=135)
walls.vertical_line(y=60, x=115, lenght=2)
walls.new(y=60, x=105)
walls.horizontal_line(y=80, x=115, lenght=2)
walls.new(y=85, x=120)
walls.horizontal_line(y=80, x=130, lenght=2)

place_wall = remove_wall = shift_pressed = False

def straighten(num: int):
    return ceil(num / 5) * 5 - 5

while True:
    pyxel.cls(0)

    pyxel.text(5, 5, "Last", 7)
    pyxel.text(5, 15, f'Y: {monster.last_y} X: {monster.last_x}', 12)

    pyxel.text(85, 5, "Current", 7)
    pyxel.text(85, 15, f'Y: {monster.y} X: {monster.x}', 12)

    pyxel.text(5, 110, f'Direction', 7)
    pyxel.text(43, 110, monster.last_pos_name, 12)

    pyxel.text(120, 110,  f"({pyxel.mouse_y}, {pyxel.mouse_x})", 14)

    if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
        place_wall = True
    
    if pyxel.btnr(pyxel.MOUSE_LEFT_BUTTON):
        place_wall = False

    if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON):
        remove_wall = True

    if pyxel.btnr(pyxel.MOUSE_RIGHT_BUTTON):
        remove_wall = False

    if place_wall or remove_wall:
        pyxel.text(75, 110, "*Editor*", 9)

        mouse_pos = Position(
            x=straighten(pyxel.mouse_x),
            y=straighten(pyxel.mouse_y)
            )
        
        pyxel.text(120, 100, f"{[item for item in mouse_pos]}", 14)

        if place_wall:
            if mouse_pos not in walls:
                walls.new(x=mouse_pos.x, y=mouse_pos.y)
        else:
            if mouse_pos in walls:
                walls.remove(x=mouse_pos.x, y=mouse_pos.y)

    if pyxel.btnp(pyxel.KEY_SHIFT):
        monster.place_at(y=straighten(pyxel.mouse_y), x=straighten(pyxel.mouse_x))
        shift_pressed = True

    if pyxel.btnr(pyxel.KEY_SHIFT):
        shift_pressed = False

    if shift_pressed:
        mouse_pos = Position(
            x=straighten(pyxel.mouse_x),
            y=straighten(pyxel.mouse_y)
            )
        
        pyxel.text(120, 100, f"{[item for item in mouse_pos]}", 14)

        pyxel.text(75, 100, "*Shift*", 9)

    if pyxel.btnp(pyxel.KEY_DELETE):
        walls.positions.clear()

    monster.draw(5)
    walls.draw()

    pyxel.flip()
