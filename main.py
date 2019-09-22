#coding=utf-8
from time import sleep
from os import system, name
from random import choice

player_char = "§"
exit_char = "#"

def clear():
    system('cls' if name == 'nt' else 'clear')

def red(string: str):
    'Deixa a string vermelha'
    return "\033[1;31m" + string + "\033[0m"

def green(string: str):
    'Deixa a string verde'
    return "\033[1;32m" + string + "\033[0m"

def blue(string: str):
    'Deixa a string azul'
    return "\033[1;36m" + string + "\033[0m"

def yellow(string: str):
    'Deixa a string amarela'
    return "\033[1;33m" + string + '\033[0m'

def line_transform(string: str) -> str:
    if player_char not in string and exit_char not in string:
        return red(string)
    else:
        if player_char in string:
            player_index = string.find(player_char)
            string = red(string[:player_index]) + green(string[player_index]) + red(string[player_index + 1:])
        else:
            exit_index = string.find(exit_char)
            string = red(string[:exit_index]) + blue(string[exit_index]) + red(string[exit_index + 1:])
        return string


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

    @property
    def exit_pos(self):
        index = 0
        for line in self.__inner__:
            if exit_char in line:
                return (index, line.find(exit_char))
            index += 1

    def character(self, line: int, colum: int):
        'Pega o caractere que está na posição informada'
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
        'Move o player para a posição informada'
        _temp_var = list(self.__inner__[actual_player_pos[0]])
        _temp_var[actual_player_pos[1]] = " "
        self.__inner__[actual_player_pos[0]] = ''.join(_temp_var)

        _temp_var = list(self.__inner__[new_player_pos[0]])
        _temp_var[new_player_pos[1]] = player_char
        self.__inner__[new_player_pos[0]] = ''.join(_temp_var)

    def show(self):
        'Mostra a tabela na tela, toda colorida'
        for line in self.__inner__:
            print(line_transform(line))

def prepare():
    'Espera um tempo e apaga o terminal'
    sleep(1/8); clear()

def opposite(direction: str):
    'Retorna o oposto daquela direção. Se direita é passado, a saída será esquerda...'
    if direction == "right":
        return "left"
    elif direction == "left":
        return "right"
    elif direction == "up":
        return "down"
    else:
        return "up"

moves = 0
exit_pos = Table().exit_pos
screen = Table()
last_pos = "left"

while True:
    prepare()

    opposite_last_pos = opposite(last_pos)

    screen.show()
    player = screen.player()

    if player.actual.value() == exit_pos:
        break

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
    moves += 1

print(yellow(f"O 'monstrinho' encontrou a saída! Ele se moveu {moves} vezes!"))
