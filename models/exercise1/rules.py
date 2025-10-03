from typing import Dict, Set, List, Optional


class Rules:
    """Класс для хранения и управления правилами логического вывода.
    
    Правила хранятся в формате: {следствие: {множество антецедентов}}
    
    Attributes:
        _rules (Dict[str, Set[str]]): Словарь правил, где ключ - следствие,
                                     значение - множество антецедентов
    """
    
    def __init__(self):
        self._rules: Dict[str, Set[str]] = {}
    
    def clear(self):
        self._rules.clear()
    
    def delete_by_fact(self, fact: str, anticedents:str) -> bool:
        if not fact in self._rules.keys():
            return False
        
        if not anticedents in self._rules[fact]:
            return False

        self._rules[fact].remove(anticedents)
        return True
    
    def add(self, consequent:str, anticedents: str) -> bool:
        if not consequent in self._rules.keys():
            self._rules[consequent] = set() 
        
        if not anticedents in self._rules[consequent]:
            self._rules[consequent].add(anticedents)
            return True
        return False
    
    def add_from_list(self, rules_list: List[str]) -> 'Rules':
        """Заполняет правила из списка строк формата 'A&B&C-->F'.
        
        Args:
            rules_list (List[str]): Список правил
            
        Returns:
            Rules: Текущий объект для цепочки вызовов
        """
        for rule_str in rules_list:
            if "-->" in rule_str:
                parts = rule_str.split("-->")
                if len(parts) == 2:
                    antecedents, consequent = parts
                    antecedents_clean = antecedents.replace("&", "")
                    self.add(consequent.strip(), antecedents_clean.strip())
        return self  
    
    def get_all_by_fact(self, fact: str) -> Optional[List[str]]:
        if fact not in self._rules or not self._rules[fact]:
            return None
        
        return list(self._rules[fact].copy())
    
    def get_keys(self) -> List[str]:
        return list(self._rules.keys())
    
    def get_copy(self) -> 'Rules':
        copy = Rules()
        for key in self._rules.keys():
            for value in self._rules[key]:
                copy.add(key, value)
        return copy

    def get_all(self) -> Dict[str, Set[str]]:
        copy = {}
        for key in self._rules.keys():
            for value in self._rules[key]:
                if key not in copy:
                    copy[key] = set()
                copy[key].add(value)
        return copy