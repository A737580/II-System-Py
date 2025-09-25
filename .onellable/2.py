from nicegui import ui

# Простой рабочий пример
items = ["Яблоко", "Банан", "Апельсин"]

def delete_selected():
    if select.value and select.value in items:
        items.remove(select.value)
        select.set_options(items)
        select.value = None
        status.text = f"Удален: {select.value}"
    else:
        status.text = "Сначала выберите элемент!"

def add_item():
    new_item = input.value.strip()
    if new_item and new_item not in items:
        items.append(new_item)
        select.set_options(items)
        input.value = ""
        status.text = f"Добавлен: {new_item}"

with ui.column().classes("p-4 gap-3 w-80"):
    ui.label("Простой ListBox").classes("text-lg font-bold")
    
    # Добавление
    with ui.row().classes("w-full gap-2"):
        input = ui.input(placeholder="Новый элемент").classes("flex-grow")
        ui.button("+", on_click=add_item, color="green")
    
    # Список
    select = ui.select(items, label="Элементы").classes("w-full")
    
    # Управление
    ui.button("Удалить выбранный", on_click=delete_selected, color="red").classes("w-full")
    
    # Статус
    status = ui.label("Выберите элемент")

ui.run()