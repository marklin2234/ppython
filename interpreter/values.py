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
        print(other, type(other))
        return Number(self.value + other.value, TT_FLOAT if other.type == TT_FLOAT else TT_INT)
    
    def __sub__(self, other):
        return Number(self.value - other.value, TT_FLOAT if other.type == TT_FLOAT else TT_INT)
    
    def __mul__(self, other):
        return Number(self.value * other.value, TT_FLOAT if other.type == TT_FLOAT else TT_INT)
    
    def __truediv__(self, other):
        return Number(self.value / other.value, TT_FLOAT)