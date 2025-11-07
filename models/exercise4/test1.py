# Тестовый файл для проверки
from models.exercise4.inputs import Inputs
"""
а если у меня максимум у нескольких классов, то есть одинаковое значение по степени истинности для двух или трех 
классов, предлагаю сделать объединение по максимумам, вот так :"z = (z1*l1+z2+l2)/(l1+l2)" где z1  это центр 
усеченного класса по степени истинности по оси X, z2 это центр другого усеченного класса по оси X,  l1  это 
длина горизонтальной составляющей по тому же усесченному классу(этот класс до усекания выглядел как треугольник 
так как задавался тремя координатами - левой, средней и правой точкой, после усечения по степени истинности это 
будет выглядеть как трапеция, l1 это длина верхней горизонтальной грани трапеции)
"""

from typing import List, Dict
from dataclasses import dataclass

@dataclass
class TriFunc:
    name: str
    left_point: int
    center_point: int
    right_point: int

@dataclass
class OptTriFunc:
    name: str
    variant: List[TriFunc]

@dataclass
class Rule:
    name: str
    variant: List[Dict[str,str]]
    opt_rule: TriFunc

class Data:
    def __init__(self):
        self.rules = None
        self.opt_tri_func = None
        self._read_data()
    
    def _read_data(self):
        self.rules: List[Rule] = [
            Rule(
                "Bad",
                [
                    # Низкая цена, но плохие характеристики
                    {"Price":"Low","Memory":"Low","Weight":"High","ColorR":"Low","ColorG":"Low","ColorB":"Low"},
                    # Высокая цена, но плохие характеристики (плохое соотношение)
                    {"Price":"High","Memory":"Low","Weight":"High","ColorR":"Low","ColorG":"Low","ColorB":"Low"},
                    # Средняя цена, но очень плохие характеристики
                    {"Price":"Medium","Memory":"Low","Weight":"High","ColorR":"Low","ColorG":"Low","ColorB":"Low"},
                ],
                TriFunc("Bad", 0, 0, 30)
            ),
            Rule(
                "Average",
                [
                    # Средняя цена и средние характеристики
                    {"Price":"Medium","Memory":"Medium","Weight":"Medium","ColorR":"Medium","ColorG":"Medium","ColorB":"Medium"},
                    # Низкая цена, средние характеристики (хорошее соотношение)
                    {"Price":"Low","Memory":"Medium","Weight":"Medium","ColorR":"Medium","ColorG":"Medium","ColorB":"High"},
                    # Высокая цена, хорошая память, но тяжелый
                    {"Price":"High","Memory":"High","Weight":"High","ColorR":"High","ColorG":"Medium","ColorB":"Low"},
                    # Средняя цена, хорошая память, легкий
                    {"Price":"Medium","Memory":"High","Weight":"Low","ColorR":"Medium","ColorG":"High","ColorB":"Medium"},
                ],
                TriFunc("Average", 25, 50, 75)
            ),
            Rule(
                "Good",
                [
                    # Высокая цена, отличные характеристики
                    {"Price":"High","Memory":"High","Weight":"Low","ColorR":"High","ColorG":"High","ColorB":"High"},
                    # Средняя цена, хорошие характеристики (отличное соотношение)
                    {"Price":"Medium","Memory":"High","Weight":"Low","ColorR":"High","ColorG":"High","ColorB":"High"},
                    # Высокая цена, хорошая память и легкий вес
                    {"Price":"High","Memory":"High","Weight":"Low","ColorR":"High","ColorG":"High","ColorB":"Medium"},
                    # Средняя цена, отличная память, средний вес
                    {"Price":"Medium","Memory":"High","Weight":"Medium","ColorR":"High","ColorG":"High","ColorB":"High"},
                ],
                TriFunc("Good", 70, 100, 100)
            )
        ]

        self.opt_tri_func: List[OptTriFunc] = [
            OptTriFunc(
                "Price",
                [
                    TriFunc("Low", 0, 0, 400),
                    TriFunc("Medium", 300, 500, 700),
                    TriFunc("High", 600, 1000, 1000),
                ]
            ),
            OptTriFunc(
                "Memory",
                [
                    TriFunc("Low", 0, 0, 64),
                    TriFunc("Medium", 32, 128, 192),
                    TriFunc("High", 128, 256, 256),
                ]
            ),
            OptTriFunc(
                "Weight",
                [
                    TriFunc("Low", 100, 100, 400),
                    TriFunc("Medium", 300, 600, 900),
                    TriFunc("High", 700, 1000, 1000),
                ]
            ),
            OptTriFunc(
                "ColorR",
                [
                    TriFunc("Low", 0, 0, 128),
                    TriFunc("Medium", 64, 128, 192),
                    TriFunc("High", 128, 255, 255),
                ]
            ),
            OptTriFunc(
                "ColorG",
                [
                    TriFunc("Low", 0, 0, 128),
                    TriFunc("Medium", 64, 128, 192),
                    TriFunc("High", 128, 255, 255),
                ]
            ),
            OptTriFunc(
                "ColorB",
                [
                    TriFunc("Low", 0, 0, 128),
                    TriFunc("Medium", 64, 128, 192),
                    TriFunc("High", 128, 255, 255),
                ]
            )
        ]


# Тестовый файл для проверки

def test_fuzzy_system():
    from models.exercise4.fuzzy_logic import FuzzyLogic
    data = Data()
    fuzzy = FuzzyLogic()
    
    # Тест 1: Плохой товар (низкая цена, плохие характеристики)
    inputs1 = Inputs(
        price=200,      # Low
        memory=32,      # Low
        weight=900,     # High
        colorR=50,      # Low
        colorG=50,      # Low
        colorB=50       # Low
    )
    result1 = fuzzy.determine_membership_class(data, inputs1, "минимум")
    print(f"Тест 1 - Плохой товар: {result1.name}, степень: {result1.membership_degree:.3f}")
    
    # Тест 2: Средний товар
    inputs2 = Inputs(
        price=500,      # Medium
        memory=128,     # Medium
        weight=600,     # Medium
        colorR=128,     # Medium
        colorG=128,     # Medium
        colorB=128      # Medium
    )
    result2 = fuzzy.determine_membership_class(data, inputs2, "минимум")
    print(f"Тест 2 - Средний товар: {result2.name}, степень: {result2.membership_degree:.3f}")
    
    # Тест 3: Хороший товар (высокая цена, отличные характеристики)
    inputs3 = Inputs(
        price=800,      # High
        memory=200,     # High
        weight=200,     # Low
        colorR=200,     # High
        colorG=200,     # High
        colorB=200      # High
    )
    result3 = fuzzy.determine_membership_class(data, inputs3, "минимум")
    print(f"Тест 3 - Хороший товар: {result3.name}, степень: {result3.membership_degree:.3f}")
    
    # Тест 4: Граничный случай
    inputs4 = Inputs(
        price=500,      # Medium
        memory=180,     # High
        weight=300,     # Low
        colorR=180,     # High
        colorG=180,     # High
        colorB=180      # High
    )
    result4 = fuzzy.determine_membership_class(data, inputs4, "алгебраическое произведение")
    print(f"Тест 4 - Граничный случай: {result4.name}, степень: {result4.membership_degree:.3f}")
