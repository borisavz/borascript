from parglare import Parser, Grammar

g = Grammar.from_file("borascript.pg")
parser = Parser(g)

res = parser.parse_file("test.bs")

print(res)