from nicegui import ui
from typing import List, Callable, Optional


class ListBox:
    """
    Аналог ListBox из WinForms для NiceGUI
    Поддерживает добавление, удаление элементов, выбор и скролл
    """
    
    def __init__(self, 
                 items: List[str] = None, 
                 height: str = "200px",
                 on_selection_change: Optional[Callable] = None):
        """
        Инициализация ListBox
        
        Args:
            items: начальный список элементов
            height: высота компонента
            on_selection_change: callback при изменении выбора
        """
        self.items = items or []
        self.selected_index = -1
        self.selected_item = None
        self.on_selection_change = on_selection_change
        
        # Создаем контейнер с прокруткой
        with ui.card().style(f'width: 100%; height: {height}; padding: 0; overflow-y: auto; border: 1px solid #ccc;'):
            self.container = ui.column().style('width: 100%; gap: 0;')
        
        self._update_display()
    
    def add_item(self, item: str) -> None:
        """Добавить элемент в конец списка"""
        self.items.append(item)
        self._update_display()
    
    def remove_item(self, item: str) -> bool:
        """
        Удалить элемент по значению
        Returns: True если элемент был найден и удален
        """
        try:
            index = self.items.index(item)
            self.items.pop(index)
            
            # Обновляем выбранный элемент
            if self.selected_index == index:
                self.selected_index = -1
                self.selected_item = None
            elif self.selected_index > index:
                self.selected_index -= 1
            
            self._update_display()
            return True
        except ValueError:
            return False
    
    def remove_at(self, index: int) -> bool:
        """
        Удалить элемент по индексу
        Returns: True если элемент был удален
        """
        if 0 <= index < len(self.items):
            self.items.pop(index)
            
            # Обновляем выбранный элемент
            if self.selected_index == index:
                self.selected_index = -1
                self.selected_item = None
            elif self.selected_index > index:
                self.selected_index -= 1
            
            self._update_display()
            return True
        return False
    
    def remove_selected(self) -> bool:
        """
        Удалить выбранный элемент
        Returns: True если элемент был удален
        """
        if self.selected_index >= 0:
            return self.remove_at(self.selected_index)
        return False
    
    def clear(self) -> None:
        """Очистить весь список"""
        self.items.clear()
        self.selected_index = -1
        self.selected_item = None
        self._update_display()
    
    def get_items(self) -> List[str]:
        """Получить все элементы списка"""
        return self.items.copy()
    
    def get_selected_item(self) -> Optional[str]:
        """Получить выбранный элемент"""
        return self.selected_item
    
    def get_selected_index(self) -> int:
        """Получить индекс выбранного элемента (-1 если ничего не выбрано)"""
        return self.selected_index
    
    def select_item(self, index: int) -> bool:
        """
        Выбрать элемент по индексу
        Returns: True если элемент был выбран
        """
        if 0 <= index < len(self.items):
            self.selected_index = index
            self.selected_item = self.items[index]
            self._update_display()
            if self.on_selection_change:
                self.on_selection_change(self.selected_item, self.selected_index)
            return True
        return False
    
    def _on_item_click(self, index: int):
        """Обработчик клика по элементу"""
        self.select_item(index)
    
    def _update_display(self):
        """Обновить отображение списка"""
        self.container.clear()
        
        for i, item in enumerate(self.items):
            is_selected = i == self.selected_index
            
            # Стиль для элемента
            style = (
                'width: 100%; padding: 8px 12px; margin: 0; cursor: pointer; '
                'border: none; text-align: left; '
                f'background-color: {"#0078d4" if is_selected else "transparent"}; '
                f'color: {"white" if is_selected else "black"};'
            )
            
            hover_style = (
                'background-color: #f0f0f0 !important; '
                f'color: {"white" if is_selected else "black"} !important;'
            ) if not is_selected else ''
            
            with self.container:
                ui.button(
                    item,
                    on_click=lambda idx=i: self._on_item_click(idx)
                ).style(style).on('mouseenter', 
                    lambda e, hs=hover_style: e.sender.style.update(hs) if hs else None
                ).on('mouseleave', 
                    lambda e, s=style: e.sender.style.update(s)
                )


# Пример использования
if __name__ in {"__main__", "__mp_main__"}:
    def on_selection_changed(item, index):
        ui.notify(f'Выбран: {item} (индекс: {index})')
    
    # Создаем ListBox
    listbox = ListBox(
        items=['Элемент 1', 'Элемент 2', 'Элемент 3'],
        height='100px',
        on_selection_change=on_selection_changed
    )
    
    # Элементы управления
    with ui.row():
        new_item_input = ui.input('Новый элемент', placeholder='Введите текст')
        ui.button('Добавить', on_click=lambda: (
            listbox.add_item(new_item_input.value) if new_item_input.value else None,
            new_item_input.set_value('')
        ))
    
    with ui.row():
        ui.button('Удалить выбранный', on_click=lambda: (
            listbox.remove_selected(),
            ui.notify('Элемент удален' if listbox.get_selected_item() else 'Нет выбранного элемента')
        ))
        
        ui.button('Очистить все', on_click=lambda: (
            listbox.clear(),
            ui.notify('Список очищен')
        ))
    
    with ui.row():
        ui.button('Показать элементы', on_click=lambda: 
            ui.notify(f'Элементы: {listbox.get_items()}')
        )
        
        ui.button('Показать выбранный', on_click=lambda: 
            ui.notify(f'Выбран: {listbox.get_selected_item() or "Ничего"}')
        )
    
    ui.run()