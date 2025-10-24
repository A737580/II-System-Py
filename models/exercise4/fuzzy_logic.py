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
        """Фаззификация входных данных"""
        pass

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
        pass

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
        pass
