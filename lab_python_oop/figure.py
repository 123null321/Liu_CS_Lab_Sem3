from abc import ABC, abstractmethod

class GeometricFigure(ABC):
    @abstractmethod
    def square(self):
        pass

    @classmethod
    def get_name(cls):
        return cls.__name__
