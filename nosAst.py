class NoAST:
    """Classe base para os nos da arvore sintática"""
    def __init__(self, linha=None):
        self.linha = linha
#
#                                  ESTRUTURA
#

class DeclaracaoVariavel(NoAST):
    def __init__(self, tipo, nome, linha=None):
        super().__init__(linha)
        self.tipo = tipo
        self.nome = nome

class Programa(NoAST):
    def __init__(
            self,
            nome,
            declaracoes_variaveis,
            declaracoes_funcoes,
            comandos,
            linha=None
    ):
        super().__init__(linha)
        self.nome = nome
        self.declaracoes_variaveis = declaracoes_variaveis
        self.declaracoes_funcoes = declaracoes_funcoes
        self.comandos = comandos

class Parametro(NoAST):
    def __init__(self, tipo, nome, linha=None):
        super().__init__(linha)
        self.tipo = tipo
        self.nome = nome

#Guarda as informacoes da funcao em alguma coisa
class Funcao(NoAST):
    def __init__(self, nome, parametros, tipo_retorno, declaracoes_variaveis, comandos, linha=None):
        super().__init__(linha)
        self.nome = nome
        self.parametros = parametros
        self.tipo_retorno = tipo_retorno
        self.declaracoes_variaveis = declaracoes_variaveis
        self.comandos = comandos

#
#                                  COMANDOS
#

class Atribuicao(NoAST):
    def __init__(self, nome, expressao, linha=None):
        super().__init__(linha)
        self.nome = nome
        self.expressao = expressao

class Leitura(NoAST):
    def __init__(self, identificadores, linha=None):
        super().__init__(linha)
        self.identificadores = identificadores

class Escrita(NoAST):
    def __init__(self, expressoes, linha=None):
        super().__init__(linha)
        self.expressoes = expressoes

#if e else
class Condicional(NoAST):
    def __init__(self, condicao, comandos_se, comandos_senao, linha=None):
        super().__init__(linha)
        self.condicao = condicao
        self.comandos_se = comandos_se
        self.comandos_senao = comandos_senao

#While
class Repeticao(NoAST):
    def __init__(self, condicao, comandos, linha=None):
        super().__init__(linha)
        self.condicao = condicao
        self.comandos = comandos

class Retorno(NoAST):
    def __init__(self, expressao, linha=None):
        super().__init__(linha)
        self.expressao = expressao

#
#                                  EXPRESSOES
#

class Numero(NoAST):
    def __init__(self, valor, linha=None):
        super().__init__(linha)
        self.valor = valor

class Booleano(NoAST):
    def __init__(self, valor, linha=None):
        super().__init__(linha)
        self.valor = valor

class Variavel(NoAST):
    def __init__(self, nome, linha=None):
        super().__init__(linha)
        self.nome = nome

class OperacaoBinaria(NoAST):
    def __init__(self, operador, esquerda, direita, linha=None):
        super().__init__(linha)
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita

class OperacaoUnaria(NoAST):
    def __init__(self, operador, expressao, linha=None):
        super().__init__(linha)
        self.operador = operador
        self.expressao = expressao

class Chamada(NoAST):
    def __init__(self, nome, argumentos, linha=None):
        super().__init__(linha)
        self.nome = nome
        self.argumentos = argumentos
