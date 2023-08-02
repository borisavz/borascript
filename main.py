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
            exit()

def execute_procedure(ast, proc, args):
    vars = Variables()

    if not hasattr(proc, 'statements'):
        return

    for s in proc.statements:
        statement_type = type(s).__name__

        if 'ProcedureCallStatement' == statement_type:
            execute_procedure_call(ast, s.procedure.name, None, vars)
        elif 'Declaration' == statement_type:
            execute_declaration(ast, s, vars)

def execute_procedure_call(ast, proc_name, args_expr, vars):
    proc = next(filter(lambda p: p.name == proc_name, ast.procedures), None)

    if proc is not None:
        execute_procedure(ast, proc, None)
    else:
        print("Missing procedure " + proc_name)
        exit()

def execute_declaration(ast, declaration, vars):
    vars.set(declaration.name, 0)

g = Grammar.from_file("borascript.pg")
parser = Parser(g)

ast = parser.parse_file("test.bs")

main_proc = next(filter(lambda p: p.name == 'main', ast.procedures), None)

if main_proc == None:
    print("Missing main!")
    exit()

execute_procedure(ast, main_proc, None)