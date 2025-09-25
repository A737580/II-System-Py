from nicegui import ui
from services.calc_service import CalcService
from models.calc_model import CalcModel

class HomePage:
    def __init__(self):
        self.service = CalcService(CalcModel())

        with ui.column().classes(" flex flex-col"):
            
            # Основной контент - 75% высоты
            with ui.column().classes("h-[75vh] items-center justify-center p-4  border-2 border-blue-200"):
                ui.label("Главная страница").classes("text-2xl font-bold")
                ui.label("Пример: модель считает сумму чисел.")

                self.input_field = ui.input("Введите числа через запятую").classes("w-64")
                ui.button("Посчитать", on_click=self.calculate)
                self.result_label = ui.label("").classes("text-lg mt-2")

    def calculate(self):
        text = self.input_field.value.strip()
        try:
            numbers = [float(x) for x in text.split(",") if x]
            result = self.service.calc_sum(numbers)
            self.result_label.text = f"Сумма: {result}"
        except ValueError:
            self.result_label.text = "Ошибка: введите числа через запятую"
