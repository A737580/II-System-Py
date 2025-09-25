from nicegui import ui

# Компонент Лист бокс

class VisualListBox:
    def __init__(self):
        self.items = ["Задача 1", "Задача 2", "Задача 3"]
        
        with ui.column().classes("p-6 gap-4 w-full max-w-2xl"):
            ui.label("Визуальный ListBox").classes("text-2xl font-bold")
            
            # Добавление новых элементов
            with ui.row().classes("w-full gap-2 items-center"):
                self.new_item_input = ui.input(placeholder="Новый элемент").classes("flex-grow")
                ui.button("+", on_click=self.add_item, color="green")
            
            # Список элементов в виде карточек
            self.items_container = ui.column().classes("w-full gap-2")
            self.refresh_list()
    
    def add_item(self):
        new_item = self.new_item_input.value.strip()
        if new_item:
            self.items.append(new_item)
            self.new_item_input.value = ""
            self.refresh_list()
    
    def delete_item(self, item):
        self.items.remove(item)
        self.refresh_list()
    
    def refresh_list(self):
        self.items_container.clear()
        with self.items_container:
            if not self.items:
                ui.label("Список пуст").classes("text-gray-500 italic")
            else:
                for item in self.items:
                    with ui.card().classes("w-full p-3"):
                        with ui.row().classes("w-full justify-between items-center"):
                            ui.label(item).classes("text-lg")
                            ui.button("×", on_click=lambda _, it=item: self.delete_item(it), 
                                     color="red", size="sm").classes("px-3")

VisualListBox()
ui.run()