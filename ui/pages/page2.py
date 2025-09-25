from nicegui import ui

class Page2:
    def __init__(self):
        with ui.element('div').classes('relative w-full h-screen bg-gray-50'):
            ui.button("Кнопка в (200,100)", on_click=self.say_hello) \
              .classes('absolute top-[100px] left-[200px]')

            ui.label("Текст снизу по центру") \
              .classes('absolute bottom-[400px] left-1/2 -translate-x-1/2 text-xl')

    def say_hello(self):
        ui.notify("Привет с Page 2 👋")
