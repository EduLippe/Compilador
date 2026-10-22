import ply.lex as lex


#Palvras reservadas
reservadas = {
    'program' : 'PROGRAM',
    'fun':'FUN',
    'int':'INT',
    'bool':'BOOL',
    'void':'VOID',
    'if':'IF',
    'else':'ELSE',
    'while':'WHILE',
    'return':'RETURN',
    'read':'READ',
    'print':'PRINT',
    'true':'TRUE',
    'false':'FALSE',
}

tokens = (
    'ID','NUM','SETA','IGUAL','DIFERENTE','MENOR_IGUAL','MAIOR_IGUAL',
    'E_LOGICO','OU_LOGICO') + tuple(reservadas.values())

#Nao precisam de token, sao caracteres soltos
literals = ['(', ')', ';', '{', '}', ',', '=', '<', '>', '+', '-', '*', '/', '!']


t_SETA           = r'->'
t_IGUAL          = r'=='
t_DIFERENTE      = r'!='
t_MENOR_IGUAL    = r'<='
t_MAIOR_IGUAL    = r'>='
t_E_LOGICO       = r'&&'
t_OU_LOGICO      = r'\|\|'

t_ignore = ' \t'
tem_erro_lexico = False

def t_newline(t): #Contas as linhas
    r'\n+'
    t.lexer.lineno += len (t.value)

#Ignora o comentario
def t_COMENTARIO(t): 
    r'//[^\n]*'
    pass

#Vira palavra reservada se for, se não fica ID mesmo
def t_ID(t): 
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value, 'ID')
    return t

def t_NUM(t): #Valor vira um inteiro
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_error(t):
    global tem_erro_lexico
    tem_erro_lexico = True
    print(f"ERRO léxico na linha {t.lineno}: caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
