class NoAST:
    """Classe base para os nos da arvore sintática"""
    pass

#
#                                  ESTRUTURA
#
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

#Guarda as informacoes da funcao em alguma coisa
class Funcao(NoAST):
    def __init__(self, nome, parametros, tipo_retorno, declaracoes_variaveis, comandos):
        self.nome = nome
        self.parametros = parametros
        self.tipo_retorno = tipo_retorno
        self.declaracoes_variaveis = declaracoes_variaveis
        self.comandos = comandos

#
#                                  COMANDOS
#
class Atribuicao(NoAST):
    def __init__(self, nome, expressao):
        self.nome = nome
        self.expressao = expressao

class Leitura(NoAST):
    def __init__(self, identificadores):
        self.identificadores = identificadores

class Escrita(NoAST):
    def __init__(self, expressoes):
        self.expressoes = expressoes

#if e else
class Condicional(NoAST):
    def __init__(self, condicao, comandos_se, comandos_senao):
        self.condicao = condicao
        self.comandos_se = comandos_se
        self.comandos_senao = comandos_senao

#While
class Repeticao(NoAST):
    def __init__(self, condicao, comandos):
        self.condicao = condicao
        self.comandos = comandos

class Retorno(NoAST):
    def __init__(self, expressao):
        self.expressao = expressao

#
#                                  EXPRESSOES
#
class Numero(NoAST):
    def __init__(self, valor):
        self.valor = valor

class Booleano(NoAST):
    def __init__(self, valor):
        self.valor = valor

class Variavel(NoAST):
    def __init__(self, nome):
        self.nome = nome

class OperacaoBinaria(NoAST):
    def __init__(self, operador, esquerda, direita):
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita

class OperacaoUnaria(NoAST):
    def __init__(self, operador, expressao):
        self.operador = operador
        self.expressao = expressao

class Chamada(NoAST):
    def __init__(self, nome, argumentos):
        self.nome = nome
        self.argumentos = argumentos
