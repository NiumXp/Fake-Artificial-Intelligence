#coding=utf-8
from time import sleep
from os import system, name
from random import choice

player_char = "§"

def clear():
    system('cls' if name == 'nt' else 'clear')

def red(string: str):
    'Deixa a string vermelinha'
    return "\033[1;31m" + string + "\033[0m"

def green(string: str):
    'Deixa a string verdinha'
    return "\033[1;32m" + string + "\033[0m"

def line_transform(string: str) -> str:
    if player_char not in string:
        return red(string)
    else:
        index = string.find(player_char)
        return red(string[:index]) + green(string[index]) + red(string[index + 1:])


class SnowBall:
    def __init__(self, **kwargs):
        self.__dict__ = dict(**kwargs)


class Position:
    __slots__ = "__inner__"

    def __init__(self, character: str, pos: tuple, name: str):
        self.__inner__ = (character, pos, name)

    def name(self):
        return self.__inner__[2]

    def iswall(self):
        return self.__inner__[0] in "─│└┌┐┘├┤┬┴┼"

    def value(self):
        '''
        :return: (line, col))'''
        return self.__inner__[1]

    def __str__(self):
        return self.__inner__[0]


class Table:
    __slots__ = "__inner__"

    def __init__(self):
        with open("table.txt", "r", encoding="UTF-8") as file:
            self.__inner__ = file.read().split("\n")[:-1]

    def character(self, line: int, colum: int):
        return self.__inner__[line][colum]

    def player(self) -> tuple:
        index = 0
        for line in self.__inner__:
            if player_char in line:
                player_pos = (index, line.find(player_char))
            index += 1

        _down = self.character(player_pos[0] + 1, player_pos[1])
        _up = self.character(player_pos[0] - 1, player_pos[1])
        _left = self.character(player_pos[0], player_pos[1] - 1)
        _right = self.character(player_pos[0], player_pos[1] + 1)

        return SnowBall(
            down=Position(_down, (player_pos[0] + 1, player_pos[1]), "down"),
            up=Position(_up, (player_pos[0] - 1, player_pos[1]), "up"),
            left=Position(_left, (player_pos[0], player_pos[1] - 1), "left"),
            right=Position(_right, (player_pos[0], player_pos[1] + 1), "right"),
            actual=Position(player_char, player_pos, "actual")
            )

    def move_player_to(self, new_player_pos, actual_player_pos):
        _temp_var = list(self.__inner__[actual_player_pos[0]])
        _temp_var[actual_player_pos[1]] = " "
        self.__inner__[actual_player_pos[0]] = ''.join(_temp_var)

        _temp_var = list(self.__inner__[new_player_pos[0]])
        _temp_var[new_player_pos[1]] = player_char
        self.__inner__[new_player_pos[0]] = ''.join(_temp_var)

    def show(self):
        for line in self.__inner__:
            print(line_transform(line))

def prepare():
    sleep(1/8); clear()

def opposite(direction: str):
    if direction == "right":
        return "left"
    elif direction == "left":
        return "right"
    elif direction == "up":
        return "down"
    else:
        return "up"

screen = Table()
last_pos = "left"
while True:
    prepare()

    opposite_last_pos = opposite(last_pos)

    screen.show()
    player = screen.player()

    positions = [player.down, player.left, player.up, player.right]
    free_positions = list(filter(lambda item: not item.iswall(), positions))
    for pos in free_positions:
        print(pos.value(), pos.name())

    if opposite_last_pos in map(lambda item: item.name(), free_positions):
        pos = list(filter(lambda item: item.name() == opposite_last_pos, free_positions))
        screen.move_player_to(pos[0].value(), player.actual.value())
        last_pos = opposite(pos[0].name())
    else:
        pos_2 = choice(free_positions)
        screen.move_player_to(pos_2.value(), player.actual.value())
        last_pos = opposite(pos_2.name())
