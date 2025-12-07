from nicegui import ui
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from models.exercise5.data import Sample
from services.exercise5.SugenoApproximationService1D import (
    SugenoApproximationService1D, 
    AVAILABLE_FUNCTIONS
)



class Page5:
    def __init__(self):
        self.service = None
        self.current_function = None
        self.train_samples = []
        
        # Параметры по умолчанию
        self.rules_count = 5
        self.mf_type = "triangular"
        self.function_name = list(AVAILABLE_FUNCTIONS.keys())[0]
        self.train_points_count = 50
        self.x_min = 0.0
        self.x_max = 6.28
        self.sigma_factor = 0.6
        self.show_train_points = True
        
        self._build_ui()
        self._update_function()
        self._draw_initial_plots()
    
    def _build_ui(self):
        """Строит пользовательский интерфейс"""
        with ui.row().classes("w-full justify-center"):
            with ui.column().classes("border-2 border-blue-200 w-[1200px] mx-auto h-full px-6 pb-6 gap-6 bg-gray-50"):
                
                ui.label("Аппроксимация функций методом Сугено 1-го порядка").classes(
                    "text-2xl font-bold text-center mt-4"
                )
                
                # ======= Параметры =======
                with ui.row().classes("w-full gap-8 items-start"):
                    
                    # Левая колонка - выбор функции
                    with ui.column().classes("gap-4 w-1/3 bg-white p-4 rounded shadow"):
                        ui.label("Функция и диапазон").classes("text-lg font-bold")
                        
                        self.function_select = ui.select(
                            label="Тестовая функция",
                            options=list(AVAILABLE_FUNCTIONS.keys()),
                            value=self.function_name,
                            on_change=self._update_function
                        ).classes("w-full")
                        
                        with ui.row().classes("w-full gap-2"):
                            self.x_min_input = ui.number(
                                label="X мин",
                                value=self.x_min,
                                step=0.1,
                                format="%.2f",
                                on_change=self._on_range_change
                            ).classes("w-1/2")
                            
                            self.x_max_input = ui.number(
                                label="X макс",
                                value=self.x_max,
                                step=0.1,
                                format="%.2f",
                                on_change=self._on_range_change
                            ).classes("w-1/2")
                        
                        ui.button(
                            "Установить диапазон функции по умолчанию",
                            on_click=self._reset_range
                        ).classes("w-full text-sm")
                    
                    # Средняя колонка - параметры модели
                    with ui.column().classes("gap-4 w-1/3 bg-white p-4 rounded shadow"):
                        ui.label("Параметры модели").classes("text-lg font-bold")
                        
                        self.mf_select = ui.select(
                            label="Функция принадлежности",
                            options={
                                "triangular": "Треугольная",
                                "gaussian": "Гауссова"
                            },
                            value=self.mf_type,
                            on_change=self._on_mf_change
                        ).classes("w-full")
                        
                        self.rules_input = ui.number(
                            label="Количество правил",
                            value=self.rules_count,
                            min=3,
                            max=15,
                            step=1,
                            on_change=lambda e: setattr(self, 'rules_count', int(e.value))
                        ).classes("w-full")
                        
                        self.points_input = ui.number(
                            label="Точек для обучения",
                            value=self.train_points_count,
                            min=20,
                            max=200,
                            step=10,
                            on_change=lambda e: setattr(self, 'train_points_count', int(e.value))
                        ).classes("w-full")
                        
                        # Параметр sigma только для гауссовых функций
                        self.sigma_container = ui.column().classes("w-full")
                        with self.sigma_container:
                            self.sigma_input = ui.slider(
                                min=0.3,
                                max=1.5,
                                step=0.1,
                                value=self.sigma_factor,
                                on_change=lambda e: setattr(self, 'sigma_factor', e.value)
                            ).props('label-always').classes("w-full")
                            ui.label("Перекрытие гауссовых ФП (σ-фактор)").classes("text-sm text-gray-600")
                        
                        self.sigma_container.set_visibility(False)
                    
                    # Правая колонка - визуализация и действия
                    with ui.column().classes("gap-4 w-1/3 bg-white p-4 rounded shadow"):
                        ui.label("Управление").classes("text-lg font-bold")
                        
                        self.show_points_switch = ui.switch(
                            "Показать обучающие точки на графике",
                            value=self.show_train_points,
                            on_change=lambda e: setattr(self, 'show_train_points', e.value)
                        ).classes("w-full")
                        
                        ui.button(
                            "🚀 Обучить модель",
                            on_click=self._train_model
                        ).classes("w-full bg-blue-500 text-white text-lg")
                        
                        ui.separator()
                        
                        self.info_label = ui.label("Модель не обучена").classes(
                            "text-sm whitespace-pre-wrap"
                        )
                
                # ======= График аппроксимации =======
                with ui.column().classes("w-full items-center gap-2 mt-4"):
                    ui.label("Исходная и аппроксимирующая функции").classes(
                        "text-xl font-bold text-center"
                    )
                    self.approx_plot = ui.image().classes(
                        "border w-[1100px] h-[450px] object-contain bg-white rounded shadow"
                    )
                
                # ======= График функций принадлежности =======
                with ui.column().classes("w-full items-center gap-2 mt-4"):
                    ui.label("Функции принадлежности и обучающие точки").classes(
                        "text-xl font-bold text-center"
                    )
                    self.mf_plot = ui.image().classes(
                        "border w-[1100px] h-[450px] object-contain bg-white rounded shadow"
                    )
    
    def _on_mf_change(self, e):
        """Обработка изменения типа функции принадлежности"""
        self.mf_type = e.value
        # Показываем/скрываем параметр sigma
        self.sigma_container.set_visibility(self.mf_type == "gaussian")
    
    def _on_range_change(self, e):
        """Обработка изменения диапазона"""
        self.x_min = self.x_min_input.value
        self.x_max = self.x_max_input.value
    
    def _reset_range(self):
        """Сбрасывает диапазон к значениям по умолчанию для выбранной функции"""
        if self.current_function:
            self.x_min = self.current_function.x_min
            self.x_max = self.current_function.x_max
            self.x_min_input.set_value(self.x_min)
            self.x_max_input.set_value(self.x_max)
    
    def _update_function(self, value=None, e=None):
        """
        value: иногда nicegui передаёт новое значение первым аргументом
        e:     или передаёт event-объект с атрибутом .value
        если ничего не пришло — читаем self.function_select.value
        """
        new_value = None

        # 1) если nicegui передал значение как первый аргумент
        if value is not None:
            new_value = value
        # 2) либо event-объект с .value
        elif e is not None and hasattr(e, "value"):
            new_value = e.value
        # 3) fallback — читаем из самого компонента
        else:
            new_value = self.function_select.value

        # теперь безопасно используем новое значение
        if new_value is None:
            return  # ничего не меняем

        self.function_name = new_value
        self.current_function = AVAILABLE_FUNCTIONS[self.function_name]
        self._reset_range()
        self._draw_initial_plots()
    
    def _draw_initial_plots(self):
        """Рисует начальные графики до обучения"""
        if not self.current_function:
            return
        
        # График функции
        fig, ax = plt.subplots(figsize=(11, 4.5), dpi=100)
        x_plot = np.linspace(self.x_min, self.x_max, 300)
        y_plot = [self.current_function(x) for x in x_plot]
        ax.plot(x_plot, y_plot, 'b-', linewidth=2, label='Исходная функция')
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('y', fontsize=12)
        ax.set_title(f'Функция: {self.function_name}', fontsize=14)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        self._set_image_from_figure(fig, self.approx_plot)
        plt.close(fig)
        
        # Пустой график ФП
        fig, ax = plt.subplots(figsize=(11, 4.5), dpi=100)
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('Степень принадлежности', fontsize=12)
        ax.set_title('Функции принадлежности (модель не обучена)', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(self.x_min, self.x_max)
        ax.set_ylim(-0.05, 1.1)
        self._set_image_from_figure(fig, self.mf_plot)
        plt.close(fig)
    
    def _train_model(self):
        """Обучает модель Сугено"""
        try:
            if self.x_min >= self.x_max:
                ui.notify("Ошибка: X мин должен быть меньше X макс", type='negative')
                return
            
            # Генерация обучающих данных
            x_train = np.linspace(self.x_min, self.x_max, self.train_points_count)
            self.train_samples = [
                Sample(x, self.current_function(x)) 
                for x in x_train
            ]
            
            # Создание и обучение модели
            self.service = SugenoApproximationService1D(
                x_min=self.x_min,
                x_max=self.x_max,
                rules_count=self.rules_count,
                mf_type=self.mf_type,
                sigma_factor=self.sigma_factor,
                min_points_per_rule=max(2, self.train_points_count // (self.rules_count * 3))
            )
            
            self.service.train(self.train_samples)
            
            # Вычисление метрик
            metrics = self.service.calculate_error_metrics(self.train_samples)
            
            # Обновление информации
            mf_name = 'Треугольная' if self.mf_type == 'triangular' else f'Гауссова (σ={self.sigma_factor:.1f})'
            info_text = f"""✅ Модель обучена!

Параметры:
  • Функция: {self.function_name}
  • Диапазон: [{self.x_min:.2f}, {self.x_max:.2f}]
  • ФП: {mf_name}
  • Правил: {self.rules_count}
  • Точек: {self.train_points_count}

Метрики:
  • MAE: {metrics['mae']:.6f}
  • RMSE: {metrics['rmse']:.6f}
  • MAX: {metrics['max_error']:.6f}
"""
            self.info_label.set_text(info_text)
            
            # Обновление графиков
            self._draw_approximation_plot()
            self._draw_membership_plot()
            
            ui.notify("Модель успешно обучена!", type='positive')
            
        except Exception as e:
            ui.notify(f"Ошибка: {str(e)}", type='negative')
            self.info_label.set_text(f"❌ Ошибка:\n{str(e)}")
    
    def _draw_approximation_plot(self):
        """Рисует график исходной и аппроксимирующей функций"""
        if not self.service or not self.current_function:
            return
        
        fig, ax = plt.subplots(figsize=(11, 4.5), dpi=100)
        
        x_plot = np.linspace(self.x_min, self.x_max, 300)
        y_true = [self.current_function(x) for x in x_plot]
        y_pred = self.service.predict_multiple(x_plot)
        
        ax.plot(x_plot, y_true, 'b-', linewidth=2.5, label='Исходная функция', alpha=0.8)
        ax.plot(x_plot, y_pred, 'r--', linewidth=2, label='Аппроксимация Сугено', alpha=0.9)
        
        # Опционально показываем обучающие точки
        if self.show_train_points:
            x_train = [s.x for s in self.train_samples]
            y_train = [s.y for s in self.train_samples]
            ax.scatter(x_train, y_train, c='green', s=20, marker='o', 
                      label='Обучающие точки', zorder=5, alpha=0.5)
        
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('y', fontsize=12)
        ax.set_title(f'Аппроксимация функции {self.function_name}', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11, loc='best')
        ax.grid(True, alpha=0.3)
        
        self._set_image_from_figure(fig, self.approx_plot)
        plt.close(fig)
    
    def _draw_membership_plot(self):
        """Рисует график функций принадлежности и обучающих точек"""
        if not self.service or not self.train_samples:
            return
        
        fig, ax = plt.subplots(figsize=(11, 4.5), dpi=100)
        
        x_plot = np.linspace(self.x_min, self.x_max, 500)
        
        # Рисуем функции принадлежности
        colors = plt.cm.tab10(np.arange(len(self.service.rules)))
        for i, rule in enumerate(self.service.rules):
            y_mf = [rule.mf.degree(x) for x in x_plot]
            ax.plot(x_plot, y_mf, color=colors[i], linewidth=2.5, 
                   label=f'Правило {i+1}', alpha=0.8)
        
        # Рисуем обучающие точки на оси X
        x_train = [s.x for s in self.train_samples]
        y_train = [0] * len(x_train)
        ax.scatter(x_train, y_train, c='black', s=40, marker='|', 
                  label='Обучающие точки', zorder=5, alpha=0.7, linewidths=2)
        
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('Степень принадлежности', fontsize=12)
        mf_name = 'треугольные' if self.mf_type == 'triangular' else 'гауссовы'
        ax.set_title(f'Функции принадлежности ({mf_name})', fontsize=14, fontweight='bold')
        ax.set_ylim(-0.05, 1.1)
        ax.legend(fontsize=10, ncol=min(3, len(self.service.rules)), loc='upper right')
        ax.grid(True, alpha=0.3)
        
        self._set_image_from_figure(fig, self.mf_plot)
        plt.close(fig)
    
    def _set_image_from_figure(self, fig, image_widget):
        """Конвертирует matplotlib фигуру в base64 и устанавливает в виджет"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()
        image_widget.set_source(f'data:image/png;base64,{img_base64}')

