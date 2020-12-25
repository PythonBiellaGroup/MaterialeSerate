class IShape:
    def draw(self):
        raise NotImplementedError


class Circle(IShape):
    def draw(self):
        pass


class Square(IShape):
    def draw(self):
        pass


class Rectangle(IShape):
    def draw(self):
        pass


"""
Con questo design saremo in grado di usare la stessa interfaccia per
disegnare anche forme particolari come semicerchi, triangoli equiliateri,
etc.
"""
