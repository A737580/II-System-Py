from __future__ import annotations
from typing import TYPE_CHECKING
import re

if TYPE_CHECKING:
    from models.exercise2.fuzzy_statement import FuzzyStatement

class FuzzyStatement:
    """Класс для хранения и управления высказываниями с нечеткой логикой.

    Высказывание хранит переменные: base_text, category_text, parameter, truth_degree.
    """

    def __init__(
        self, base_text: str, category_text: str, parameter: float, truth_degree: float
    ):
        self._base_text: str = base_text
        self._category_text: str = category_text
        self._parameter: float = parameter
        self._truth_degree: float = max(0.0, min(1.0, truth_degree))

    @property
    def base_text(self) -> str:
        return self._base_text

    @property
    def category_text(self) -> str:
        return self._category_text

    @property
    def parameter(self) -> float:
        return self._parameter

    @property
    def truth_degree(self) -> float:
        return self._truth_degree

    def ToString(self) -> str:
        return f"{self._base_text} {self._parameter} - {self._category_text} [{self._truth_degree}]"

    def Negative(self) -> FuzzyStatement:
        truth_degree: float = round(1.0 - self._truth_degree,2)
        new_category: str = re.sub(r"^не\s+", "", self._category_text)
        category_text=""
        if new_category == self._category_text:
            category_text = f"не {new_category}"
        else:
            category_text = new_category
        return FuzzyStatement(self._base_text, category_text, self._parameter, truth_degree)
    
    @staticmethod
    def Conjunction(
        firstStatement: FuzzyStatement, secondStatement: FuzzyStatement, type: str
    ) -> FuzzyStatement:
        new_truth_degree: float = 0.0
        match type:
            case "алгебраическая сумма":
                new_truth_degree = (
                    firstStatement.truth_degree * secondStatement.truth_degree
                )
            case "граничная сумма":
                new_truth_degree = max(
                    0, firstStatement.truth_degree + secondStatement.truth_degree - 1
                )
            case "драстическая сумма":
                if firstStatement.truth_degree == 1.0:
                    new_truth_degree = secondStatement.truth_degree
                elif secondStatement.truth_degree == 1.0:
                    new_truth_degree = firstStatement.truth_degree
                else:
                    new_truth_degree = 0
            case _:
                new_truth_degree = min(
                    firstStatement.truth_degree, secondStatement.truth_degree
                )
        new_base = f"{firstStatement.base_text} {firstStatement.category_text} И {secondStatement.base_text} {secondStatement.category_text}"
        return FuzzyStatement(new_base, "", 0.0, new_truth_degree)
    
    @staticmethod
    def Disjunction(
        firstStatement: FuzzyStatement, secondStatement: FuzzyStatement, type: str
    ) -> FuzzyStatement:
        new_truth_degree: float = 0.0
        match type:
            case "алгебраическая сумма":
                new_truth_degree = (
                    firstStatement.truth_degree
                    + secondStatement.truth_degree
                    - (firstStatement.truth_degree * secondStatement.truth_degree)
                )
            case "граничная сумма":
                new_truth_degree = min(
                    1, firstStatement.truth_degree + secondStatement.truth_degree
                )
            case "драстическая сумма":
                if firstStatement.truth_degree == 0.0:
                    new_truth_degree = secondStatement.truth_degree
                elif secondStatement.truth_degree == 0.0:
                    new_truth_degree = firstStatement.truth_degree
                else:
                    new_truth_degree = 1
            case _:
                new_truth_degree = max(
                    firstStatement.truth_degree, secondStatement.truth_degree
                )
        new_base = f"{firstStatement.base_text} {firstStatement.category_text} ИЛИ {secondStatement.base_text} {secondStatement.category_text}"
        return FuzzyStatement(new_base, "", 0.0, new_truth_degree)
