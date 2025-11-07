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
                    # Плохие комбинации
                    {"Price":"High","Memory":"Low","Weight":"High","ColorR":"Low","ColorG":"Low","ColorB":"Low"},
                    {"Price":"Low","Memory":"Low","Weight":"High","ColorR":"Low","ColorG":"Low","ColorB":"Low"},
                    {"Price":"Medium","Memory":"Low","Weight":"High","ColorR":"Low","ColorG":"Low","ColorB":"Medium"},
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
                ],
                TriFunc("Good", 70, 85, 100)
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