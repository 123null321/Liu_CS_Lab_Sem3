from .rectangle import Rectangle

class Square(Rectangle):

    def __init__(self, side, color):
        super().__init__(side, side, color)

    def __repr__(self):
        return "{} {} цвета со стороной {} площадью {}.".format(
            self.get_name(),
            self.color.color,
            self.width,
            self.square()
        )
