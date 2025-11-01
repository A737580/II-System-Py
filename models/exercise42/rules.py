from models.exercise4.tri_membership_func import TriMembershipFunc
from models.exercise4.user_param import UserParam
from models.exercise4.degree_truth_func import DegreeTruthFunc
from models.exercise4.category import Category
from typing import Dict, List, Tuple

TriMembershipList = List['TriMembershipFunc']
DegreeTruthList = List['DegreeTruthFunc']
ParamList = List['UserParam']

class Rules:

    def __init__(self, len_rule:int):
        self.len_rule = len_rule
        self._fuzzification_opt:Dict[str,List['TriMembershipFunc']] = dict()
        self._rules:Dict[str,List[Category]] = dict()
    
    def read_fuzzi_opt(self,fuzzi_opt:Dict[str,List['TriMembershipFunc']]):
        
        for name, values in fuzzi_opt.items():
            name = name.lower()
            if len(values) != self.len_rule:
                raise ValueError(f"Must contain exactly {self.len_rule} membership functions")
            
            if name not in self._fuzzification_opt:
                self._fuzzification_opt[name]=values
            else:
                raise ValueError(f"Key {name} contain exactly")
            
    def read_rules(self,rules:Dict[str,List[Category]]):
        for name, values in fuzzi_opt.items():
            name = name.lower()
            if len(values) != self.len_rule:
                raise ValueError(f"Must contain exactly {self.len_rule} membership functions")
            
            if name not in self._fuzzification_opt:
                self._fuzzification_opt[name]=values
            else:
                raise ValueError(f"Key {name} contain exactly")

    def clear(self):
        self._fuzzification_opt = dict()
        self.len_rule = None

    def _triangle(self, x, a, b, c):
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

    def _fuzzify(self, variable:str, value:int)->DegreeTruthList:
        """Фаззификация входных данных"""

        if variable not in self._fuzzification_opt:
                raise ValueError(f"Key {variable} not contains")
        
        degree_truth_list:DegreeTruthList = list()
        tri_membership_list:TriMembershipList = self._fuzzification_opt[variable]
        
        for tri_membership in tri_membership_list:
            degree_truth = self._triangle(tri_membership,value)
            degree_truth_list.append(DegreeTruthList(tri_membership.name, degree_truth))
        return degree_truth_list
       
    def _conjunction(degree_truth_list:DegreeTruthList, type: str)->float:
        new_truth_degree: float = 0.0
        match type:
            case "алгебраическая сумма":
                new_truth_degree = self._truth_degree * secondStatement.truth_degree
            case "граничная сумма":
                new_truth_degree = max(
                    0, self._truth_degree + secondStatement.truth_degree - 1
                )
            case "драстическая сумма":
                if self._truth_degree == 1.0:
                    new_truth_degree = secondStatement.truth_degree
                elif secondStatement.truth_degree == 1.0:
                    new_truth_degree = self._truth_degree
                else:
                    new_truth_degree = 0
            case _:
                new_truth_degree = min(self._truth_degree, secondStatement.truth_degree)
        new_base = f"{self._base_text} {self._category_text} И {secondStatement.base_text} {secondStatement.category_text}"
        
        return new_truth_degree
    

    def infer(self, params:ParamList, norm: str):
        if len(params)!=self.len_rule:
                raise ValueError(f"Contain exactly {self.len_rule} param from user")
        for param in params:
            degree_truth_list:DegreeTruthList = list()
            name = param.name.lower()
            value = param.value
            
            
            # Получаю степени истинности для каждой функций принадлежности, по name для функции категории для каждой функций принадлежности по value
            degree_truth_list = self._fuzzify(name,value)

            general_truth_degree = self._conjunction(degree_truth_list,norm)


        
        
        
        
        """База правил + вывод"""
        fp = self._fuzzify('price', price)
        fm = self._fuzzify('memory', memory)
        fw = self._fuzzify('weight', weight)
        fc = self._fuzzify('color', color)

        rules = {
            'Bad': [
                ('Low', 'Low', 'Light', None),
                ('Low', 'Low', 'Medium', None),
                ('High', 'Low', 'Heavy', None),
            ],
            'Average': [
                ('Medium', 'Medium', 'Medium', None),
                ('High', 'Low', 'Light', None),
                ('Low', 'High', 'Heavy', None),
            ],
            'Good': [
                ('Medium', 'High', 'Medium', 'Bright'),
                ('High', 'High', 'Medium', None),
                ('High', 'Medium', 'Light', None),
            ],
        }

        result = {'Bad': 0.0, 'Average': 0.0, 'Good': 0.0}
        for label, rule_set in rules.items():
            vals = []
            for r in rule_set:
                p, m, w, c = r
                μ_price = fp.get(p, 1.0)
                μ_mem = fm.get(m, 1.0)
                μ_w = fw.get(w, 1.0)
                μ_c = fc.get(c, 1.0) if c else 1.0
                vals.append((μ_price * μ_mem * μ_w * μ_c) ** (1/4)) # считается иначе получаются нули при проходе по правилу и все правило становится нулевым
            result[label] = max(vals)

        # дефаззификация (взвешенное среднее)
        numeric = {'Bad': 2, 'Average': 5, 'Good': 8}
        numerator = sum(result[k] * numeric[k] for k in result)
        denominator = sum(result.values())
        crisp = numerator / denominator if denominator > 0 else 0

        # определяем словесный класс
        best = max(result, key=result.get)
        return best, crisp, result


    

