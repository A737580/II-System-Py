# pep8



# 1. Имена классов (Class Names)
# python

# Правильно - CamelCase
class MyClass:
    pass

class DatabaseConnection:
    pass

class HTTPRequestHandler:
    pass

# Неправильно
class my_class:  # должно быть MyClass
    pass

class databaseConnection:  # должно быть DatabaseConnection
    pass

# 2. Имена методов и функций
# python

class MyClass:
    # Правильно - snake_case для методов
    def calculate_total(self):
        pass
    
    def get_user_data(self):
        pass
    
    def is_valid(self):
        pass  # для булевых методов лучше использовать is_*, has_*
    
    # Неправильно
    def CalculateTotal(self):  # должно быть calculate_total
        pass
    
    def GetUserData(self):  # должно быть get_user_data
        pass

# 3. Имена атрибутов и свойств
# python

class BankAccount:
    def __init__(self):
        # Правильно - snake_case для атрибутов
        self.account_balance = 0
        self.account_holder = ""
        self.is_active = True
        
        # Константы в классе - UPPER_CASE
        self.MAX_BALANCE = 1000000
        
        # Неправильно
        self.accountBalance = 0  # должно быть account_balance
        self.AccountHolder = ""  # должно быть account_holder

# 4. Приватные методы и атрибуты
# python

class MyClass:
    def __init__(self):
        # Одно подчеркивание - "защищенный" (protected)
        self._internal_data = []
        
        # Два подчеркивания - приватный (private, name mangling)
        self.__very_private_data = None
    
    def public_method(self):
        """Публичный метод - вызывается извне"""
        pass
    
    def _protected_method(self):
        """Защищенный метод - для внутреннего использования"""
        pass
    
    def __private_method(self):
        """Приватный метод - не должен вызываться извне"""
        pass

# 5. Свойства (properties)
# python

class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age
    
    # Property - используем snake_case
    @property
    def full_name(self):
        return self._name
    
    @full_name.setter
    def full_name(self, value):
        self._name = value
    
    @property
    def is_adult(self):
        return self._age >= 18
