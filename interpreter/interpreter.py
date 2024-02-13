from interpreter.values import Number
from parse import ExprNode, NumNode, UnaryOpNode, VarVisitNode, VarAssignNode
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
        self.variable_table = None

    def __repr__(self) -> str:
        return f'{self.display_name}, {self.parent}, {self.parent_entry_pos}'
    
class VariableTable:
    def __init__(self):
        self.variables = {}
    
    def get(self, value):
        return self.variables.get(value, None)
    
    def set(self, name, value):
        self.variables[name] = value

class Interpreter:
    def __init__(self, ast):
        self.ast = ast

    def evaluate(self, ctx):
        return self.traverse_ast(self.ast, ctx)

    def traverse_ast(self, node, context):
        res = RTResult()
        if isinstance(node, VarAssignNode):
            var_name = node.name.value

            value = res.register(self.traverse_ast(node.value, context))
            if res.err:
                return res

            context.variable_table.set(var_name, value)
            return res.success(value).set_context(context)
        elif isinstance(node, VarVisitNode):
            var_name = node.name.value
            value = context.variable_table.get(var_name)
            if value is None:
                return res.failure(RTError(node.start, node.end, f'{var_name} is not assigned', context))
            return res.success(value.set_pos(node.start, node.end)).set_context(context)
        elif isinstance(node, ExprNode):
            left_node = node.left
            right_node = node.right
            left = res.register(self.traverse_ast(left_node, context))
            right = res.register(self.traverse_ast(right_node, context))
            if res.err: return res
            start = left_node.start
            end = right_node.end
            if (node.op.type == TT_ADD):
                return res.success((left + right).set_pos(start, end)).set_context(context)
            elif (node.op.type == TT_SUB):
                return res.success((left - right).set_pos(start, end)).set_context(context)
            elif (node.op.type == TT_MULT):
                return res.success((left * right).set_pos(start, end)).set_context(context)
            elif (node.op.type == TT_DIV):
                if (right == 0):
                    return res.failure(RTError(start, end, 'Division by zero', context))
                return res.success((left / right).set_pos(start, end)).set_context(context)
        elif isinstance(node, UnaryOpNode):
            num = res.register(self.traverse_ast(node.node, context))
            if res.err:
                return res
            if node.op.type == TT_SUB:
                num *= -1

            return res.success(Number(num, num.type).set_pos(node.op.start, node.node.tok.end)).set_context(context)
        elif isinstance(node, NumNode):
            return res.success(Number(node.tok.value, node.tok.type).set_pos(node.tok.start, node.tok.end)).set_context(context)
        
        return res.success(0).set_context(context)

glob_var_table = VariableTable()

def run(ast):
    interpreter = Interpreter(ast)
    ctx = Context('<ppython>')
    ctx.variable_table = glob_var_table
    res = interpreter.evaluate(ctx)
    return res.value, res.err