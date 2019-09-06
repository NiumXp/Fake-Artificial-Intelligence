
wall_characters = "─│└┌┐┘├┤┬┴┼"
exit_character = "#"
player_character = "§"

class Dimension:
    __slots__ = "length", "height"

    def __init__(self, length: int, height: int):
        if type(length) is not int or  type(length) is not int:
            raise TypeError('expected int')
        else:
            self.length = length
            self.height = height

    def __call__(self):
        return (self.height, self.length)


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


class SnowBall:
    def __init__(self, **kwargs):
        self.__dict__ = **kwargs


class Map:
    __slots__ = ("__map__", "__dimension__")

    def __init__(self, map: str, dimension: Dimension):
        if type(map) is not str:
            raise TypeError('expected str')
        elif type(dimension) is not Dimension:
            raise TypeError('expected Dimension object')
        else:
            self.__dimension__ = dimension
            self.__map__ = self._transform_map(map, dimension.length)

    def __str__(self):
        return self.__map__

    @staticmethod
    def _transform_map(map: str, lenght: int) -> str:
        if type(map) is not str:
            raise TypeError('expected str')
        elif type(lenght) is not int:
            raise TypeError('expected int')
        else:
            map = list(map)
            counter = -1
            for index in range(0, len(map), lenght):
                if index != 0:
                    map.insert(index + counter, '\n')
                counter += 1
            return ''.join(map)

    @property
    def dimension(self):
        return self.__dimension__

    @dimension.setter
    def dimension(self, new_value):
        return self.__dimension__


mapa = Map("......   ..   ..   ......", Dimension(5, 5))
print(mapa)

