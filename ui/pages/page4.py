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
                        self.memory_input = ui.number(label="Память (ГБ)", value=8, min=0, max=128, step=1).classes("w-64")
                        self.weight_input = ui.number(label="Вес (г)", value=200, min=0, max=2000, step=10).classes("w-64")

                        ui.button("Рассчитать", on_click=self.calculate).classes("mt-4")

                    # ---- Правая часть: вывод результатов ----
                    with ui.column().classes("gap-4 w-1/2"):
                        ui.label("Результат классификации").classes("text-xl font-bold")

                        self.result_label = ui.label("Пока нет данных").classes("text-lg text-gray-600")
                        self.membership_label = ui.label("").classes("text-base text-gray-500")

                # ======= Визуализация треугольных функций =======
                with ui.row().classes("w-full flex-wrap justify-around gap-8"):
                    ui.label("Функции принадлежности").classes("text-xl font-bold text-center w-full")

                    self.figures = {}
                    for param in ["Price", "Memory", "Weight", "ColorR", "ColorG", "ColorB"]:
                        with ui.column().classes("items-center"):
                            ui.label(param).classes("font-semibold")
                            self.figures[param] = ui.image().classes("border w-[320px] h-[220px] object-contain")

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

        # Создаём Inputs
        inputs = Inputs(price, memory, weight, r, g, b)

        # Вызываем нечеткую систему
        result = self.logic.determine_membership_class(self.data, inputs, norm="Минимум")

        # Обновляем результат
        self.result_label.text = f"Класс: {result.name}"
        self.membership_label.text = f"Степень принадлежности: {result.membership_degree:.3f}"

        # Рисуем графики
        self._update_graphs(inputs)

    # --------------------------------------------------------
    # Построение треугольных функций
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
            ax.axvline(value, color='red', linestyle='--', linewidth=2)
            ax.set_title(param_name)
            ax.set_xlabel("Значение")
            ax.set_ylabel("Степень принадлежности")
            ax.legend(loc="upper right", fontsize=8)
            ax.grid(True)

            # Сохраняем в base64 и выводим
            buffer = io.BytesIO()
            plt.tight_layout()
            fig.savefig(buffer, format='png')
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
