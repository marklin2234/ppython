from constants import *
from error import IllegalCharError

"""
variable declarations
    expression ::= term | expression ( '+' | '-' ) term
    term       ::= factor | term ( '*' | '/' ) factor
    factor     ::= '(' expression ')' | number | variable
    number     ::= [0-9]+
    variable   ::= [a-zA-Z_][a-zA-Z0-9_]*
"""

class Token:
    def __init__(self, type_, value = None, start=None, end=None):
        self.type = type_
        self.value = value
        
        if start != None:
            self.start = start.copy()
            self.end = start.copy()
            self.end.step()
        
        if end != None:
            self.end = end
    
    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        else:
            return self.type
        
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def step(self, curr_char=None):
        self.idx += 1
        self.col += 1
        if curr_char == '\n':
            self.ln += 1
            self.col = 0

        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
    
#############################################
# LEXER
#############################################
    
class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current = None
        self.step()

    def step(self):
        self.pos.step()
        self.current = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def tokenize(self):
        tokens = []

        while self.current != None:
            curr = self.current
            
            if curr in ' \t':
                self.step()
            elif curr == '+':
                tokens.append(Token(TT_ADD, start=self.pos))
                self.step()
            elif curr == '-':
                tokens.append(Token(TT_SUB, start=self.pos))
                self.step()
            elif curr == '*':
                tokens.append(Token(TT_MULT, start=self.pos))
                self.step()
            elif curr == '/':
                tokens.append(Token(TT_DIV, start=self.pos))
                self.step()
            elif curr == '(':
                tokens.append(Token(TT_LPAR, start=self.pos))
                self.step()
            elif curr == ')':
                tokens.append(Token(TT_RPAR, start=self.pos))
                self.step()
            elif curr == '[':
                tokens.append(Token(TT_LSQB, start=self.pos))
                self.step()
            elif curr == ']':
                tokens.append(Token(TT_RSQB, start=self.pos))
                self.step()
            elif curr == '-':
                tokens.append(Token(TT_SUB, start=self.pos))
                self.step()
            elif curr == '\'' or curr == '\"':
                apos_type = self.current
                self.step()
                tokens.append(self.make_string(apos_type))
            elif curr in DIGITS:
                tokens.append(self.make_num())
            else:
                char = self.current
                start = self.pos.copy()
                self.step()
                return [], IllegalCharError(details=f'{char} is not valid.', start=start, end=self.pos)         

        tokens.append(Token(TT_EOF, start=self.pos))
        return tokens, None
    
    def make_num(self):
        num_str = ''
        num_dec = 0
        start = self.pos

        while self.current != None and self.current in DIGITS or self.current == '.':
            if self.current == '.' and num_dec == 1:
                break
            num_str += self.current
            self.step()
        
        if num_dec == 0:
            return Token(TT_INT, int(num_str), start, self.pos)
        elif num_dec == 1:
            return Token(TT_FLOAT, float(num_str), start, self.pos)
        
    def make_string(self, apos_type):
        str = ''
        start = self.pos
        while self.current != None:
            if self.current == apos_type:
                self.step()
                break
            str += self.current
            self.step()

        return Token(TT_STRING, str, start, self.pos)


#############################################
# RUN
#############################################

def run(fn, text):
    lexer = Lexer(fn, text)

    tokens, error = lexer.tokenize()

    return tokens, error

