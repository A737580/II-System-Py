from nicegui import ui

class Navbar:
    def __init__(self):
        with ui.row().classes("w-full justify-between bg-gray-200 p-2"):
            ui.label("Системы искусственного интеллекта. 20490 Максим Алексеевич Вохминцев").classes("text-lg font-bold")
            with ui.row():
                ui.link("Главная", "/")
                ui.link("Задание 1", "/page1")
                ui.link("Задание 2", "/page2")
