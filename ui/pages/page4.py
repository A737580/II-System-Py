from nicegui import ui
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class Page4:
    """🎛️ Нечёткая экспертная система: оценка устройства по цене, памяти, весу и цвету"""

    def __init__(self):
        self._build_ui()
        self.update_all()

    # --- базовые функции нечёткой логики ---
    def triangle(self, x, a, b, c):
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

    def fuzzify(self, variable, value):
        """Фаззификация входных данных"""
        if variable == 'price':
            return {
                'Low': self.triangle(value, 0, 0, 400),
                'Medium': self.triangle(value, 300, 500, 700),
                'High': self.triangle(value, 600, 1000, 1000)
            }
        elif variable == 'memory':
            return {
                'Low': self.triangle(value, 0, 0, 64),
                'Medium': self.triangle(value, 32, 128, 192),
                'High': self.triangle(value, 128, 256, 256)
            }
        elif variable == 'weight':
            return {
                'Light': self.triangle(value, 100, 100, 400),
                'Medium': self.triangle(value, 300, 600, 900),
                'Heavy': self.triangle(value, 700, 1000, 1000)
            }
        elif variable == 'color':
            return {
                'Dark': self.triangle(value, 0, 0, 128),
                'Bright': self.triangle(value, 128, 255, 255)
            }

    def _conjunction(self,a: float, b: float, c: float, d: float, type: str) -> float:
        match type.lower():
            case "алгебраическое произведение":
                return a * b * c * d
            case "граничное произведение":
                return max(0, a + b + c + d - 3)
            case "драстическое произведение":
                if a == 1.0 and b == 1.0 and c == 1.0 and d == 1.0:
                    return 1.0
                elif any(x == 0.0 for x in [a, b, c, d]):
                    return 0.0
                else:
                    return min(a, b, c, d)
            case _:  # "Минимум" по умолчанию
                return min(a, b, c, d)

    def _find_x_from_membership(self, truth_degree_list: dict, triangles: dict) -> dict:
        """Найти x по y для всех треугольных функций."""
        result = {}
        
        for category, (a, b, c) in triangles.items():
            x_values = []
            y = truth_degree_list[category]
            # Левая сторона треугольника
            if a != b:
                x_left = a + y * (b - a)
                if a <= x_left <= b:
                    x_values.append(x_left)
            
            # Правая сторона треугольника  
            if b != c:
                x_right = c - y * (c - b)
                if b <= x_right <= c:
                    x_values.append(x_right)
            
            # Особый случай - вершина треугольника
            if y == 1.0 and len(x_values) > 1:
                x_values = [b]  # только вершина
            
            result[category] = x_values
    
        return result   
    def check_truth_degrees(self,corners:dict,degrees:dict):
        #написать вычисление дефазификацию для каждого из треугольников и по правилу


    def infer(self, price, memory, weight, color, norm:str):
        """База правил + вывод"""
        fp = self.fuzzify('price', price)
        fm = self.fuzzify('memory', memory)
        fw = self.fuzzify('weight', weight)
        fc = self.fuzzify('color', color)

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
                
                vals.append(self._conjunction(μ_price,μ_mem,μ_w,μ_c, norm)) # считается иначе получаются нули при проходе по правилу и все правило становится нулевым
            result[label] = max(vals)

        # дефаззификация (взвешенное среднее) 
        triangles = {'Bad': (0,0,25), 'Average': (20,50,80), 'Good': (75,100,100)}
        c_answers = self._find_x_from_membership(result, triangles)

        numerator = sum(result[k] * numeric[k] for k in result)
        denominator = sum(result.values())
        crisp = numerator / denominator if denominator > 0 else 0

        # определяем словесный класс
        best = max(result, key=result.get)
        return best, crisp, result

    # --- визуализация функций принадлежности ---
    def plot_membership(self, variable, value):
        xs = []
        sets = {}
        if variable == 'price':
            xs = list(range(0, 1001, 10))
            sets = {
                'Low': [self.triangle(x, 0, 0, 400) for x in xs],
                'Medium': [self.triangle(x, 300, 500, 700) for x in xs],
                'High': [self.triangle(x, 600, 1000, 1000) for x in xs],
            }
            title, xlabel = 'Цена', '₽'
        elif variable == 'memory':
            xs = list(range(0, 257, 4))
            sets = {
                'Low': [self.triangle(x, 0, 0, 64) for x in xs],
                'Medium': [self.triangle(x, 32, 128, 192) for x in xs],
                'High': [self.triangle(x, 128, 256, 256) for x in xs],
            }
            title, xlabel = 'Память', 'ГБ'
        elif variable == 'weight':
            xs = list(range(100, 1001, 20))
            sets = {
                'Light': [self.triangle(x, 100, 100, 400) for x in xs],
                'Medium': [self.triangle(x, 300, 600, 900) for x in xs],
                'Heavy': [self.triangle(x, 700, 1000, 1000) for x in xs],
            }
            title, xlabel = 'Вес', 'грамм'
        elif variable == 'color':
            xs = list(range(0, 256, 4))
            sets = {
                'Dark': [self.triangle(x, 0, 0, 128) for x in xs],
                'Bright': [self.triangle(x, 128, 255, 255) for x in xs],
            }
            title, xlabel = 'Яркость цвета', '0–255'

        plt.figure(figsize=(4, 2.2))
        for label, ys in sets.items():
            plt.plot(xs, ys, label=label)
        plt.axvline(value, color='red', linestyle='--', label=f'Value = {value}')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel('Membership')
        plt.ylim(-0.05, 1.05)
        plt.legend(fontsize=8)
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        return base64.b64encode(buf.getvalue()).decode('utf-8')

    # --- интерфейс ---
    def _build_ui(self):
        ui.label('🤖 Нечёткая система оценки устройства').classes('text-2xl text-center m-4')

        with ui.row().classes('justify-center gap-4'):
            self.price_input = ui.number('Цена (₽)', value=500, min=0, max=1000, step=50, on_change=self.update_all)
            self.memory_input = ui.number('Память (ГБ)', value=128, min=0, max=256, step=8, on_change=self.update_all)
            self.weight_input = ui.number('Вес (г)', value=500, min=100, max=1000, step=50, on_change=self.update_all)
            self.color_input = ui.numtriangleber('Яркость цвета', value=128, min=0, max=255, step=10, on_change=self.update_all)

        self.result_label = ui.label().classes('text-lg mt-4 text-center')
        self.bar = ui.linear_progress(value=0.5).props('color=green').classes('w-1/2 mx-auto mt-2')

        ui.label('📊 Функции принадлежности:').classes('text-md mt-6 font-bold text-center')

        with ui.row().classes('justify-center gap-4'):
            self.price_plot = ui.html()
            self.memory_plot = ui.html()
        with ui.row().classes('justify-center gap-4'):
            self.weight_plot = ui.html()
            self.color_plot = ui.html()

    # --- обновление ---
    def update_all(self, _=None):
        p, m, w, c = self.price_input.value, self.memory_input.value, self.weight_input.value, self.color_input.value
        label, crisp, fuzzy = self.infer(p, m, w, c)
        self.result_label.text = f'📱 Оценка устройства: {label} ({crisp:.2f})'
        self.bar.value = crisp / 10
        self.bar.props(f'color={"green" if label=="Good" else "orange" if label=="Average" else "red"}')
        # обновляем графики
        self.price_plot.content = f'<img src="data:image/png;base64,{self.plot_membership("price", p)}">'
        self.memory_plot.content = f'<img src="data:image/png;base64,{self.plot_membership("memory", m)}">'
        self.weight_plot.content = f'<img src="data:image/png;base64,{self.plot_membership("weight", w)}">'
        self.color_plot.content = f'<img src="data:image/png;base64,{self.plot_membership("color", c)}">'
