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
        vars.set(proc.params[i].name, args[i])

    if not hasattr(proc, 'statements'):
        return

    for s in proc.statements:
        statement_type = type(s).__name__

        if 'ProcedureCallStatement' == statement_type:
            execute_procedure_call(ast, s.procedure, vars)
        elif 'Declaration' == statement_type:
            execute_declaration(ast, s, vars)
        elif 'Assignment' == statement_type:
            execute_assignment(ast, s, vars)
        elif 'Return' == statement_type:
            if hasattr(s, 'val'):
                return evaluate_expression(ast, s.val, vars)
            else:
                return

def execute_procedure_call(ast, proc_call, vars):
    if proc_call.name == 'input':
        return int(input(">> "))
    elif proc_call.name == 'print':
        if proc_call.args is not None:
            for a in proc_call.args:
                print(evaluate_expression(ast, a.expr, vars))

        return

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
    vars.set(declaration.name, evaluate_expression(ast, declaration.rval, vars))

def execute_assignment(ast, assignment, vars):
    vars.set(assignment.lval.name, evaluate_expression(ast, assignment.rval, vars))

def evaluate_expression(ast, expression, vars):
    if hasattr(expression, 'op'):
        if expression.op == '^':
            return evaluate_expression(ast, expression.l, vars) ** evaluate_expression(ast, expression.r, vars)
        elif expression.op == '*':
            return evaluate_expression(ast, expression.l, vars) * evaluate_expression(ast, expression.r, vars)
        elif expression.op == '/':
            return evaluate_expression(ast, expression.l, vars) / evaluate_expression(ast, expression.r, vars)
        elif expression.op == '+':
            return evaluate_expression(ast, expression.l, vars) + evaluate_expression(ast, expression.r, vars)
        elif expression.op == '-':
            return evaluate_expression(ast, expression.l, vars) - evaluate_expression(ast, expression.r, vars)
        elif expression.op == '<':
            return evaluate_expression(ast, expression.l, vars) < evaluate_expression(ast, expression.r, vars)
        elif expression.op == '<=':
            return evaluate_expression(ast, expression.l, vars) <= evaluate_expression(ast, expression.r, vars)
        elif expression.op == '>':
            return evaluate_expression(ast, expression.l, vars) > evaluate_expression(ast, expression.r, vars)
        elif expression.op == '>=':
            return evaluate_expression(ast, expression.l, vars) >= evaluate_expression(ast, expression.r, vars)
        elif expression.op == '==':
            return evaluate_expression(ast, expression.l, vars) == evaluate_expression(ast, expression.r, vars)
        elif expression.op == '!=':
            return evaluate_expression(ast, expression.l, vars) != evaluate_expression(ast, expression.r, vars)
        elif expression.op == '&&':
            return evaluate_expression(ast, expression.l, vars) and evaluate_expression(ast, expression.r, vars)
        elif expression.op == '||':
            return evaluate_expression(ast, expression.l, vars) or evaluate_expression(ast, expression.r, vars)
        elif expression.op == '!':
            return not evaluate_expression(ast, expression.r, vars)
    elif hasattr(expression, 'num'):
        return int(expression.num)
    elif hasattr(expression, 'bool'):
        return bool(expression.bool)
    elif hasattr(expression, 'id'):
        return vars.get(expression.id)
    elif hasattr(expression, 'proc'):
        return execute_procedure_call(ast, expression.proc, vars)
    elif hasattr(expression, 'expr'):
        return evaluate_expression(ast, expression.expr, vars)

g = Grammar.from_file("borascript.pg")
parser = Parser(g)

ast = parser.parse_file("test.bs")

main_proc = next(filter(lambda p: p.name == 'main', ast.procedures), None)

if main_proc == None:
    print("Missing main!")
    exit()

execute_procedure(ast, main_proc, [])