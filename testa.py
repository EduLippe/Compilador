from parser import parser
from lexer import lexer

codigo = """program t {
  int x;
  fun soma(int a, int b) -> int { return a + b; }
  fun nada() -> void { }
  x = soma(1, 2 * 3) + soma(x, 4);
  nada();
  soma(1, 2);
  print(soma(1, 2));
}"""

lexer.lineno = 1
r = parser.parse(codigo, lexer=lexer)

for c in r.comandos:
    print(type(c).__name__)

a = r.comandos[0].expressao
print(a.operador, type(a.esquerda).__name__, type(a.direita).__name__)