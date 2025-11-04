from dataclasses import dataclass
from typing import List, Tuple, Dict


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
    opt_rule: TriFunc # ширина по Х в результирующих классах(bad,average,good)

class Data:
    """ 
    opt_tri_func: List[OptTriFunc]
    rules: List[Rule]
    
    class Rule:
        name: str
        variant: List[Tuple[str, str, str, str, str, str]]
    
    class OptTriFunc:
        name: str
        variant: List[TriFunc]

    class TriFunc:
        name: str
        left_point: int
        center_point: int
        right_point: int
    """
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