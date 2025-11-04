from dataclasses import dataclass
from typing import Dict, List
from models.exercise3.fuzzy_color_data import FuzzyColorData, TriFunc


@dataclass
class FuzzyValue:
    """Нечеткое значение для одного компонента"""
    low: float
    medium: float
    high: float


@dataclass
class ColorResult:
    """Результат определения цвета"""
    color_name: str
    truth_degree: float
    all_degrees: Dict[str, float]

class FuzzyColorLogic:
    """Основной класс нечеткой логики для определения цвета"""
    
    def __init__(self):
        self.data = FuzzyColorData()
    
    def determine_color(self, r: int, g: int, b: int, norm: str = "минимум") -> ColorResult:
        """
        Определяет цвет по RGB значениям
        
        Args:
            r: Красный компонент (0-255)
            g: Зеленый компонент (0-255)
            b: Синий компонент (0-255)
            norm: Тип нормы для конъюнкции
            
        Returns:
            ColorResult с названием цвета и степенью истинности
        """
        # Фаззификация
        fuzzy_r = self._fuzzify(r)
        fuzzy_g = self._fuzzify(g)
        fuzzy_b = self._fuzzify(b)
        
        # Вывод (inference)
        color_degrees = self._infer(fuzzy_r, fuzzy_g, fuzzy_b, norm)
        
        # Дефаззификация (выбор максимума)
        best_color = max(color_degrees, key=color_degrees.get)
        
        return ColorResult(
            color_name=best_color,
            truth_degree=color_degrees[best_color],
            all_degrees=color_degrees
        )
    
    def _triangle(self, x: float, a: float, b: float, c: float) -> float:
        """
        Треугольная функция принадлежности
        
        Args:
            x: Входное значение
            a: Левая граница (y=0)
            b: Вершина (y=1)
            c: Правая граница (y=0)
            
        Returns:
            Степень принадлежности [0, 1]
        """
        if a == b == c:
            return 1.0 if x == a else 0.0
        elif a == b:  # Вершина совпадает с началом
            if x <= a:
                return 1.0
            elif x <= c:
                return max(0, (c - x) / (c - a))
            else:
                return 0.0
        elif b == c:  # Вершина совпадает с концом
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
    
    def _fuzzify(self, value: int) -> FuzzyValue:
        """
        Фаззификация одного компонента RGB
        
        Args:
            value: Значение компонента (0-255)
            
        Returns:
            FuzzyValue с степенями принадлежности к Low, Medium, High
        """
        low = self._triangle(value, 0, 0, 128)
        medium = self._triangle(value, 64, 128, 192)
        high = self._triangle(value, 128, 255, 255)
        
        return FuzzyValue(low=low, medium=medium, high=high)
    
    def _infer(self, fuzzy_r: FuzzyValue, fuzzy_g: FuzzyValue, 
               fuzzy_b: FuzzyValue, norm: str) -> Dict[str, float]:
        """
        Нечеткий вывод по правилам
        
        Args:
            fuzzy_r: Нечеткое значение красного
            fuzzy_g: Нечеткое значение зеленого
            fuzzy_b: Нечеткое значение синего
            norm: Тип нормы для конъюнкции
            
        Returns:
            Словарь {цвет: степень_истинности}
        """
        result = {}
        
        # Преобразуем FuzzyValue в словарь для удобства
        r_dict = {"Low": fuzzy_r.low, "Medium": fuzzy_r.medium, "High": fuzzy_r.high}
        g_dict = {"Low": fuzzy_g.low, "Medium": fuzzy_g.medium, "High": fuzzy_g.high}
        b_dict = {"Low": fuzzy_b.low, "Medium": fuzzy_b.medium, "High": fuzzy_b.high}
        
        # Применяем каждое правило
        for rule in self.data.color_rules:
            r_membership = r_dict[rule.r_state]
            g_membership = g_dict[rule.g_state]
            b_membership = b_dict[rule.b_state]
            
            # Вычисляем степень истинности правила через конъюнкцию
            truth = self._conjunction([r_membership, g_membership, b_membership], norm)
            result[rule.name] = truth
        
        return result
    
    def _conjunction(self, values: List[float], norm_type: str) -> float:
        """
        Конъюнкция (И) для нечетких значений
        
        Args:
            values: Список значений для конъюнкции
            norm_type: Тип нормы
            
        Returns:
            Результат конъюнкции
        """
        if not values:
            return 0.0
        
        match norm_type.lower():
            case "минимум":
                return min(values)
            
            case "алгебраическое произведение":
                result = 1.0
                for v in values:
                    result *= v
                return result
            
            case "граничное произведение":
                return max(0, sum(values) - (len(values) - 1))
            
            case "драстическое произведение":
                if all(v == 1.0 for v in values):
                    return 1.0
                elif any(v == 0.0 for v in values):
                    return 0.0
                else:
                    return min(values)
            
            case "среднее геометрическое":
                # Дополнительный метод: среднее геометрическое
                result = 1.0
                for v in values:
                    result *= v
                return result ** (1.0 / len(values))
            
            case _:
                return min(values)
    
    def get_rgb_functions(self) -> List[TriFunc]:
        """Возвращает треугольные функции для визуализации"""
        return self.data.rgb_functions
    
    def get_membership_values(self, value: int) -> Dict[str, float]:
        """
        Получить степени принадлежности для визуализации
        
        Args:
            value: Значение компонента (0-255)
            
        Returns:
            Словарь {Low: ..., Medium: ..., High: ...}
        """
        fuzzy = self._fuzzify(value)
        return {
            "Low": fuzzy.low,
            "Medium": fuzzy.medium,
            "High": fuzzy.high
        }