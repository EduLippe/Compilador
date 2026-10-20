from parser import parser
from lexer import lexer

codigo = """program t {
  int a;
  print(a);
  print(1, true, a);
  read(a);
}"""

lexer.lineno = 1
r = parser.parse(codigo, lexer=lexer)

for c in r.comandos:
    if type(c).__name__ == 'Escrita':
        print('Escrita', [type(e).__name__ for e in c.expressoes])
    else:
        print(type(c).__name__)