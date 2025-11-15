import math
from .figure import GeometricFigure
from .color import FigureColor

class Circle(GeometricFigure):

    def __init__(self, radius, color):
        self.radius = radius
        self.color = FigureColor(color)

    def square(self):
        return math.pi * self.radius ** 2

    def __repr__(self):
        return "{} {} цвета радиусом {} площадью {:.2f}.".format(
            self.get_name(),
            self.color.color,
            self.radius,
            self.square()
        )
