from nicegui import ui


# Плохо работает выбор элементов


class AdvancedListBox:
    def __init__(self):
        self.items = [f"Задача {i}" for i in range(1, 16)]
        self.selected_index = None
        
        with ui.column().classes("p-6 gap-4 w-96"):
            ui.label("Advanced ListBox").classes("text-xl font-bold")
            
            # ListBox контейнер
            ui.label("Список элементов (кликните для выбора, двойной клик для удаления):")
            with ui.column().classes("border-2 border-gray-400 rounded h-64 overflow-y-auto w-full bg-white"):
                self.list_items_container = ui.column().classes("w-full")
                self.refresh_list()
            
            # Статусная строка как в WinForms
            with ui.row().classes("w-full justify-between items-center p-2 bg-gray-100 border-t"):
                self.status_label = ui.label(f"Элементов: {len(self.items)}")
                self.selected_label = ui.label("Выбрано: нет")
            
            # Панель инструментов
            with ui.row().classes("w-full gap-2 justify-center"):
                with ui.column().classes("gap-2"):
                    with ui.row().classes("gap-2"):
                        self.new_item_input = ui.input(placeholder="Новый элемент").classes("w-48")
                        ui.button("Добавить", on_click=self.add_item, color="green")
                    
                    with ui.row().classes("gap-2"):
                        ui.button("Удалить выбранный", on_click=self.delete_selected, color="red")
                        ui.button("Очистить все", on_click=self.clear_all, color="orange")
                        ui.button("Обновить", on_click=self.refresh_list)
    
    def refresh_list(self):
        self.list_items_container.clear()
        with self.list_items_container:
            if not self.items:
                ui.label("Список пуст").classes("w-full p-4 text-center text-gray-500 italic")
            else:
                for i, item in enumerate(self.items):
                    # Определяем стиль для выбранного элемента
                    bg_color = "bg-blue-500 text-white" if i == self.selected_index else "bg-white hover:bg-gray-50"
                    
                    # Создаем элемент списка
                    with ui.row().classes(f"w-full p-3 border-b border-gray-200 cursor-pointer select-none {bg_color}"):
                        ui.label(f"{i+1}. {item}").classes("flex-grow")
                        
                        # Обработчики событий
                        row_element = ui.element('div').classes("absolute inset-0") \
                            .on('click', lambda e, idx=i: self.select_item(idx)) \
                            .on('dblclick', lambda e, idx=i: self.delete_item(idx))
    
    def select_item(self, index):
        self.selected_index = index
        self.refresh_list()
        self.selected_label.text = f"Выбрано: {self.items[index]}"
    
    def delete_item(self, index):
        deleted_item = self.items.pop(index)
        if self.selected_index == index:
            self.selected_index = None
            self.selected_label.text = "Выбрано: нет"
        elif self.selected_index > index:
            self.selected_index -= 1
        
        self.refresh_list()
        ui.notify(f"Удален: {deleted_item}")
    
    def add_item(self):
        new_item = self.new_item_input.value.strip()
        if new_item:
            self.items.append(new_item)
            self.new_item_input.value = ""
            self.refresh_list()
            self.status_label.text = f"Элементов: {len(self.items)}"
            ui.notify(f"Добавлен: {new_item}")
    
    def delete_selected(self):
        if self.selected_index is not None:
            self.delete_item(self.selected_index)
        else:
            ui.notify("Сначала выберите элемент!")
    
    def clear_all(self):
        self.items.clear()
        self.selected_index = None
        self.refresh_list()
        self.status_label.text = "Элементов: 0"
        self.selected_label.text = "Выбрано: нет"
        ui.notify("Список очищен")

AdvancedListBox()
ui.run()