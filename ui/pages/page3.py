from nicegui import ui
import matplotlib.pyplot as plt
import io
import base64
from typing import List, Dict

from models.exercise3.fuzzy_color_logic import FuzzyColorLogic, ColorResult
from models.exercise3.fuzzy_color_data import FuzzyColorData, TriFunc


class Page3:
    """
    GUI для демонстрации нечеткой логики определения цвета по RGB.
    """
    
    def __init__(self):
        self.logic = FuzzyColorLogic()
        self.current_result: ColorResult = None
        
        # Словарь для хранения ссылок на UI элементы графиков
        self.figures: Dict[str, ui.image] = {}

        # ======= Основной макет =======
        with ui.row().classes("w-full justify-center"):
            with ui.column().classes("border-2 border-blue-200 w-[1100px] mx-auto h-full px-6 pb-6 gap-10 bg-gray-50"):

                ui.label("Нечёткая логика: Определение цвета по RGB").classes("text-2xl font-bold text-center w-full")

                # ======= Ввод данных и Результат =======
                with ui.row().classes("w-full gap-0 items-start"):
                    
                    # ---- Левая часть: Ввод ----
                    with ui.column().classes("gap-0 w-1/3"):
                        ui.label("Ввод данных").classes("text-xl font-bold")
                        
                        self.color_picker = ui.color_input(
                            label='Выберите цвет (RGB)', 
                            value='#FF0000', # Начнем с красного
                            on_change=self.calculate
                        ).classes("w-64")

                        # Поле для отображения выбранного цвета
                        self.color_swatch = ui.label().classes("w-64 h-24 border-2 border-gray-400")
                        
                        self.conjunction_select = ui.select(
                            label="Тип конъюнкции (t-норма)",
                            options=[
                                "минимум",
                                "алгебраическое произведение",
                                "граничное произведение",
                                "драстическое произведение",
                                "среднее геометрическое"
                            ],
                            value="минимум",
                            on_change=self.calculate
                        ).classes("w-64")
                        
                        # Кнопка не обязательна, т.к. есть on_change, но оставим для примера
                        # ui.button("Рассчитать", on_click=self.calculate).classes("mt-4")

                    # ---- Правая часть: Вывод результата ----
                    with ui.column().classes("gap-0 w-1/3"):
                        ui.label("Результат определения").classes("text-xl font-bold")
                        
                        self.result_label = ui.label().classes("text-2xl font-semibold text-gray-800")
                        self.result_degree = ui.label().classes("text-lg text-gray-600")

                        ui.label("Все степени истинности:").classes("text-lg font-semibold mt-4")
                    with ui.column().classes("gap-0 w-1/3"):
                        # Таблица для всех результатов
                        self.grid = ui.aggrid({
                            'columnDefs': [
                                {'headerName': 'Цвет', 'field': 'color', 'sortable': True, 'width': 150},
                                {'headerName': 'Степень', 'field': 'degree', 'sortable': True, 'width': 150, 'sort': 'desc'},
                            ],
                            'rowData': [],
                            'domLayout': 'autoHeight',
                        }).classes('w-[320px]')

                # ======= График выходных значений (Гистограмма) =======
                with ui.column().classes("w-full items-center gap-4 mt-6"):
                    ui.label("Степени истинности выходных цветов").classes("text-xl font-bold text-center")
                    self.output_figure = ui.image().classes("border w-full max-w-[900px] h-[450px] object-contain")

                # ======= Визуализация функций принадлежности (Вход) =======
                with ui.column().classes("w-full items-center gap-6 mt-6"):
                    ui.label("Функции принадлежности входных параметров (RGB)").classes("text-xl font-bold text-center w-full")
                    
                    with ui.row().classes("w-full flex-wrap justify-around gap-8"):
                        for param in ["Red", "Green", "Blue"]:
                            with ui.column().classes("items-center"):
                                ui.label(param).classes("font-semibold text-lg")
                                self.figures[param] = ui.image().classes("border w-[320px] h-[220px] object-contain bg-white")
        
        # --- Первый расчет при запуске ---
        self.calculate()

    # --------------------------------------------------------
    # Расчёт и обновление UI
    # --------------------------------------------------------
    def calculate(self):
        """Обработка введённых данных и обновление интерфейса"""
        
        # 1. Получаем значения
        color_hex = self.color_picker.value or "#000000"
        r, g, b = self._hex_to_rgb(color_hex)
        norm = self.conjunction_select.value

        # 2. Вызываем нечеткую систему
        result = self.logic.determine_color(r, g, b, norm=norm)
        self.current_result = result

        # 3. Обновляем текстовые результаты
        self.result_label.text = f"Определённый цвет: {result.color_name}"
        self.result_degree.text = f"Степень истинности: {result.truth_degree:.4f}"
        
        # Обновляем цветной квадрат
        self.color_swatch.style(f"background-color: {color_hex}")

        # 4. Обновляем таблицу
        row_data = [
            {"color": name, "degree": f"{degree:.4f}"}
            for name, degree in sorted(
                result.all_degrees.items(), key=lambda x: x[1], reverse=True
            )[:5]
        ]
        self.grid.options['rowData'] = row_data
        self.grid.update()

        # 5. Рисуем графики
        self._update_input_graphs(r, g, b)
        self._draw_output_barchart(result)

    # --------------------------------------------------------
    # Построение гистограммы выходных значений
    # --------------------------------------------------------
    def _draw_output_barchart(self, result: ColorResult):
        """Рисует гистограмму степеней истинности для всех цветов"""
        
        data = result.all_degrees
        
        # Сортируем для красоты
        sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
        
        names = list(sorted_data.keys())
        values = list(sorted_data.values())
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Создаем цвета для столбиков (выделяем лучший)
        colors = ['#007bff' if name == result.color_name else '#c0c0c0' for name in names]
        
        bars = ax.bar(names, values, color=colors)
        
        ax.set_title("Результаты вывода (до дефаззификации)", fontsize=14, fontweight='bold')
        ax.set_ylabel("Степень истинности", fontsize=12)
        ax.set_ylim(0, 1.1)
        ax.grid(True, axis='y', linestyle='--', alpha=0.6)
        
        # Добавляем значения над столбиками
        for bar in bars:
            yval = bar.get_height()
            if yval > 0.01: # Показываем только значимые
                ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f'{yval:.3f}', 
                        ha='center', va='bottom', fontsize=9)

        plt.xticks(rotation=45, ha='right')
        
        # Сохраняем в base64
        img_b64 = self._fig_to_base64(fig)
        self.output_figure.source = f"data:image/png;base64,{img_b64}"

    # --------------------------------------------------------
    # Построение треугольных функций входных параметров
    # --------------------------------------------------------
    def _update_input_graphs(self, r: int, g: int, b: int):
        """Перерисовать треугольные функции для R, G, B"""
        
        inputs = {"Red": r, "Green": g, "Blue": b}
        functions = self.logic.get_rgb_functions()
        
        for param_name, value in inputs.items():
            img_b64 = self._plot_membership_fig(param_name, value, functions)
            self.figures[param_name].source = f"data:image/png;base64,{img_b64}"

    def _plot_membership_fig(self, title: str, value: int, functions: List[TriFunc]) -> str:
        """Рисует один график ф-ций принадлежности (Low, Medium, High)"""
        
        fig, ax = plt.subplots(figsize=(4, 2.8))
        
        # Цвета для графиков
        func_colors = {"Low": "blue", "Medium": "green", "High": "red"}
        
        for func in functions:
            x = [func.left_point, func.center_point, func.right_point]
            y = [0, 1, 0]
            ax.plot(x, y, label=func.name, color=func_colors.get(func.name, 'gray'), linewidth=2)
        
        # Вертикальная линия для текущего значения
        ax.axvline(value, color='black', linestyle='--', linewidth=2, label=f'Значение: {value}')
        
        # Получаем степени принадлежности для этого значения
        memberships = self.logic.get_membership_values(value)
        for name, m_val in memberships.items():
            if m_val > 0:
                ax.plot([value], [m_val], 'o', color=func_colors.get(name, 'black'))

        ax.set_title(f"Компонент: {title}", fontsize=11)
        ax.set_xlabel("Значение (0-255)", fontsize=9)
        ax.set_ylabel("μ (Степень)", fontsize=9)
        ax.set_xlim(-5, 260)
        ax.set_ylim(0, 1.1)
        ax.legend(loc="upper right", fontsize=8)
        ax.grid(True, alpha=0.3)
        
        return self._fig_to_base64(fig)

    # --------------------------------------------------------
    # Вспомогательные методы
    # --------------------------------------------------------
    def _hex_to_rgb(self, hex_color: str) -> tuple[int, int, int]:
        """Конвертирует HEX строку в (R, G, B) кортеж"""
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _fig_to_base64(self, fig: plt.Figure) -> str:
        """Конвертирует фигуру Matplotlib в строку base64"""
        buffer = io.BytesIO()
        plt.tight_layout()
        fig.savefig(buffer, format='png', dpi=100)
        buffer.seek(0)
        img_b64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close(fig)
        return img_b64