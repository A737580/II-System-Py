class CalcService:
    def __init__(self, model):
        self.model = model

    def calc_sum(self, numbers: list[float]) -> float:
        return self.model.calculate(numbers)
