from models.exercise5.rule import SugenoRule1D


class SugenoModel1D:
    def __init__(self, rules: list[SugenoRule1D]):
        self.rules = rules

    def predict(self, x: float) -> float:
        numerator = 0.0
        denominator = 0.0

        for rule in self.rules:
            w = rule.firing_strength(x)
            y = rule.output(x)

            numerator += w * y
            denominator += w

        return numerator / denominator if denominator != 0 else 0.0
    

