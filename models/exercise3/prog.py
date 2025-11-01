from nicegui import ui
import matplotlib.pyplot as plt
from io import BytesIO
import base64


# -----------------------------
# НЕЧЁТКАЯ ЛОГИКА
# -----------------------------

def triangle(x, a, b, c):
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
    



def fuzzify(value):
    """Фаззификация одного компонента RGB"""
    print(triangle(value, 0, 0, 128))
    print(triangle(value, 64, 128, 192))
    print(triangle(value, 128, 255, 255))
    print()
    print()
    print()
    print()
    return {
        'Low': triangle(value, 0, 0, 128),
        'Medium': triangle(value, 64, 128, 192),
        'High': triangle(value, 128, 255, 255)
    }


def infer(r, g, b):
    """Вывод предсказанного цвета и степени истинности"""
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

    fr = fuzzify(r)
    fg = fuzzify(g)
    fb = fuzzify(b)

    result = {}
    for color, (r_state, g_state, b_state) in rules.items():
        # truth = min(fr[r_state], fg[g_state], fb[b_state])
        truth = (fr[r_state] * fg[g_state] * fb[b_state]) ** (1/3)
        result[color] = truth

    best_color = max(result, key=result.get)
    return best_color, result[best_color]


# -----------------------------
# ВИЗУАЛИЗАЦИЯ
# -----------------------------

def plot_membership(value, channel_name):
    """Создаёт график треугольных функций для одного канала"""
    xs = list(range(0, 256))
    low = [triangle(x, 0, 0, 128) for x in xs]
    medium = [triangle(x, 64, 128, 192) for x in xs]
    high = [triangle(x, 128, 255, 255) for x in xs]

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
# FRONTEND (NiceGUI)
# -----------------------------

ui.label('🎨 Нечёткий предсказатель цвета (Fuzzy RGB Predictor)').classes('text-2xl text-center m-4')

with ui.row().classes('justify-center gap-4'):
    r_input = ui.number('R', value=128, min=0, max=255, step=1)
    g_input = ui.number('G', value=128, min=0, max=255, step=1)
    b_input = ui.number('B', value=128, min=0, max=255, step=1)

result_label = ui.label().classes('text-lg mt-4')
color_box = ui.html('<div style="width:120px;height:120px;border-radius:10px;margin-top:10px;"></div>')

# Контейнеры для графиков
r_plot = ui.html()
g_plot = ui.html()
b_plot = ui.html()


def update_graphs(r, g, b):
    """Обновление графиков"""
    r_plot.content = f'<img src="data:image/png;base64,{plot_membership(r, "Red")}">'
    g_plot.content = f'<img src="data:image/png;base64,{plot_membership(g, "Green")}">'
    b_plot.content = f'<img src="data:image/png;base64,{plot_membership(b, "Blue")}">'


def predict_color():
    r, g, b = r_input.value, g_input.value, b_input.value
    color, truth = infer(r, g, b)
    hex_color = f'#{int(r):02x}{int(g):02x}{int(b):02x}'

    result_label.text = f'Предсказанный цвет: {color} (степень истинности {truth:.2f})'
    color_box.content = f'<div style="width:120px;height:120px;border-radius:10px;background-color:{hex_color};border:1px solid #aaa;"></div>'
    update_graphs(r, g, b)


ui.button('Угадать цвет', on_click=predict_color).classes('mt-4')

ui.label('📊 Функции принадлежности для RGB:').classes('text-md mt-6 font-bold text-center')

with ui.row().classes('justify-center gap-4'):
    r_plot
    g_plot
    b_plot

# Первоначальная отрисовка
update_graphs(128, 128, 128)

ui.run(title='Fuzzy Color Predictor', reload=False)
