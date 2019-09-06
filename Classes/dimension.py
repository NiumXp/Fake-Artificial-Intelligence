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
