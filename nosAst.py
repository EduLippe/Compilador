class NoAST:
    """Classe base para os nos da arvore sintática"""
    pass

class DeclaracaoVariavel(NoAST):
    def __init__(self, tipo, nome):
        self.tipo = tipo
        self.nome = nome

class Programa(NoAST):
    def __init__(
            self,
            nome,
            declaracoes_variaveis,
            declaracoes_funcoes,
            comandos
    ):
        self.nome = nome
        self.declaracoes_variaveis = declaracoes_variaveis
        self.declaracoes_funcoes = declaracoes_funcoes
        self.comandos = comandos

class Parametro(NoAST):
    def __init__(self, tipo, nome):
        self.tipo = tipo
        self.nome = nome
        