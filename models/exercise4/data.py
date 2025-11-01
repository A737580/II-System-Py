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
                    {"Price":"Low","Memory":"Low","Weight":"Low","ColorR":"Low","ColorG":"Low","ColorB":"Low"},
                    {"Price":"Low","Memory":"Low","Weight":"Medium","ColorR":"High","ColorG":"Low","ColorB":"Low"},
                    {"Price":"High","Memory":"Low","Weight":"High","ColorR":"Low","ColorG":"High","ColorB":"Low"}
                ],
                TriFunc("Bad",0,0,30) 
            ),
            Rule(
                "Average",
                [
                    {"Price":"Medium","Memory":"Medium","Weight":"Medium","ColorR":"Low","ColorG":"Low","ColorB":"High"},
                    {"Price":"High","Memory":"Low","Weight":"Low","ColorR":"High","ColorG":"Medium","ColorB":"Low"},
                    {"Price":"Low","Memory":"High","Weight":"High","ColorR":"Medium","ColorG":"High","ColorB":"Low"}
                ],
                TriFunc("Average",20,50,80) 
            ),
            Rule(
                "Good",
                [
                    {"Price":"Medium","Memory":"High","Weight":"Medium","ColorR":"High","ColorG":"High","ColorB":"High"},
                    {"Price":"High","Memory":"High","Weight":"Medium","ColorR":"High","ColorG":"Medium","ColorB":"Medium"},
                    {"Price":"High","Memory":"Medium","Weight":"Low","ColorR":"Medium","ColorG":"Medium","ColorB":"Low"}
                ],
                TriFunc("Good",70,100,100) 
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
