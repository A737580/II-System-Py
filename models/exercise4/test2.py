from dataclasses import dataclass
from typing import List, Dict

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

class Inputs:
    def __init__(self, price: int, memory: int, weight: int, colorR: int, colorG: int, colorB: int):
        self.price = price
        self.memory = memory
        self.weight = weight
        self.colorR = colorR
        self.colorG = colorG
        self.colorB = colorB

class TestData:
    def __init__(self):
        self.rules = None
        self.opt_tri_func = None
        self._read_data()
    
    def _read_data(self):
        # Правила для классификации
        self.rules: List[Rule] = [
            Rule(
                "Bad",
                [
                    # Плохие комбинации
                    {"Price":"High","Memory":"Low","Weight":"High","ColorR":"Low","ColorG":"Low","ColorB":"Low"},
                    {"Price":"Low","Memory":"Low","Weight":"High","ColorR":"Low","ColorG":"Low","ColorB":"Low"},
                    {"Price":"Medium","Memory":"Low","Weight":"Medium","ColorR":"Low","ColorG":"Low","ColorB":"Medium"},
                ],
                TriFunc("Bad", 0, 15, 30)
            ),
            Rule(
                "Average",
                [
                    # Средние комбинации
                    {"Price":"Medium","Memory":"Medium","Weight":"Medium","ColorR":"Medium","ColorG":"Medium","ColorB":"Medium"},
                    {"Price":"Low","Memory":"Medium","Weight":"Low","ColorR":"Medium","ColorG":"Medium","ColorB":"High"},
                    {"Price":"Medium","Memory":"High","Weight":"Medium","ColorR":"High","ColorG":"Medium","ColorB":"Medium"},
                    {"Price":"High","Memory":"Medium","Weight":"Low","ColorR":"High","ColorG":"High","ColorB":"Low"},
                    {"Price":"Medium","Memory":"Low","Weight":"Medium","ColorR":"Low","ColorG":"Low","ColorB":"Medium"},
                    
                ],
                TriFunc("Average", 25, 50, 75)
            ),
            Rule(
                "Good",
                [
                    # Хорошие комбинации
                    {"Price":"Medium","Memory":"High","Weight":"Low","ColorR":"High","ColorG":"High","ColorB":"High"},
                    {"Price":"High","Memory":"High","Weight":"Low","ColorR":"High","ColorG":"High","ColorB":"High"},
                    {"Price":"High","Memory":"High","Weight":"Medium","ColorR":"High","ColorG":"High","ColorB":"Medium"},
                    {"Price":"Medium","Memory":"Low","Weight":"Medium","ColorR":"Low","ColorG":"Low","ColorB":"Medium"},

                ],
                TriFunc("Good", 70, 85, 100)
            )
        ]

        # Функции принадлежности для параметров
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
                    TriFunc("Medium", 48, 128, 192),
                    TriFunc("High", 160, 256, 256),
                ]
            ),
            OptTriFunc(
                "Weight",
                [
                    TriFunc("Low", 100, 100, 400),
                    TriFunc("Medium", 300, 600, 900),
                    TriFunc("High", 800, 1000, 1000),
                ]
            ),
            OptTriFunc(
                "ColorR",
                [
                    TriFunc("Low", 0, 0, 128),
                    TriFunc("Medium", 64, 128, 192),
                    TriFunc("High", 160, 255, 255),
                ]
            ),
            OptTriFunc(
                "ColorG",
                [
                    TriFunc("Low", 0, 0, 128),
                    TriFunc("Medium", 64, 128, 192),
                    TriFunc("High", 160, 255, 255),
                ]
            ),
            OptTriFunc(
                "ColorB",
                [
                    TriFunc("Low", 0, 0, 128),
                    TriFunc("Medium", 64, 128, 192),
                    TriFunc("High", 160, 255, 255),
                ]
            )
        ]


# ============================================
# ТЕСТОВЫЕ СЦЕНАРИИ
# ============================================

