from models.exercise5.membership import TriangularMF

class SugenoRule1D:
    def __init__(self, mf, a=0.0, b=0.0):
        self.mf = mf
        self.a = a
        self.b = b

    def firing_strength(self, x):
        return self.mf.degree(x)

    def output(self, x):
        return self.a * x + self.b

