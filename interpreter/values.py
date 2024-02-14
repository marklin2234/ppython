from constants import TT_FLOAT, TT_INT


class Number:
    def __init__(self, value, type_):
        self.type = type_
        self.value = value
        self.set_pos()
    
    def set_pos(self, start=None, end=None):
        self.start = start
        self.end = end
        return self

    def __repr__(self):
        return f'{self.value}'
    
    def __add__(self, other):
        return Number(self.value + other.value, TT_FLOAT if other.type == TT_FLOAT else TT_INT)
    
    def __sub__(self, other):
        return Number(self.value - other.value, TT_FLOAT if other.type == TT_FLOAT else TT_INT)
    
    def __mul__(self, other):
        return Number(self.value * other.value, TT_FLOAT if other.type == TT_FLOAT else TT_INT)
    
    def __truediv__(self, other):
        return Number(self.value / other.value, TT_FLOAT)
    
    def __lt__(self, other):
        return Boolean(self.value < other.value)
    
    def __gt__(self, other):
        return Boolean(self.value > other.value)
    
    def __le__(self, other):
        return Boolean(self.value <= other.value)
    
    def __ge__(self, other):
        return Boolean(self.value >= other.value)
    
    def __eq__(self, other):
        return Boolean(self.value == other.value)
    
class String:
    def __init__(self, value):
        self.value = value
        self.set_pos()

    def set_pos(self, start=None, end=None):
        self.start = start
        self.end = end
        return self
    
    def __add__(self, other):
        return String(self.value + str(other.value))
    
    def __sub__(self, other):
        return String(self.value - str(other.value))
    
    def __repr__(self):
        return f'{self.value}'
    
    def __lt__(self, other):
        return Boolean(self.value < other.value)
    
    def __gt__(self, other):
        return Boolean(self.value > other.value)
    
    def __le__(self, other):
        return Boolean(self.value <= other.value)
    
    def __ge__(self, other):
        return Boolean(self.value >= other.value)
    
    def __eq__(self, other):
        return Boolean(self.value == other.value)

class Boolean:
    def __init__(self, value):
        self.value = value
        self.set_pos()

    def set_pos(self, start=None, end=None):
        self.start = start
        self.end = end
        return self
    
    def __repr__(self):
        return f'{self.value}'