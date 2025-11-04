from models.exercise4.data import Data, OptTriFunc, Rule
from models.exercise4.inputs import Inputs
from dataclasses import dataclass
from typing import List


@dataclass
class ClassMembership:
    name: str
    membership_degree: float


@dataclass
class TruthDegreeByClass:
    name: str
    truth_degree: float


@dataclass
class FuzzyEstimates:
    name: str
    truth_degree: float


@dataclass
class FuzzifyInput:
    name: str
    fuzzy_estimates: List[FuzzyEstimates]


class FuzzyLogic:
    def __init__(self):
        pass

    def determine_membership_class(self, data: Data, inputs: Inputs, norm: str) -> ClassMembership:
        fuzzify_inputs = self._fuzzify(inputs, data.opt_tri_func)
        truth_degrees_by_cls = self._calculating_truth_degree_by_class(fuzzify_inputs, data.rules, norm)
        class_membership = self._de_fuzzify(truth_degrees_by_cls, data.rules)
        return class_membership
    
    def _fuzzify(self, inputs: Inputs, opts: List[OptTriFunc]) -> List[FuzzifyInput]:
        """Фаззификация входных данных"""
        result = []
        
        # Создаем словарь для быстрого доступа к входным значениям
        input_values = {
            "Price": inputs.price,
            "Memory": inputs.memory,
            "Weight": inputs.weight,
            "ColorR": inputs.colorR,
            "ColorG": inputs.colorG,
            "ColorB": inputs.colorB
        }
        
        # Для каждого параметра
        for opt in opts:
            fuzzy_estimates = []
            
            # Получаем входное значение для текущего параметра
            input_value = input_values.get(opt.name)
            
            # print(opt.name)
            
            if input_value is not None:
                # Для каждой лингвистической переменной (Low, Medium, High)
                for tri_func in opt.variant:
                    # Вычисляем степень принадлежности
                    membership = self._triangle(
                        input_value,
                        tri_func.left_point,
                        tri_func.center_point,
                        tri_func.right_point
                    )
                    
                    fuzzy_estimates.append(
                        FuzzyEstimates(name=tri_func.name, truth_degree=membership)
                    )

                    # print(tri_func.name +" : "+ str(membership))
                # print("===========================")
            
            result.append(FuzzifyInput(name=opt.name, fuzzy_estimates=fuzzy_estimates))
        
        return result

    def _triangle(self, x, a, b, c) -> float:
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

    def _calculating_truth_degree_by_class(self, f_inputs: List[FuzzifyInput], rules: List[Rule], norm: str) -> List[TruthDegreeByClass]:
        """Вычисление степени истинности для каждого класса"""
        result = []
        
        for rule in rules:
            max_truth_degree = 0.0
            
            # Для каждого варианта правила
            for variant in rule.variant:
                # Получаем степени принадлежности для всех 6 параметров
                memberships = []
                
                for f_input in f_inputs:
                    # Получаем требуемое значение для текущего параметра
                    required_value = variant.get(f_input.name)
                    
                    if required_value:
                        # Находим степень принадлежности для требуемого значения
                        for estimate in f_input.fuzzy_estimates:
                            if estimate.name == required_value:
                                memberships.append(estimate.truth_degree)
                                break
                
                # Применяем конъюнкцию для всех 6 параметров
                if len(memberships) == 6:
                    truth_degree = self._conjunction(memberships, norm)
                    
                    # Берем максимум по всем вариантам (дизъюнкция)
                    max_truth_degree = max(max_truth_degree, truth_degree)
            
            result.append(TruthDegreeByClass(name=rule.name, truth_degree=max_truth_degree))
        
        return result

    def _conjunction(self, values: List[float], type: str) -> float:
        """Конъюнкция для произвольного количества значений"""
        if not values:
            return 0.0
        
        match type.lower():
            case "алгебраическое произведение":
                result = 1.0
                for v in values:
                    result *= v
                return result
            
            case "граничное произведение":
                return max(0, sum(values) - (len(values) - 1)) #max(0, a + b + c + d + e + f - 5)
            
            case "драстическое произведение":
                if all(v == 1.0 for v in values):
                    return 1.0
                elif any(v == 0.0 for v in values): #any(x == 0.0 for x in [a, b, c, d, e, f]):
                    return 0.0
                else:
                    return min(values) #min(a, b, c, d, e, f)
            
            case _:  # "Минимум" по умолчанию
                return min(values)
            

    def _de_fuzzify(self, truth_degrees_by_cls: List[TruthDegreeByClass], rules: List[Rule]) -> ClassMembership:
        """
        Дефаззификация методом центроида.
        Возвращает класс и координату X на оси абсцисс (не степень принадлежности!)
        """
        numerator = 0.0
        denominator = 0.0
        
        for i, truth_degree_cls in enumerate(truth_degrees_by_cls):
            # Получаем соответствующее правило
            rule = rules[i]
            
            # Центр треугольной функции результирующего класса (по оси X)
            center = rule.opt_rule.center_point
            
            # Степень истинности (высота усеченной функции принадлежности)
            mu = truth_degree_cls.truth_degree
            
            # Вычисляем числитель и знаменатель для центроида
            numerator += center * mu
            denominator += mu
        
        # Вычисляем центроид (координату X)
        if denominator == 0:
            # Если все степени истинности равны 0, возвращаем первый класс с координатой 0
            return ClassMembership(name=rules[0].name, membership_degree=0.0)
        
        centroid_x = numerator / denominator
        
        # Определяем класс: находим правило, в диапазон которого попадает centroid_x
        selected_class = None
        
        for rule in rules:
            left = rule.opt_rule.left_point
            right = rule.opt_rule.right_point
            
            # Проверяем, попадает ли centroid_x в диапазон класса
            if left <= centroid_x <= right:
                selected_class = rule.name
                break
        
        # Если не попали ни в один диапазон, выбираем класс с ближайшим центром
        if selected_class is None:
            min_distance = float('inf')
            for rule in rules:
                distance = abs(rule.opt_rule.center_point - centroid_x)
                if distance < min_distance:
                    min_distance = distance
                    selected_class = rule.name
        
        return ClassMembership(name=selected_class, membership_degree=centroid_x)