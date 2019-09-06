from dimension import Dimension

wall_characters = "─│└┌┐┘├┤┬┴┼"
exit_character = "#"
player_character = "§"


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
