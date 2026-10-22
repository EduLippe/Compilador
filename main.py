import sys
from lexer import lexer
from parser import parser
from nosAst import NoAST

#percorre a arvore e a partir da raiz imprime cada no em um nivel mais a direita
def imprimir_arvore(no, nivel=0, rotulo=""):
    recuo = " " * nivel
    prefixo = f"{rotulo}: " if rotulo else""

    if isinstance(no, NoAST):
        print(f"{recuo}{prefixo}{type(no).__name__}")
        for campo, valor in vars(no).items():
            imprimir_arvore(valor, nivel + 1, campo)
    elif isinstance(no, NoAST):
        if no:
            print(f"{recuo}{prefixo}lista")
            for item in no:
                imprimir_arvore(item, nivel + 1)
        else:
            print(f"{recuo}{prefixo}lista vazia")
    else:
        print(f"{recuo}{prefixo}{no!r}")

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py arquivo.coda")
        sys.exit(1)

    caminho = sys.argv[1]
    try:
        with open(caminho, encoding='utf-8') as arquivo:
            codigo = arquivo.read()
    except OSError:
        print(f"Erro: nao foi possivel abrir o arquivo '{caminho}'")
        sys.exit(1)

    lexer.lineno = 1
    arvore = parser.parse(codigo, lexer=lexer)

    if arvore is None:
        print("Compilacao interrompida: erros sintaticos.")
        sys.exit(1)

    print("Analise sintatica concluida sem erros.")
    imprimir_arvore(arvore)

if __name__ == "__main__":
    main()