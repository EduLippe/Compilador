from parser import parser
from lexer import lexer

codigo = """program teste {
  int x;
  bool b;
  fun soma(int a, int c) -> int {
    int r;
    r = a;
    r = 5;
  }
  fun nada() -> void { }
  x = 10;
  b = true;
  x = x;
}"""

lexer.lineno = 1
r = parser.parse(codigo, lexer=lexer)

for c in r.comandos:
    print(type(c).__name__, c.nome, type(c.expressao).__name__)