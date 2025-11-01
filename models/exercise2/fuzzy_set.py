from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Dict, List
from models.exercise2.fuzzy_statement import FuzzyStatement
import re

if TYPE_CHECKING:
    from models.exercise2.fuzzy_set import FuzzySet

class FuzzySet:
    def __init__(self, name: str):
        self._name = name
        self._fuzzy_set: List[FuzzyStatement] = list()

    # === Методы доступа ===

    def get_name(self) -> str:
        return self._name

    def get_all(self) -> List[str]:
        return [stmt.to_string_fuzzy_set() for stmt in self._fuzzy_set]

    def add(self, parameter: float, truth_degree: float) -> bool:
        param_list = [stmt.parameter for stmt in self._fuzzy_set]
        epsilon = 1e-9

        for i in range(0, len(param_list)):
            if abs(param_list[i] - parameter) < epsilon:
                return False  

        self._fuzzy_set.append(FuzzyStatement(None, None, parameter, truth_degree))
        return True
        
    def remove(self, parameter: float) -> bool:
        param_list = [stmt.parameter for stmt in self._fuzzy_set]
        epsilon = 1e-9
        index = None
        for i in range(0, len(param_list)):
            if abs(param_list[i] - parameter) < epsilon:
                index = i
                break
        if index is not None:
            self._fuzzy_set.pop(index)
            return True
        return False

    def clear(self):
        self._name = None
        self._fuzzy_set = list()

    # === Вспомогательные методы для операций ===

    def _find_statement_by_parameter(self, parameter: float) -> FuzzyStatement:
        """Находит statement по параметру с учетом погрешности"""
        epsilon = 1e-9
        for stmt in self._fuzzy_set:
            if abs(stmt.parameter - parameter) < epsilon:
                return stmt
        return None

    def _t_norm(self, a: float, b: float, type: str) -> float:
        """T-норма (конъюнкция)"""
        match type:
            case "алгебраическая сумма":
                return a * b
            case "граничная сумма":
                return max(0, a + b - 1)
            case "драстическая сумма":
                if a == 1.0:
                    return b
                elif b == 1.0:
                    return a
                else:
                    return 0.0
            case _:  # "Минмакс" по умолчанию
                return min(a, b)

    def _s_norm(self, a: float, b: float, type: str) -> float:
        """S-норма (дизъюнкция)"""
        match type:
            case "алгебраическая сумма":
                return a + b - a * b
            case "граничная сумма":
                return min(a + b, 1)
            case "драстическая сумма":
                if a == 0.0:
                    return b
                elif b == 0.0:
                    return a
                else:
                    return 1.0
            case _:  # "Минмакс" по умолчанию
                return max(a, b)

    # === Основные операции ===

    def conjunction(self, secondSet: FuzzySet, type: str) -> FuzzySet:
        """Конъюнкция (пересечение) с различными нормами"""
        result = FuzzySet(f"{self._name}_AND_{secondSet._name}")
        
        # Получаем все уникальные параметры из обоих множеств
        all_params = set()
        for stmt in self._fuzzy_set:
            all_params.add(stmt.parameter)
        for stmt in secondSet._fuzzy_set:
            all_params.add(stmt.parameter)
        
        # Для каждого параметра вычисляем степень принадлежности
        for param in all_params:
            stmt1 = self._find_statement_by_parameter(param)
            stmt2 = secondSet._find_statement_by_parameter(param)
            
            truth1 = stmt1.truth_degree if stmt1 else 0.0
            truth2 = stmt2.truth_degree if stmt2 else 0.0
            
            # Применяем T-норму (конъюнкцию)
            new_truth = self._t_norm(truth1, truth2, type)
            
            # Добавляем в результат, если степень принадлежности > 0
            if new_truth > 0:
                result.add(param, round(new_truth, 2))
        
        return result

    def disjunction(self, secondSet: FuzzySet, type: str) -> FuzzySet:
        """Дизъюнкция (объединение) с различными нормами"""
        result = FuzzySet(f"{self._name}_OR_{secondSet._name}")
        
        # Получаем все уникальные параметры из обоих множеств
        all_params = set()
        for stmt in self._fuzzy_set:
            all_params.add(stmt.parameter)
        for stmt in secondSet._fuzzy_set:
            all_params.add(stmt.parameter)
        
        # Для каждого параметра вычисляем степень принадлежности
        for param in all_params:
            stmt1 = self._find_statement_by_parameter(param)
            stmt2 = secondSet._find_statement_by_parameter(param)
            
            truth1 = stmt1.truth_degree if stmt1 else 0.0
            truth2 = stmt2.truth_degree if stmt2 else 0.0
            
            # Применяем S-норму (дизъюнкцию)
            new_truth = self._s_norm(truth1, truth2, type)
            
            # Добавляем в результат
            result.add(param, round(new_truth, 2))
        
        return result

    def negate(self) -> FuzzySet:
        """Дополнение (отрицание)"""
        result = FuzzySet(f"NOT_{self._name}")
        for stmt in self._fuzzy_set:
            result._fuzzy_set.append(
                FuzzyStatement(
                    None, None, 
                    stmt.parameter, 
                    round(1.0 - stmt.truth_degree, 2)
                )
            ) 
        return result

    # === Базовые операции (min/max) ===

    def union(self, other: FuzzySet) -> FuzzySet:
        """Объединение по min/max (стандартное)"""
        return self.disjunction(other, "Минмакс")

    def intersection(self, other: FuzzySet) -> FuzzySet:
        """Пересечение по min/max (стандартное)"""
        return self.conjunction(other, "Минмакс")

    # === Удобные операторы ===

    def __or__(self, other: FuzzySet):
        return self.union(other)

    def __and__(self, other: FuzzySet):
        return self.intersection(other)

    def __repr__(self):
        items = ", ".join([f'{stmt.parameter}: {stmt.truth_degree}' for stmt in self._fuzzy_set])
        return f"FuzzySet({self._name!r}, {{{items}}})"

    # === Дополнительные методы ===

    def get_parameters(self) -> List[float]:
        """Возвращает список всех параметров"""
        return [stmt.parameter for stmt in self._fuzzy_set]

    def get_truth_degree(self, parameter: float) -> float:
        """Возвращает степень принадлежности для параметра"""
        stmt = self._find_statement_by_parameter(parameter)
        return stmt.truth_degree if stmt else 0.0

    def to_dict(self) -> Dict[float, float]:
        """Представляет множество в виде словаря {параметр: степень_принадлежности}"""
        return {stmt.parameter: stmt.truth_degree for stmt in self._fuzzy_set}