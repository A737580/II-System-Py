from nicegui import ui

class App:
    def __init__(self):
        self.name = 'Аноним'
        self.show_ui()

    @ui.refreshable_method
    def show_ui(self):
        # Этот метод будет перезапускаться при вызове refresh()
        ui.label(f'Привет, {self.name}!').classes('text-2xl font-bold')

    def update_name(self, new_name):
        self.name = new_name
        self.show_ui.refresh() # Магия! Интерфейс обновляется

app = App()
ui.input('Имя', on_change=lambda e: app.update_name(e.value))

ui.run()