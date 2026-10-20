from Coda_lexer import lexer

codigo = """
program fun int bool void if else while return read print true false
nome_1 123 -> == != < <= > >= + - * / && || ! = ; , ( ) { }
// este comentário deve ser ignorado
outro_nome
"""

lexer.lineno = 1
lexer.input(codigo)

while True:
    token = lexer.token()
    if token is None:
        break
    print(token.type, repr(token.value), token.lineno)