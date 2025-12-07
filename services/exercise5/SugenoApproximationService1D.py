import math
import numpy as np
from models.exercise5.data import Sample
from models.exercise5.model import SugenoModel1D
from models.exercise5.trainer_ls import SugenoLeastSquaresTrainer1D
from models.exercise5.rule import SugenoRule1D
from models.exercise5.membership import TriangularMF, GaussianMF


class TestFunction:
    """Базовый класс для тестовых функций"""
    def __init__(self, name, x_min, x_max):
        self.name = name
        self.x_min = x_min
        self.x_max = x_max
    
    def __call__(self, x):
        raise NotImplementedError


class SinFunction(TestFunction):
    def __init__(self):
        super().__init__("sin(x)", 0, 2 * math.pi)
    
    def __call__(self, x):
        return math.sin(x)


class CosFunction(TestFunction):
    def __init__(self):
        super().__init__("cos(x)", 0, 2 * math.pi)
    
    def __call__(self, x):
        return math.cos(x)


class PolynomialFunction(TestFunction):
    def __init__(self):
        super().__init__("0.1x² - x + 2", -5, 10)
    
    def __call__(self, x):
        return 0.1 * x**2 - x + 2


class ExponentialFunction(TestFunction):
    def __init__(self):
        super().__init__("e^(-x/2) * sin(2x)", 0, 10)
    
    def __call__(self, x):
        return math.exp(-x/2) * math.sin(2*x)


class ComplexFunction(TestFunction):
    def __init__(self):
        super().__init__("sin(x) + 0.5*cos(2x)", 0, 2 * math.pi)
    
    def __call__(self, x):
        return math.sin(x) + 0.5 * math.cos(2*x)


class TanhFunction(TestFunction):
    def __init__(self):
        super().__init__("tanh(x)", -3, 3)
    
    def __call__(self, x):
        return math.tanh(x)


class StepFunction(TestFunction):
    def __init__(self):
        super().__init__("Ступенька", -2, 8)
    
    def __call__(self, x):
        if x < 1:
            return 0
        elif x < 3:
            return 1
        elif x < 5:
            return 0.5
        else:
            return 1.5


AVAILABLE_FUNCTIONS = {
    "sin(x)": SinFunction(),
    "cos(x)": CosFunction(),
    "0.1x² - x + 2": PolynomialFunction(),
    "e^(-x/2) * sin(2x)": ExponentialFunction(),
    "sin(x) + 0.5*cos(2x)": ComplexFunction(),
    "tanh(x)": TanhFunction(),
    "Ступенька": StepFunction()
}


class SugenoApproximationService1D:
    def __init__(self, x_min, x_max, rules_count, mf_type="triangular", sigma_factor=0.6, min_points_per_rule=3):
        self.x_min = x_min
        self.x_max = x_max
        self.rules_count = rules_count
        self.mf_type = mf_type
        self.sigma_factor = sigma_factor
        
        self.rules = [
            SugenoRule1D(mf)
            for mf in self._create_overlapping_mfs(x_min, x_max, rules_count, mf_type, sigma_factor)
        ]

        self.model = SugenoModel1D(self.rules)
        self.trainer = SugenoLeastSquaresTrainer1D(self.model)
        self.min_points_per_rule = min_points_per_rule
    
    def train(self, samples):
        """Обучает модель на выборке"""
        buckets = self._assign_points_to_rules(samples, self.rules)
        self._check_points_per_rule(buckets, self.min_points_per_rule)
        self.trainer.train(samples)

    def predict(self, x):
        """Предсказывает значение для одной точки"""
        return self.model.predict(x)
    
    def predict_multiple(self, x_values):
        """Предсказывает значения для массива точек"""
        return [self.model.predict(x) for x in x_values]

    def _create_overlapping_mfs(self, x_min, x_max, rules_count, mf_type, sigma_factor):
        """Создает перекрывающиеся функции принадлежности"""
        mfs = []

        if mf_type == "triangular":
            step = (x_max - x_min) / (rules_count - 1)
            for i in range(rules_count):
                center = x_min + i * step
                a = center - step
                c = center + step
                mfs.append(TriangularMF(a, center, c))
        
        elif mf_type == "gaussian":
            step = (x_max - x_min) / (rules_count - 1)
            sigma = step * sigma_factor  # Настраиваемое перекрытие
            for i in range(rules_count):
                center = x_min + i * step
                mfs.append(GaussianMF(center, sigma))
        
        else:
            raise ValueError(f"Неизвестный тип функции принадлежности: {mf_type}")

        return mfs
    
    def _assign_points_to_rules(self, samples, rules):
        """Распределяет точки по правилам"""
        buckets = {i: [] for i in range(len(rules))}

        for s in samples:
            strengths = [r.firing_strength(s.x) for r in rules]
            best = max(range(len(rules)), key=lambda i: strengths[i])
            buckets[best].append(s)

        return buckets
    
    def _check_points_per_rule(self, buckets, min_points):
        """Проверяет достаточное количество точек для каждого правила"""
        for rule_id, pts in buckets.items():
            if len(pts) < min_points:
                raise ValueError(
                    f"Правило {rule_id} имеет только {len(pts)} точек, требуется минимум {min_points}"
                )

    def calculate_error_metrics(self, test_samples):
        """Вычисляет метрики ошибок"""
        errors = []
        for sample in test_samples:
            y_pred = self.model.predict(sample.x)
            errors.append(abs(sample.y - y_pred))
        
        mae = np.mean(errors)  # Mean Absolute Error
        mse = np.mean([e**2 for e in errors])  # Mean Squared Error
        rmse = math.sqrt(mse)  # Root Mean Squared Error
        
        return {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'max_error': max(errors)
        }