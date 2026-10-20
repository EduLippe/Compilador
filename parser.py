import ply.yacc as yacc
from lexer import tokens, literals, lexer
from nosAst import DeclaracaoVariavel, Programa, Parametro, Funcao, Atribuicao, Numero, Booleano, Variavel, Leitura

#Ensinando o parser a reconhcer uma sequencia de zero ou mais declarações de funcao
#usa p por que o PLY procuras regras da gramatica nessa formatação
def p_declaracoes_funcoes(p):
    """declaracoes_funcoes : declaracoes_funcoes declaracao_funcao
                            | empty""" 
    #gramatica que o PLy le
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = p[1]

#Fala que um comando pode ser uma atribuicao
def p_comando(p):
    """comando : atribuicao
                | leitura"""
    p[0] = p[1]

#Reconhece uma atribuicao EX: idade = 20
def p_atribuicao(p):
    """atribuicao : ID '=' expressao ';'"""
    p[0] = Atribuicao(p[1], p[3])

#Ta reconhecendo uma lista de nomes separados por vírgula EX: a, b, c
def p_lista_identificadores(p):
    """lista_identificadores : lista_identificadores ',' ID
                                | ID"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

#reconhece o comando READ
def p_leituira(p):
    """leitura : READ '(' lista_identificadores ')' ';'"""
    p[0] = Leitura(p[3])

#Vai reconhecer um número escrito no código,
def p_expressao_numero(p):
    """expressao : NUM"""
    p[0] = Numero(p[1])

#reconhece true ou False
def p_expressao_booleano(p):
    """expressao : TRUE
                    | FALSE"""
    p[0] = Booleano(p[1] == 'true')

#Reconhe o uso de uma variavel (x) dentro da expressao
def p_expressao_variavel(p):
    """expressao : ID"""
    p[0] = Variavel(p[1])

#Ensinando o parser a reconhcer uma sequencia de zero ou mais variaveis
def p_declaracoes_variaveis(p):
    """declaracoes_variaveis : declaracoes_variaveis declaracao_variavel
                                | empty """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = p[1]

#Guarda todos os comandos que aparecem no programa
#Ensinando o parser a reconhcer uma sequencia de zero ou mais comandos
def p_comandos(p):
    """comandos : comandos comando
                | empty """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = p[1]

#Represetna a estrutural geral do programa
# p4 declarações de variaveis
# p5 lista de declarações de funcoes
# p6 lista de comandos
def p_programa(p):
    """programa : PROGRAM ID '{' declaracoes_variaveis declaracoes_funcoes comandos '}'"""
    p[0] = Programa(
       p[2],
       p[4],
       p[5],
       p[6]
   )

def p_empty(p):
    """empty :"""
    p[0] = []

#Reconhece uma declaração
def p_declaracao_variavel(p):
    """declaracao_variavel : tipo ID ';' """
    p[0] = DeclaracaoVariavel(p[1], p[2])
#Exemplo do que essa função cria no nó (DeclaracaoVariavel("int", "idade"))

#Reconhece se é int ou bool e repassa o valor do token
def p_tipo(p):
    """tipo : INT   
            | BOOL"""
    p[0] = p[1]

def p_tipo_retorno(p):
    """tipo_retorno : tipo
                    | VOID"""
    p[0] = p[1]

#um parâmetro é um tipo seguido de um identificador, como em int(p1) a(p2)
def p_parametro(p):
    """parametro : tipo ID"""
    p[0] = Parametro(p[1], p[2])

#Vai reconhecer um ou mais parametros sempre separados por uma ','
def p_lista_parametros(p):
    """lista_parametros : lista_parametros ',' parametro 
                        | parametro"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

#Caso uma funcao nao tenha nenhum parametro
def p_parametros_opcionais(p):
    """parametros_opcionais : lista_parametros
                            | empty"""
    p[0] = p[1]

#Define a regra para reconhecer uma declaracao de funcao da linguagem 
def p_declaracao_funcao(p):
    """declaracao_funcao : FUN ID '(' parametros_opcionais ')' SETA tipo_retorno '{' declaracoes_variaveis comandos '}'"""
    p[0] = Funcao(p[2], p[4], p[7], p[9], p[10])

#Chama erro quando encontra um token que nao tem na gramatica
def p_error(p):
    if p is None:
        print ("Erro sintatico: o arquivo terminou antes do esperado.")
    else: 
        print(
            f"Erro sintatico na linha {p.lineno}: " 
            f"token inesperado {p.value!r}." 
        )

parser = yacc.yacc(start='programa')