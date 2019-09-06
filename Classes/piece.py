from dimension import Dimension
from map import exit_character, player_character, wall_characters


class Piece:
    __slots__ = ("value", "position_value")

    def __init__(self, character: str, position_value: Dimension):
        if type(character) is not str:
            raise TypeError('expected str')
        elif type(position_value) is not Dimension:
            raise TypeError('expected Dimension object')
        else:
            self.value = character
            self.position_value = position_value

    def iswall(self):
        return self.value in wall_characters

    def isexit(self):
        return self.value == exit_character

    def isplayer(self):
        return self.value == player_character

    def __str__(self):
        return self.character
