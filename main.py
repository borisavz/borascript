from parglare import Parser, Grammar

class Variables:
    def __init__(self):
        self.vars = {}
        self.parent = None

    def set(self, key, value):
        self.vars[key] = value

    def get(self, key):
        if key in self.vars:
            return self.vars[key]
        elif self.parent is not None:
            self.parent.get(key)
        else:
            print("No variable " + key)
            exit()

def execute_procedure(ast, proc, args):
    vars = Variables()

    if len(args) != len(proc.params):
        print("Wrong param num!")
        exit()

    for i in range(0, len(args)):
        vars.set(proc.params[i], args[i])

    if not hasattr(proc, 'statements'):
        return

    for s in proc.statements:
        statement_type = type(s).__name__

        if 'ProcedureCallStatement' == statement_type:
            execute_procedure_call(ast, s.procedure, vars)
        elif 'Declaration' == statement_type:
            execute_declaration(ast, s, vars)
        elif 'Return' == statement_type:
            if hasattr(s, 'val'):
                return evaluate_expression(ast, s.val, vars)
            else:
                return

def execute_procedure_call(ast, proc_call, vars):
    proc = next(filter(lambda p: p.name == proc_call.name, ast.procedures), None)

    if proc is not None:
        args = []

        if proc_call.args is not None:
            for a in proc_call.args:
                args.append(evaluate_expression(ast, a.expr, vars))

        return execute_procedure(ast, proc, args)
    else:
        print("Missing procedure " + proc_call.name)
        exit()

def execute_declaration(ast, declaration, vars):
    vars.set(declaration.name, 0)

def evaluate_expression(ast, expression, vars):
    expr_type = type(expression).__name__
    print(expr_type)

    if 'E1' == expr_type:
        return evaluate_e1(ast, expression, vars)
    elif 'E2' == expr_type:
        return evaluate_e2(ast, expression, vars)
    elif 'E3' == expr_type:
        return evaluate_e3(ast, expression, vars)
    elif 'E4' == expr_type:
        return evaluate_e4(ast, expression, vars)

def evaluate_e1(ast, expression, vars):
    if hasattr(expression, 'l'):
        if expression.op == '+':
            return evaluate_expression(ast, expression.l, vars) + evaluate_expression(ast, expression.r, vars)
        else:
            return evaluate_expression(ast, expression.l, vars) - evaluate_expression(ast, expression.r, vars)
    else:
        return evaluate_expression(ast, expression.val, vars)

def evaluate_e2(ast, expression, vars):
    if hasattr(expression, 'l'):
        if expression.op == '*':
            return evaluate_expression(ast, expression.l, vars) * evaluate_expression(ast, expression.r, vars)
        else:
            return evaluate_expression(ast, expression.l, vars) / evaluate_expression(ast, expression.r, vars)
    else:
        return evaluate_expression(ast, expression.val, vars)

def evaluate_e3(ast, expression, vars):
    if hasattr(expression, 'l'):
        return evaluate_expression(ast, expression.l, vars) ** evaluate_expression(ast, expression.r, vars)
    else:
        return evaluate_expression(ast, expression.val, vars)

def evaluate_e4(ast, expression, vars):
    if hasattr(expression, 'num'):
        return int(expression.num)
    elif hasattr(expression, 'bool'):
        return bool(expression.bool)
    elif hasattr(expression, 'id'):
        return vars.get(expression.id)
    elif hasattr(expression, 'proc'):
        return execute_procedure_call(ast, expression.proc, vars)
    else:
        return evaluate_expression(ast, expression.expr, vars)

g = Grammar.from_file("borascript.pg")
parser = Parser(g)

ast = parser.parse_file("test.bs")

main_proc = next(filter(lambda p: p.name == 'main', ast.procedures), None)

if main_proc == None:
    print("Missing main!")
    exit()

execute_procedure(ast, main_proc, [])