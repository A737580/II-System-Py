from nicegui import ui
from typing import List, Callable, Optional


class ListBox:
    """Переиспользуемый аналог ListBox из WinForms для NiceGUI"""
    
    def __init__(self, items: List[str] = None, height: str = "200px", on_selection_change: Optional[Callable] = None):
        self.items = items or []
        self.selected_index = -1
        self.selected_item = None
        self.on_selection_change = on_selection_change
        
        with ui.card().style(f'width: 100%; height: {height}; padding: 0; overflow-y: auto; border: 1px solid #999; background-color: white;'):
            self.container = ui.column().style('width: 100%; gap: 0;')
        
        self._update_display()
    
    def add_item(self, item: str) -> None:
        """Добавить элемент в конец списка"""
        self.items.append(item)
        self._update_display()
    
    def remove_item(self, item: str) -> bool:
        """Удалить элемент по значению"""
        try:
            index = self.items.index(item)
            self.items.pop(index)
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
        """Удалить элемент по индексу"""
        if 0 <= index < len(self.items):
            self.items.pop(index)
            if self.selected_index == index:
                self.selected_index = -1
                self.selected_item = None
            elif self.selected_index > index:
                self.selected_index -= 1
            self._update_display()
            return True
        return False
    
    def remove_selected(self) -> bool:
        """Удалить выбранный элемент"""
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
        """Выбрать элемент по индексу"""
        if 0 <= index < len(self.items):
            self.selected_index = index
            self.selected_item = self.items[index]
            self._update_display()
            if self.on_selection_change:
                self.on_selection_change(self.selected_item, self.selected_index)
            return True
        return False
    
    def _on_item_click(self, index: int):
        self.select_item(index)
    
    def _update_display(self):
        """Обновить отображение списка"""
        self.container.clear()
        
        for i, item in enumerate(self.items):
            is_selected = i == self.selected_index
            
            style = (
                'width: 100%; padding: 8px 12px; margin: 0; cursor: pointer; '
                'border: 1px solid #ccc; text-align: left; '
                f'background-color: {"#0078d4" if is_selected else "#f0f0f0"}; '
                f'color: {"white" if is_selected else "black"};'
                'text-transform: none;'
            )
            
            with self.container:
                ui.button(item, on_click=lambda idx=i: self._on_item_click(idx)).style(style)
