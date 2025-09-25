from nicegui import ui

# Создаем реактивные переменные
text = ui.label('Изначальный текст') # Метка, которую будем менять
name = 'Аноним' # Переменная, которую будем привязывать

# Функция для обновления текста
def update_text():
    text.text = f'Привет, {name}!'

# Поле ввода, привязанное к переменной `name`
ui.input('Ваше имя', on_change=lambda e: (
    setattr(ui, 'name', e.value),  # Динамически обновляем переменную (простой способ)
    update_text() # Вызываем обновление метки
))

# Альтернативный, БОЛЕЕ КРАСИВЫЙ способ с использованием классов
class App:
    def __init__(self):
        self.name = 'Аноним'
        self.label = ui.label(f'Привет, {self.name}!')
        ui.input('Ваше имя', on_change=self.update_name)

    def update_name(self, event):
        self.name = event.value
        self.label.text = f'Привет, {self.name}!'

App()

ui.run()