import math

class TriangularMF:
    """Треугольная функция принадлежности"""
    def __init__(self, a, b, c):
        assert a < b < c, "Параметры должны быть: a < b < c"
        self.a = a
        self.b = b
        self.c = c

    def degree(self, x: float) -> float:
        if x <= self.a or x >= self.c:
            return 0.0
        if x == self.b:
            return 1.0
        if self.a < x < self.b:
            return (x - self.a) / (self.b - self.a)
        if self.b < x < self.c:
            return (self.c - x) / (self.c - self.b)
        return 0.0


class GaussianMF:
    """Гауссова функция принадлежности"""
    def __init__(self, center, sigma):
        assert sigma > 0, "Сигма должна быть положительной"
        self.center = center
        self.sigma = sigma

    def degree(self, x: float) -> float:
        return math.exp(-((x - self.center) ** 2) / (2 * self.sigma ** 2))