from nicegui import ui

ui.label('Это метка (Label)')

# Кнопка с обработчиком события
button = ui.button('Нажми меня!')
def handle_click():
    ui.notify('Кнопка была нажата!') # Всплывающее уведомление
button.on('click', handle_click)

# Поле ввода текста
input_field = ui.input(placeholder='Введите текст здесь')
input_field.on('input', lambda e: ui.notify(f'Вы вводите: {e.value}'))

# Чекбокс
checkbox = ui.checkbox('Согласен с условиями')
checkbox.on('change', lambda e: ui.notify(f'Чекбокс теперь: {e.value}'))

# Выпадающий список
select = ui.select(['Вариант 1', 'Вариант 2', 'Вариант 3'])
select.on('change', lambda e: ui.notify(f'Выбран: {e.value}'))

ui.run()