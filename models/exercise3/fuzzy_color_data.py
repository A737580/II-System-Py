from dataclasses import dataclass
from typing import Dict, Tuple, List


@dataclass
class TriFunc:
    """Треугольная функция принадлежности"""
    name: str
    left_point: float
    center_point: float
    right_point: float


@dataclass
class ColorRule:
    """Правило для определения цвета"""
    name: str
    r_state: str
    g_state: str
    b_state: str
    
class FuzzyColorData:
    """Класс с данными для нечеткой логики определения цвета"""
    
    def __init__(self):
        # Треугольные функции для RGB компонентов (0-255)
        self.rgb_functions: List[TriFunc] = [
            TriFunc("Low", 0, 0, 128),
            TriFunc("Medium", 64, 128, 192),
            TriFunc("High", 128, 255, 255)
        ]
        
        # Правила для определения цветов
        self.color_rules: List[ColorRule] = [
            ColorRule("Red", "High", "Low", "Low"),
            ColorRule("Green", "Low", "High", "Low"),
            ColorRule("Blue", "Low", "Low", "High"),
            ColorRule("Yellow", "High", "High", "Low"),
            ColorRule("Cyan", "Low", "High", "High"),
            ColorRule("Magenta", "High", "Low", "High"),
            ColorRule("White", "High", "High", "High"),
            ColorRule("Black", "Low", "Low", "Low"),
            ColorRule("Gray", "Medium", "Medium", "Medium"),
            ColorRule("Orange", "High", "Medium", "Low"),
            ColorRule("Purple", "Medium", "Low", "High"),
            ColorRule("Pink", "High", "Medium", "Medium"),
        ]