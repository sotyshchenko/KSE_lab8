import math


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalized(self):
        magnitude = self.magnitude()
        return Vector(self.x / magnitude, self.y / magnitude)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f'({self.x}, {self.y})'
