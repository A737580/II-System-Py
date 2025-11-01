from models.exercise4.data import Data, OptTriFunc, Rule
from models.exercise4.inputs import Inputs
from dataclasses import dataclass
from typing import List


@dataclass
class ClassMembership:
    name: str
    membership_degree: float


@dataclass
class TruthDegreeByClass:
    name: str
    truth_degree: float


@dataclass
class FuzzyEstimates:
    name: str
    truth_degree: float


@dataclass
class FuzzifyInput:
    name: str
    fuzzy_estimates: List[FuzzyEstimates]


class FuzzyLogic:
    def __init__(self):
        pass

    def determine_membership_class(self, data: Data, inputs: Inputs, norm: str) -> ClassMembership:
        fuzzify_inputs = self._fuzzify(inputs, data.opt_tri_func)
        truth_degrees_by_cls = self._calculating_truth_degree_by_class(fuzzify_inputs, data.rules, norm)
        class_membership = self._de_fuzzify(truth_degrees_by_cls, data.rules)
        return class_membership
    
    def _fuzzify(self, inputs: Inputs, opts: List[OptTriFunc]) -> List[FuzzifyInput]:
        fuzzified = []
        input_dict = inputs.__dict__
        for opt in opts:
            name = opt.name[0].lower() + opt.name[1:]
            x_val = input_dict.get(name)
            fuzzy_vals = []
            for tri in opt.variant:
                degree = self._triangle(x_val, tri.left_point, tri.center_point, tri.right_point)
                fuzzy_vals.append(FuzzyEstimates(tri.name, degree))
            fuzzified.append(FuzzifyInput(name, fuzzy_vals))
        return fuzzified

    def _triangle(self, x, a, b, c) -> float:
        """
        Треугольная функция с параметрами:
        a - левая граница (y=0)
        b - вершина (y=1)
        c - правая граница (y=0)
        """
        if a == b == c:
            return 1.0 if x == a else 0.0
        elif a == b:  # Случай, когда вершина совпадает с началом
            if x <= a:
                return 1.0
            elif x <= c:
                return max(0, (c - x) / (c - a))
            else:
                return 0.0
        elif b == c:  # Случай, когда вершина совпадает с концом
            if x >= c:
                return 1.0
            elif x >= a:
                return max(0, (x - a) / (c - a))
            else:
                return 0.0
        else:  # Классический треугольник
            if x <= a or x >= c:
                return 0.0
            elif a <= x <= b:
                return (x - a) / (b - a)
            elif b <= x <= c:
                return (c - x) / (c - b)

    def _calculating_truth_degree_by_class(self, f_inputs: List[FuzzifyInput], rules: List[Rule], norm:str) -> List[TruthDegreeByClass]:
        result = []
        for rule in rules:
            class_name = rule.name
            rule_truth_values = []
            for variant in rule.variant:  # Каждое правило — это комбинация условий
                vals = []
                for f_input in f_inputs:
                    feature_name = f_input.name
                    fuzzy_est_name = variant.get(feature_name)
                    if fuzzy_est_name is None:
                        continue
                    val = next((fe.truth_degree for fe in f_input.fuzzy_estimates if fe.name == fuzzy_est_name), 0.0)
                    vals.append(val)
                # объединяем по норме
                while len(vals) < 4:  # защита от ошибок (если меньше 4)
                    vals.append(1.0)
                truth_degree = self._conjunction(*vals[:4], type=norm)
                rule_truth_values.append(truth_degree)
            # объединяем по максимуму
            final_truth = max(rule_truth_values) if rule_truth_values else 0.0
            result.append(TruthDegreeByClass(class_name, final_truth))
        return result


    def _conjunction(self,a: float, b: float, c: float, d: float, type: str) -> float:
        match type.lower():
            case "алгебраическое произведение":
                return a * b * c * d
            case "граничное произведение":
                return max(0, a + b + c + d - 3)
            case "драстическое произведение":
                if a == 1.0 and b == 1.0 and c == 1.0 and d == 1.0:
                    return 1.0
                elif any(x == 0.0 for x in [a, b, c, d]):
                    return 0.0
                else:
                    return min(a, b, c, d)
            case _:  # "Минимум" по умолчанию
                return min(a, b, c, d)

    def _de_fuzzify(self, truth_degrees_by_cls:List[TruthDegreeByClass], rules: List[Rule]) -> ClassMembership:
        numerator = 0.0
        denominator = 0.0
        for td in truth_degrees_by_cls:
            rule = next((r for r in rules if r.name == td.name), None)
            if rule is None:
                continue
            μ = td.truth_degree
            center = rule.opt_rule.center_point
            numerator += μ * center
            denominator += μ
        if denominator == 0:
            return ClassMembership("Undefined", 0.0)
        center_value = numerator / denominator
        # выбираем ближайший по центру класс
        best_rule = min(
            rules, key=lambda r: abs(center_value - r.opt_rule.center_point)
        )
        best_truth = next(td.truth_degree for td in truth_degrees_by_cls if td.name == best_rule.name)
        return ClassMembership(best_rule.name, best_truth)
