from .figure import GeometricFigure
from .color import FigureColor

class Rectangle(GeometricFigure):

    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = FigureColor(color)

    def square(self):
        return self.width * self.height

    def __repr__(self):
        return "{} {} цвета шириной {} и высотой {} площадью {}.".format(
            self.get_name(),
            self.color.color,
            self.width,
            self.height,
            self.square()
        )
