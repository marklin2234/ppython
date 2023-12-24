from basic import ExprNode, NumNode, UnaryOpNode
from constants import *
from error import RTError

class RTResult:
    def __init__(self):
        self.value = None
        self.err = None

    def register(self, res):
        if isinstance(res, RTResult):
            if res.err:
                self.err = res.err
            return res.value

        return res

    def success(self, value):
        self.value = value
        return self

    def failure(self, err):
        self.err = err
        return self
    
    def set_context(self, context):
        self.context = context
        return self

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos

    def __repr__(self) -> str:
        return f'{self.display_name}, {self.parent}, {self.parent_entry_pos}'

class Interpreter:
    def __init__(self, ast):
        self.ast = ast

    def evaluate(self):
        ctx = Context('<ppython>')
        return self.traverse_ast(self.ast, ctx)

    def traverse_ast(self, node, context):
        res = RTResult()
        if isinstance(node, ExprNode):
            left = res.register(self.traverse_ast(node.left, context))
            right = res.register(self.traverse_ast(node.right, context))
            if (node.op.type == TT_ADD):
                return res.success(left + right).set_context(context)
            elif (node.op.type == TT_SUB):
                return res.success(left - right).set_context(context)
            elif (node.op.type == TT_MULT):
                return res.success(left * right).set_context(context)
            elif (node.op.type == TT_DIV):
                if (right == 0):
                    print(node.left.tok)
                    return res.failure(RTError(node.left.tok.start, node.right.tok.end, 'Division by zero', context))
                return res.success(left / right).set_context(context)
        elif isinstance(node, UnaryOpNode):
            num = res.register(self.traverse_ast(node.node, context))
            if res.err:
                return res
            if node.op.type == TT_SUB:
                num *= -1
            return res.success(num).set_context(context)
        elif isinstance(node, NumNode):
            return res.success(node.tok.value).set_context(context)
        
        return res.success(0).set_context(context)
    
def run(ast):
    interpreter = Interpreter(ast)
    res = interpreter.evaluate()
    return res.value, res.err