def run_tests():
    '''Граничный случай между двумя классами возникает при одинаковых правилах в классах, в двух  классах'''
    from models.exercise4.fuzzy_logic import FuzzyLogic
    
    data = TestData()
    logic = FuzzyLogic()
    
    print("="*70)
    print("ТЕСТИРОВАНИЕ НЕЧЕТКОЙ ЛОГИКИ С ДЕФАЗЗИФИКАЦИЕЙ")
    print("="*70)
    
    # # Тест 1: Явно плохой товар (один максимум)
    # print("\n" + "="*70)
    # print("ТЕСТ 1: Явно плохой товар")
    # print("-"*70)
    # inputs1 = Inputs(
    #     price=800,      # High
    #     memory=20,      # Low
    #     weight=950,     # High
    #     colorR=30,      # Low
    #     colorG=30,      # Low
    #     colorB=30       # Low
    # )
    # result1 = logic.determine_membership_class(data, inputs1, "минимум")
    # print(f"Входные данные: Price=800, Memory=20, Weight=950, RGB=(30,30,30)")
    # print(f"Результат: Класс '{result1.name}', X-координата: {result1.membership_degree:.2f}")
    # print(f"Ожидается: Bad, X около 15")
    
    # # Тест 2: Явно хороший товар (один максимум)
    # print("\n" + "="*70)
    # print("ТЕСТ 2: Явно хороший товар")
    # print("-"*70)
    # inputs2 = Inputs(
    #     price=700,      # Medium-High
    #     memory=220,     # High
    #     weight=250,     # Low
    #     colorR=200,     # High
    #     colorG=200,     # High
    #     colorB=200      # High
    # )
    # result2 = logic.determine_membership_class(data, inputs2, "минимум")
    # print(f"Входные данные: Price=700, Memory=220, Weight=250, RGB=(200,200,200)")
    # print(f"Результат: Класс '{result2.name}', X-координата: {result2.membership_degree:.2f}")
    # print(f"Ожидается: Good, X около 85")
    
    # # Тест 3: Средний товар (один максимум)
    # print("\n" + "="*70)
    # print("ТЕСТ 3: Средний товар")
    # print("-"*70)
    # inputs3 = Inputs(
    #     price=500,      # Medium
    #     memory=128,     # Medium
    #     weight=600,     # Medium
    #     colorR=128,     # Medium
    #     colorG=128,     # Medium
    #     colorB=128      # Medium
    # )
    # result3 = logic.determine_membership_class(data, inputs3, "минимум")
    # print(f"Входные данные: Price=500, Memory=128, Weight=600, RGB=(128,128,128)")
    # print(f"Результат: Класс '{result3.name}', X-координата: {result3.membership_degree:.2f}")
    # print(f"Ожидается: Average, X около 50")
    
    # # Тест 4: Граничный случай между Average и Good (возможны два максимума)
    # print("\n" + "="*70)
    # print("ТЕСТ 4: Граничный случай (Average-Good)")
    # print("-"*70)
    # inputs4 = Inputs(
    #     price=650,      # Medium-High (между Medium и High)
    #     memory=180,     # High
    #     weight=400,     # Medium-Low
    #     colorR=180,     # High
    #     colorG=180,     # High
    #     colorB=150      # Medium-High
    # )
    # result4 = logic.determine_membership_class(data, inputs4, "алгебраическое произведение")
    # print(f"Входные данные: Price=650, Memory=180, Weight=400, RGB=(180,180,150)")
    # print(f"Результат: Класс '{result4.name}', X-координата: {result4.membership_degree:.2f}")
    # print(f"Ожидается: Average или Good, X между 50-85")
    
    # # Тест 5: Специально созданный случай с двумя максимумами
    # print("\n" + "="*70)
    # print("ТЕСТ 5: Два класса с равными степенями истинности")
    # print("-"*70)
    # inputs5 = Inputs(
    #     price=500,      # Medium (точно)
    #     memory=128,     # Medium (точно)
    #     weight=600,     # Medium (точно)
    #     colorR=128,     # Medium (точно)
    #     colorG=128,     # Medium (точно)
    #     colorB=128      # Medium (точно)
    # )
    # # Используем драстическое произведение для получения разных результатов
    # result5a = logic.determine_membership_class(data, inputs5, "минимум")
    # result5b = logic.determine_membership_class(data, inputs5, "граничное произведение")
    # print(f"Входные данные: Price=500, Memory=128, Weight=600, RGB=(128,128,128)")
    # print(f"Результат (минимум): Класс '{result5a.name}', X: {result5a.membership_degree:.2f}")
    # print(f"Результат (граничное): Класс '{result5b.name}', X: {result5b.membership_degree:.2f}")
    
    # Тест 6: Граничный случай между Bad и Average
    print("\n" + "="*70)
    print("ТЕСТ 6: Граничный случай (Bad-Average)")
    print("-"*70)
    inputs6 = Inputs(
        price=350,      # Low-Medium
        memory=50,      # Low-Medium
        weight=700,     # Medium-High
        colorR=90,      # Low-Medium
        colorG=90,      # Low-Medium
        colorB=100      # Low-Medium
    )
    result6 = logic.determine_membership_class(data, inputs6, "минимум")
    print(f"Входные данные: Price=350, Memory=50, Weight=700, RGB=(90,90,100)")
    print(f"Результат: Класс '{result6.name}', X-координата: {result6.membership_degree:.2f}")
    print(f"Ожидается: Bad или Average, X между 15-50")
    
    # # Тест 7: Проверка разных типов конъюнкции
    # print("\n" + "="*70)
    # print("ТЕСТ 7: Сравнение разных типов конъюнкции")
    # print("-"*70)
    # inputs7 = Inputs(
    #     price=600,
    #     memory=150,
    #     weight=350,
    #     colorR=150,
    #     colorG=150,
    #     colorB=140
    # )
    # print(f"Входные данные: Price=600, Memory=150, Weight=350, RGB=(150,150,140)")
    
    # for norm in ["минимум", "алгебраическое произведение", "граничное произведение", "драстическое произведение"]:
    #     result = logic.determine_membership_class(data, inputs7, norm)
    #     print(f"  {norm:30s}: Класс '{result.name}', X: {result.membership_degree:.2f}")
    
    print("\n" + "="*70)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("="*70)
