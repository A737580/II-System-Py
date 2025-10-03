from typing import Set, List

class Facts:
    """Класс для хранения и управления фактами (символами).
    
    Attributes:
        _facts (Set[str]): Множество фактов, где каждый факт - одиночный символ
    """

    def __init__(self):
        self._facts: Set[str] = set()
    
    def clear(self):
        self._facts.clear()
    
    def delete(self, fact:str) -> bool: 
        if fact in self._facts:
            self._facts.remove(fact)
            return True
        return False
    
    def add(self, fact:str)->bool:
        if len(fact) != 1:
            return False
        
        if fact not in self._facts:
            self._facts.add(fact)
            return True
        return False

    def add_from_list(self, facts_list: List[str]) -> 'Facts':
        """Заполняет факты из списка строк и возвращает self.
        
        Args:
            facts_list (List[str]): Список фактов
            
        Returns:
            Facts: Текущий объект для цепочки вызовов
        """
        for fact in facts_list:
            if len(fact) == 1:  # Проверяем что это одиночный символ
                self._facts.add(fact)
        return self  

    def find(self, fact:str)->bool:
        return fact in self._facts
    
    def get_all(self) -> Set[str]:
        return self._facts.copy() # строки- неизменяемый тип