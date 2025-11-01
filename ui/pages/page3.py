from nicegui import ui
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class Page3:
    """
    Класс-страница NiceGUI, инкапсулирующий вашу оригинальную логику.
    Страница доступна по пути /page3
    """
    def __init__(self):
        # --- создаём страницу NiceGUI ---
        self._build_ui()
        # первоначальная отрисовка значений 128,128,128
        self.update_graphs(128, 128, 128)

    # -----------------------------
    # НЕЧЁТКАЯ ЛОГИКА (оригинальная, без изменений)
    # -----------------------------
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

    def fuzzify(self, value):
        """Фаззификация одного компонента RGB (как было в вашем коде)"""
        # сохраняем оригинальные debug-print'ы (не меняем логику)
        print(self.triangle(value, 0, 0, 128))
        print(self.triangle(value, 64, 128, 192))
        print(self.triangle(value, 128, 255, 255))
        print()
        print()
        print()
        print()
        return {
            'Low': self.triangle(value, 0, 0, 128),
            'Medium': self.triangle(value, 64, 128, 192),
            'High': self.triangle(value, 128, 255, 255)
        }

    def infer(self, r, g, b):
        """Вывод предсказанного цвета и степени истинности (логика не изменена)"""
        rules = {
            'Red':     ('High', 'Low', 'Low'),
            'Green':   ('Low', 'High', 'Low'),
            'Blue':    ('Low', 'Low', 'High'),
            'Yellow':  ('High', 'High', 'Low'),
            'Cyan':    ('Low', 'High', 'High'),
            'Magenta': ('High', 'Low', 'High'),
            'White':   ('High', 'High', 'High'),
            'Black':   ('Low', 'Low', 'Low'),
            'Gray':    ('Medium', 'Medium', 'Medium')
        }

        fr = self.fuzzify(r)
        fg = self.fuzzify(g)
        fb = self.fuzzify(b)

        result = {}
        for color, (r_state, g_state, b_state) in rules.items():
            # truth = min(fr[r_state], fg[g_state], fb[b_state])
            truth = (fr[r_state] * fg[g_state] * fb[b_state]) ** (1/3)
            result[color] = truth

        best_color = max(result, key=result.get)
        return best_color, result[best_color]

    # -----------------------------
    # ВИЗУАЛИЗАЦИЯ (оригинальная, только вынесена в методы класса)
    # -----------------------------
    def plot_membership(self, value, channel_name):
        """Создаёт график треугольных функций для одного канала и возвращает base64 PNG"""
        xs = list(range(0, 256))
        low = [self.triangle(x, 0, 0, 128) for x in xs]
        medium = [self.triangle(x, 64, 128, 192) for x in xs]
        high = [self.triangle(x, 128, 255, 255) for x in xs]

        plt.figure(figsize=(4, 2.2))
        plt.plot(xs, low, label='Low', color='blue')
        plt.plot(xs, medium, label='Medium', color='orange')
        plt.plot(xs, high, label='High', color='green')
        plt.axvline(value, color='red', linestyle='--', label=f'Value = {value}')
        plt.title(f'{channel_name} Component')
        plt.xlabel('Value')
        plt.ylabel('Membership degree')
        plt.ylim(-0.05, 1.05)
        plt.legend(fontsize=8)
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        return base64.b64encode(buf.getvalue()).decode('utf-8')

    # -----------------------------
    # FRONTEND (NiceGUI) — собран из оригинальных элементов
    # -----------------------------
    def _build_ui(self):
        ui.label('🎨 Нечёткий предсказатель цвета (Fuzzy RGB Predictor)').classes('text-2xl text-center m-4')

        with ui.row().classes('justify-center gap-4'):
            self.r_input = ui.number('R', value=128, min=0, max=255, step=1)
            self.g_input = ui.number('G', value=128, min=0, max=255, step=1)
            self.b_input = ui.number('B', value=128, min=0, max=255, step=1)

        self.result_label = ui.label().classes('text-lg mt-4')
        # используем ui.html, чтобы полностью сохранить оригинальную разметку
        self.color_box = ui.html('<div style="width:120px;height:120px;border-radius:10px;margin-top:10px;"></div>',       sanitize=False)

        # Контейнеры для графиков
        self.r_plot = ui.html(    sanitize=False)
        self.g_plot = ui.html(    sanitize=False)
        self.b_plot = ui.html(    sanitize=False)

        # Кнопка — привязка на метод класса
        ui.button('Угадать цвет', on_click=self.predict_color).classes('mt-4')

        ui.label('📊 Функции принадлежности для RGB:').classes('text-md mt-6 font-bold text-center')

        with ui.row().classes('justify-center gap-4'):
            # вставляем html-виджеты (они будут обновляться методом update_graphs)
            self.r_plot
            self.g_plot
            self.b_plot

    def update_graphs(self, r, g, b):
        """Обновление графиков (как в оригинале)"""
        self.r_plot.content = f'<img src="data:image/png;base64,{self.plot_membership(r, "Red")}">'
        self.g_plot.content = f'<img src="data:image/png;base64,{self.plot_membership(g, "Green")}">'
        self.b_plot.content = f'<img src="data:image/png;base64,{self.plot_membership(b, "Blue")}">'

    def predict_color(self):
        """Обработчик кнопки — вызывает infer и обновляет UI"""
        r, g, b = self.r_input.value, self.g_input.value, self.b_input.value
        color, truth = self.infer(r, g, b)
        hex_color = f'#{int(r):02x}{int(g):02x}{int(b):02x}'

        # обновляем текст и цветовую панель точно так же, как в оригинале
        self.result_label.text = f'Предсказанный цвет: {color} (степень истинности {truth:.2f})'
        self.color_box.content = f'<div style="width:120px;height:120px;border-radius:10px;background-color:{hex_color};border:1px solid #aaa;"></div>'
        # и обновим графики
        self.update_graphs(r, g, b)

