from error import InvalidSyntaxError
import tokenizer
from constants import *

#############################################
# NODES
#############################################

class ExprNode:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f'({self.left}, {self.op}, {self.right})'

class NumNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'
    
class UnaryOpNode:
    def __init__(self, op, node):
        self.op = op
        self.node = node
    
    def __repr__(self):
        return f'({self.op}, {self.node})'


#############################################
# PARSE RESULT
#############################################
    
class ParseResult:
    def __init__(self):
        self.err = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.err:
                self.err = res.err
            return res.node
        
        return res

    def success(self, node):
        self.node = node
        return self
    
    def failure(self, err):
        self.err = err
        return self
    
    def __repr__(self):
        return repr(self.node)

#############################################
# PARSER
#############################################
    
class Parser:
    def __init__(self, tokens):
        self.idx = -1
        self.tokens = tokens
        self.step()

    def step(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.curr_tok = self.tokens[self.idx]

    def parse(self):
        res = self.expr()
        if not res.err and self.curr_tok.type != TT_EOF:
            return ParseResult().failure(InvalidSyntaxError(self.curr_tok.start, self.curr_tok.end, "Expected EOF."))
        return res

    def factor(self):
        res = ParseResult()
        curr = self.curr_tok
        if curr.type in [TT_ADD, TT_SUB]:
            if self.idx == 0 or curr.type == TT_SUB:
                self.step()
                factor = res.register(self.factor())
                if res.err:
                    return res
                return res.success(UnaryOpNode(curr, factor))
        elif curr.type in [TT_INT, TT_FLOAT]:
            self.step()
            return res.success(NumNode(curr))
        elif curr.type == TT_LPAR:
            self.step()
            expr = res.register(self.expr())
            if res.err:
                return res
            if self.curr_tok.type == TT_RPAR:
                self.step()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.curr_tok.start, self.curr_tok.end, "Expected ')'."))
        return res.failure(InvalidSyntaxError(curr.start, curr.end, "Expected int or float."))

    def term(self):
        return self.bin_op(self.factor, [TT_MULT, TT_DIV])
    
    def expr(self):
        return self.bin_op(self.term, [TT_ADD, TT_SUB])
    
    def bin_op(self, func, terms):
        res = ParseResult()
        left = res.register(func())
        if res.err:
            return res
        while self.curr_tok.type in terms:
            curr = self.curr_tok
            self.step()
            right = res.register(func())
            if res.err:
                return res
            left = ExprNode(curr, left, right)
        return res.success(left)

#############################################
# RUN
#############################################

def run(fn, text):
    tokens, error = tokenizer.run(fn, text)
    # print(tokens)

    if error:
        return None, error
    else:
        parser = Parser(tokens)
        ast = parser.parse()
        # if (ast.err):
        #     print(ast.err)
        # else:
        #     print(ast.node)

        return ast.node, ast.err