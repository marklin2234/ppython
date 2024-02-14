from error import InvalidSyntaxError
import tokenizer as tokenizer
from constants import *

#############################################
# NODES
#############################################

class ExprNode:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

        self.start = left.start
        self.end = right.end
    
    def __repr__(self):
        return f'({self.left}, {self.op}, {self.right})'

class NumNode:
    def __init__(self, tok):
        self.tok = tok
        self.start = tok.start
        self.end = tok.end

    def __repr__(self):
        return f'{self.tok}'
    
class UnaryOpNode:
    def __init__(self, op, node):
        self.op = op
        self.node = node
        self.start = op.start
        self.end = node.end
    
    def __repr__(self):
        return f'({self.op}, {self.node})'
    
class VarAssignNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.start = name.start
        self.end = value.end

    def __repr__(self):
        return f'({self.name} = {self.value})'
        
class VarVisitNode:
    def __init__(self, name):
        self.name = name
        self.start = name.start
        self.end = name.end

    def __repr__(self):
        return f'{self.name}'
    
class StringNode:
    def __init__(self, tok):
        self.tok = tok
        self.start = tok.start
        self.end = tok.end

    def __repr__(self):
        return f'{self.tok}'

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
        return self.curr_tok

    def parse(self):
        res = self.expr()
        if not res.err and self.curr_tok.type != TT_EOF:
            return ParseResult().failure(InvalidSyntaxError(self.curr_tok.start, self.curr_tok.end, "Expected EOF."))
        return res

    def factor(self):
        res = ParseResult()
        curr = self.curr_tok
        if curr.type == TT_IDEN:
            self.step()
            return res.success(VarVisitNode(curr))
        if curr.type in [TT_ADD, TT_SUB]:
            if self.idx == 0 or curr.type == TT_SUB:
                self.step()
                factor = res.register(self.factor())
                if res.err:
                    return res
                return res.success(UnaryOpNode(curr, factor))
        elif curr.type == TT_STRING:
            self.step()
            return res.success(StringNode(curr))
        elif curr.type in [TT_INT, TT_FLOAT]:
            self.step()
            return res.success(NumNode(curr))
        elif curr.type == TT_LPAR:
            self.step()
            expr = res.register(self.arith_expr())
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
        res = ParseResult()
        if self.curr_tok.type == TT_IDEN:
            var_name = self.curr_tok
            res.register(self.step())

            if self.curr_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(self.curr_tok.start, self.curr_tok.end, "Expected \"=\""))

            res.register(self.step())
            expr = res.register(self.expr())

            if res.err:
                return res
            return res.success(VarAssignNode(var_name, expr))
        
        expr = res.register(self.arith_expr())
        if self.curr_tok.type in COMPARATORS:
            comparator = self.curr_tok
            res.register(self.step())
            right_expr = res.register(self.arith_expr())
            expr = ExprNode(comparator, expr, right_expr)
        return res.success(expr)

    def arith_expr(self):
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
    # print("tok", tokens)

    if error:
        return None, error
    else:
        parser = Parser(tokens)
        ast = parser.parse()
        # if (ast.err):
        #     print(ast.err)
        # else:
        #     print("ast", ast.node)

        return ast.node, ast.err