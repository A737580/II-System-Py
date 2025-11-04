from nicegui import ui
import matplotlib.pyplot as plt
import io
import base64

from models.exercise4.data import Data
from models.exercise4.inputs import Inputs
from models.exercise4.fuzzy_logic import FuzzyLogic 


class Page4:
    def __init__(self):
        self.logic = FuzzyLogic()
        self.data = Data()
        self.current_result = None  # Для хранения результата расчета

        # ======= Основной макет =======
        with ui.row().classes("w-full justify-center"):
            with ui.column().classes("border-2 border-blue-200 w-[1100px] mx-auto h-full px-6 pb-6 gap-10 bg-gray-50"):

                ui.label("Нечёткая логика: классификация параметров").classes("text-2xl font-bold text-center")

                # ======= Ввод параметров =======
                with ui.row().classes("w-full gap-16 items-start"):

                    # ---- Левая часть: ввод параметров ----
                    with ui.column().classes("gap-3 w-1/3"):
                        ui.label("Ввод данных").classes("text-xl font-bold")
                        self.color_picker = ui.color_input(label='Цвет (RGB)', value='#000000').classes("w-64")
                        self.price_input = ui.number(label="Цена (₽)", value=500, min=0, max=2000, step=10).classes("w-64")
                        self.memory_input = ui.number(label="Память (ГБ)", value=8, min=0, max=256, step=1).classes("w-64")
                        self.weight_input = ui.number(label="Вес (г)", value=200, min=0, max=2000, step=10).classes("w-64")
                        
                        # Комбобокс для выбора типа конъюнкции
                        self.conjunction_select = ui.select(
                            label="Тип конъюнкции",
                            options=[
                                "минимум",
                                "алгебраическое произведение",
                                "граничное произведение",
                                "драстическое произведение"
                            ],
                            value="минимум"
                        ).classes("w-64")

                        ui.button("Рассчитать", on_click=self.calculate).classes("mt-4")

                    # ---- Правая часть: вывод результатов ----
                    with ui.column().classes("gap-4 w-1/2"):
                        ui.label("Результат классификации").classes("text-xl font-bold")

                        self.result_label = ui.label("Пока нет данных").classes("text-lg text-gray-600")
                        self.membership_label = ui.label("").classes("text-base text-gray-500")

                # ======= График выходных классов =======
                with ui.column().classes("w-full items-center gap-4 mt-6"):
                    ui.label("Выходные классы (результат дефаззификации)").classes("text-xl font-bold text-center")
                    self.output_figure = ui.image().classes("border w-[800px] h-[400px] object-contain")

                # ======= Визуализация треугольных функций =======
                with ui.row().classes("w-full flex-wrap justify-around gap-8"):
                    ui.label("Функции принадлежности входных параметров").classes("text-xl font-bold text-center w-full")

                    self.figures = {}
                    for param in ["Price", "Memory", "Weight", "ColorR", "ColorG", "ColorB"]:
                        with ui.column().classes("items-center"):
                            ui.label(param).classes("font-semibold")
                            self.figures[param] = ui.image().classes("border w-[320px] h-[220px] object-contain")

        # Рисуем начальный график выходных классов
        self._draw_output_classes()

    # --------------------------------------------------------
    # Расчёт и отрисовка
    # --------------------------------------------------------
    def calculate(self):
        """Обработка введённых данных"""
        # Получаем значения
        color_hex = self.color_picker.value or "#000000"
        r, g, b = self._hex_to_rgb(color_hex)
        price = int(self.price_input.value)
        memory = int(self.memory_input.value)
        weight = int(self.weight_input.value)
        
        # Получаем выбранный тип конъюнкции
        norm = self.conjunction_select.value

        # Создаём Inputs
        inputs = Inputs(price, memory, weight, r, g, b)

        # Вызываем нечеткую систему
        result = self.logic.determine_membership_class(self.data, inputs, norm=norm)
        self.current_result = result

        # Обновляем результат
        self.result_label.text = f"Класс: {result.name}"
        self.membership_label.text = f"Координата X (центроид): {result.membership_degree:.2f}"

        # Рисуем графики
        self._update_graphs(inputs)
        self._draw_output_classes(result.membership_degree)

    # --------------------------------------------------------
    # Построение графика выходных классов
    # --------------------------------------------------------
    def _draw_output_classes(self, centroid_x=None):
        """Рисует треугольные функции выходных классов и вертикальную линию центроида"""
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Рисуем треугольные функции для каждого класса
        colors = {'Bad': 'red', 'Average': 'orange', 'Good': 'green'}
        
        for rule in self.data.rules:
            tri = rule.opt_rule
            x = [tri.left_point, tri.center_point, tri.right_point]
            y = [0, 1, 0]
            color = colors.get(rule.name, 'blue')
            ax.plot(x, y, label=rule.name, linewidth=2, color=color)
            ax.fill(x, y, alpha=0.2, color=color)
        
        # Если есть результат расчета, рисуем вертикальную линию
        if centroid_x is not None:
            ax.axvline(centroid_x, color='blue', linestyle='--', linewidth=3, 
                      label=f'Центроид: {centroid_x:.2f}')
        
        ax.set_title("Выходные классы", fontsize=14, fontweight='bold')
        ax.set_xlabel("Значение (координата X)", fontsize=12)
        ax.set_ylabel("Степень принадлежности", fontsize=12)
        ax.set_xlim(-5, 105)
        ax.set_ylim(0, 1.1)
        ax.legend(loc="upper right", fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Сохраняем в base64
        buffer = io.BytesIO()
        plt.tight_layout()
        fig.savefig(buffer, format='png', dpi=100)
        buffer.seek(0)
        img_b64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close(fig)
        
        self.output_figure.source = f"data:image/png;base64,{img_b64}"

    # --------------------------------------------------------
    # Построение треугольных функций входных параметров
    # --------------------------------------------------------
    def _update_graphs(self, inputs: Inputs):
        """Перерисовать треугольные функции для каждого параметра"""
        params = {
            "Price": inputs.price,
            "Memory": inputs.memory,
            "Weight": inputs.weight,
            "ColorR": inputs.colorR,
            "ColorG": inputs.colorG,
            "ColorB": inputs.colorB,
        }

        for opt in self.data.opt_tri_func:
            param_name = opt.name
            value = params[param_name]

            fig, ax = plt.subplots(figsize=(3.5, 2.3))
            for tri in opt.variant:
                x = [tri.left_point, tri.center_point, tri.right_point]
                y = [0, 1, 0]
                ax.plot(x, y, label=tri.name)
            
            # Вертикальная линия для текущего значения
            ax.axvline(value, color='red', linestyle='--', linewidth=2, label=f'Значение: {value}')
            ax.set_title(param_name)
            ax.set_xlabel("Значение")
            ax.set_ylabel("μ")
            ax.legend(loc="upper right", fontsize=7)
            ax.grid(True, alpha=0.3)

            # Сохраняем в base64 и выводим
            buffer = io.BytesIO()
            plt.tight_layout()
            fig.savefig(buffer, format='png', dpi=80)
            buffer.seek(0)
            img_b64 = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close(fig)

            self.figures[param_name].source = f"data:image/png;base64,{img_b64}"

    # --------------------------------------------------------
    # Вспомогательные методы
    # --------------------------------------------------------
    def _hex_to_rgb(self, hex_color: str):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))