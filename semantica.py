from nosAst import Atribuicao, Leitura, Condicional, Repeticao, Numero, Booleano, Variavel, OperacaoBinaria, OperacaoUnaria, Escrita, Chamada, Retorno

#guarda informações sobre os nomes declarados no programa
# Ex: variáveis, parâmetros e funções
class TabelaSimbolos: 
    #Classe usada pela analise semantica para fazer consulta

    def __init__(self):
        self.escopos = [{}] 
        # escopo global do programa

    def entrar_escopo(self):
        self.escopos.append({}) 
        # adiciona um escopo vazio, e sera usado quando a analise semantica comecar 
        # o corpo da funcao

    def sair_escopo(self):
        if len(self.escopos) > 1:
            self.escopos.pop()
        #aqui removemos o escopo mais interno, mas o global permanece

    #recebe o nome e as informações que serão guardadas.
    def declarar(self, nome, informacoes):
        escopo_atual = self.escopos[-1]

        if nome in escopo_atual: #Se tiver o nome nao registra
            return False

        escopo_atual[nome] = informacoes
        return True # se nao tiver registra o nome
    #Tenta registrar um nome noo escopo atual 

    def buscar(self, nome):
        for escopo in reversed(self.escopos):
            if nome in escopo:
                return escopo[nome]
        #procura um nome nos escopos, começando pelo mais interno.
        return None


#Vai percorrer a AST e usa a tabela de símbolos para verificar o programa.
#As definicoes com o comeco _ sao auxiliares
class AnalisadorSemantico:

    def __init__(self):
        self.tabela = TabelaSimbolos()
        self.erros = []
        self.funcao_atual = None #Guarda a função que esta sendo analisada

    #Organiza toda analise
    def analisar(self, programa):

        #registra as variaveis e as assinaturas das funcoes globais
        self.registrar_globais(programa)
        self._visitar_comandos(programa.comandos)

        for funcao in programa.declaracoes_funcoes:
            #percorre cada funcao, e marca qual esta sendo analisada
            self.funcao_atual = funcao
            self.tabela.entrar_escopo()

            for parametro in funcao.parametros:
                self._registrar_parametro(parametro)

            for declaracao in funcao.declaracoes_variaveis:
                self._registrar_variavel(declaracao)

            # Analisa o corpo enquanto o escopo da função esta aberto
            self._visitar_comandos(funcao.comandos)
            
            #Essa funcao pergunta se precisa retornar um valor e nao tem return?
            if(
                funcao.tipo_retorno != "void"
                and not self._possui_retorno(funcao.comandos)):

                self._erro_semantico(
                    f"a funcao '{funcao.nome}' precisa ter um return.",
                    funcao.linha)

            self.tabela.sair_escopo() #Remove o escopo local
            self.funcao_atual = None

        # Retorna true se tiver vazia e false se tiver algum erro  
        return len(self.erros) == 0

#Registra as variaveis e funcoes globais, depois de verifcar um comando o analisador consulta
#a tabela com buscar(nome), cria somente uma tabela
#Os métodos de registro colocam na tabela de símbolos as informações das declarações que 
#estão na AST:
    def registrar_globais(self, programa):
        for declaracao in programa.declaracoes_variaveis:
            self._registrar_variavel(declaracao)

        #registras as funcoes tipo de retorno, nome e tipos dos parametros
        for funcao in programa.declaracoes_funcoes:
            self._registrar_funcao(funcao)

    def _registrar_parametro(self, parametro):
        #Transforma as informacoes de um no parametro apra um registro na tabela
        informacoes = {
            "categoria" : "parametro",
            "tipo" : parametro.tipo,
            "linha" : parametro.linha}

        self._registrar(
            parametro.nome,
            informacoes,
            parametro.linha)

    def _registrar_variavel(self, declaracao):
        #Serve tanto para globais quanto para as locais 
        informacoes = {"categoria" : "variavel",
                       "tipo" : declaracao.tipo,
                       "linha" : declaracao.linha}
        
        self._registrar(declaracao.nome, informacoes, declaracao.linha)

    def _registrar_funcao(self, funcao):
        informacoes = {"categoria" : "funcao",
                        "tipo" : funcao.tipo_retorno,
                        "parametros" : [parametro.tipo for parametro in funcao.parametros],
                        "linha" : funcao.linha}

        self._registrar(
            funcao.nome,
            informacoes,
            funcao.linha)

    def _registrar(self, nome, informacoes, linha):
        if not self.tabela.declarar(nome, informacoes):

            mensagem = (f"'{nome}' ja foi declarado neste escopo.")
            erro = f"Erro semantico na linha {linha}: {mensagem}"
            self.erros.append(erro)
            print(erro)

    def _visitar_comandos(self, comandos):
        #EX: idade = 2+3;
        #O _visitar_comandos reconhece o nó atribuição, verifica se a idade foi declarada
        # e chamada _visitar_expressao para analisar a soma, sendo assim ele reconhece a
        # OperacaoBinaria, visita os dois operandos para realizar o calculo, isso serve
        # para if, else ou while fazendo a mesma logica de verificação
 
        for comando in comandos:

            #Esse trecho verifica se o destino foi declarado e se a expressão tem o mesmo
            #tipo. Por exemplo, atribuir true a uma variável int gera erro.
            if isinstance(comando, Atribuicao):
                self._verificar_variavel(comando.nome, comando.linha)

                simbolo = self.tabela.buscar(comando.nome)
                tipo_expressao = self._visitar_expressao(comando.expressao)

                if(
                    simbolo is not None
                    and simbolo["categoria"] in ("variavel", "parametro")
                    and tipo_expressao is not None
                    and tipo_expressao != simbolo["tipo"]
                ):
                    self._erro_semantico(
                        f"atribuicao para '{comando.nome}' espera "
                        f"'{simbolo['tipo']}', mas recebeu "
                        f"'{tipo_expressao}'.",
                        comando.linha)
                    
            elif isinstance(comando, Leitura):
                #Verifica se os dois nomes foram declarados como variaveis ou parametros.
                for nome in comando.identificadores:
                    self._verificar_variavel(nome, comando.linha)

            elif isinstance(comando, Escrita):
                for expressao in comando.expressoes:
                    tipo = self._visitar_expressao(expressao)

                    if tipo is not None and tipo not in ("int", "bool"):
                        self._erro_semantico(
                            "print aceita somente expressoes dos tipos 'int' ou 'bool'.",
                            expressao.linha) 
                #Analisa cada expressao dentro de print e verificar se e do tipo int ou bool

            elif isinstance(comando, Chamada):
                self._visitar_expressao(comando)

            #se encontrar condicional descobre qual if
            elif isinstance(comando, Condicional):
                tipo_condicao = self._visitar_expressao(comando.condicao)

                if tipo_condicao is not None and tipo_condicao != "bool":
                    self._erro_semantico(
                        "a condicao do if deve ter tipo 'bool'.",
                        comando.linha)
                    #se a condicao for diferente de bool da erro
                    
                self._visitar_comandos(comando.comandos_se)
                #verifica nome dentro do if, se tiver else olha tambem

                if comando.comandos_senao is not None:
                    self._visitar_comandos(comando.comandos_senao)

            #se encontrar condicional descobre qual while
            elif isinstance(comando, Repeticao):
                tipo_condicao = self._visitar_expressao(comando.condicao)

                if tipo_condicao is not None and tipo_condicao != 'bool':
                    self._erro_semantico(
                        "a condicao do while deve ter tipo 'bool'.",
                        comando.linha)
                    
                self._visitar_comandos(comando.comandos)

            #se encontra return verifica se esta fora da funcao
            #se tiver dentro retorna o tidpo de expressao e o tipo de declaracao
            elif isinstance(comando, Retorno):
                if self.funcao_atual is None:
                    self._erro_semantico(
                        "return so pode ser usado dentro de uma funcao.",
                        comando.linha)
                    
                else:
                    tipo_expressao = self._visitar_expressao(comando.expressao)
                    tipo_esperado = self.funcao_atual.tipo_retorno

                    if tipo_esperado == "void":
                        self._erro_semantico(
                            "funcao void nao deve retornar um valor.",
                            comando.linha
                        )

                    elif(
                        tipo_expressao is not None
                        and tipo_expressao != tipo_esperado):

                        self._erro_semantico(
                            f"o return deve ter tipo '{tipo_esperado}', "
                            f"mas recebeu '{tipo_expressao}'.",
                            comando.linha)

#procura se existe um retorno
    def _possui_retorno(self, comandos):
    #procura return nos comandos da função e também dentro de blocos if, else e while.

        for comando in comandos:
            if isinstance(comando, Retorno):
                return True
            #procura o no retorno

            if isinstance(comando, Condicional):
                if self._possui_retorno(comando.comandos_se):
                    return True

                if (
                    comando.comandos_senao is not None 
                    and self._possui_retorno(comando.comandos_senao)):

                    return True

            elif isinstance(comando, Repeticao):
                if self._possui_retorno(comando.comandos):
                    return True
        
        return False

#confere o nome, procura o nome na tabela
#tendo tres opcoes
    #Nome não encontrado
    #Nome encontrado mas representa uma funcao
    #Nome encontrado como variavel ou parametro
    def _verificar_variavel(self, nome, linha):
    #o proposito e verificar se o nome pode ser usado como variavel
        #Acessa direto a tabela para verifcar
        informacoes = self.tabela.buscar(nome)

        if informacoes is None:
            erro = (f"Erro semantico na linha {linha}: "
                    f"variavel '{nome}' nao foi declarada.")
            self.erros.append(erro)
            print(erro)

        elif informacoes["categoria"] not in ("variavel", "parametro"):
            erro = (f"Erro semantico na linha {linha}: "
                    f'{nome} nao e uma variavel.')
            self.erros.append(erro)
            print(erro)

#Verificar os tipos de expressao
    def _visitar_expressao(self, expressao):
        if isinstance(expressao, Numero):
            return "int"

        if isinstance(expressao, Booleano):
            return "bool"

        if isinstance(expressao, Variavel):
            simbolo = self.tabela.buscar(expressao.nome)

            if simbolo is None:
                self._erro_semantico(f"variavel '{expressao.nome}' nao foi declarada.",
                                     expressao.linha)
                return None

            if simbolo["categoria"] not in ("variavel", "parametro"):
                self._erro_semantico(f"'{expressao.nome}' nao e uma variavel.",
                                     expressao.linha)
                return None

            return simbolo["tipo"]

        if isinstance(expressao, Chamada):
            simbolo = self.tabela.buscar(expressao.nome)

            if simbolo is None:
                self._erro_semantico(
                    f"funcao '{expressao.nome}' nao foi declarada.",
                    expressao.linha
                )
                return None

            if simbolo["categoria"] != "funcao":
                self._erro_semantico(
                    f"'{expressao.nome}' nao e uma funcao.",
                    expressao.linha
                )
                return None
            
            tipos_parametros = simbolo["parametros"]

            if len(expressao.argumentos) != len(tipos_parametros):
                self._erro_semantico(
                    f"funcao '{expressao.nome}' espera {len(tipos_parametros)} "
                    f"argumento(s), mas recebeu {len(expressao.argumentos)}.",
                    expressao.linha
                )    

            for indice, argumento in enumerate(expressao.argumentos):
                tipo_argumento = self._visitar_expressao(argumento)

                if (
                    indice < len (tipos_parametros)
                    and tipo_argumento is not None
                    and tipo_argumento != tipos_parametros[indice]):

                    self._erro_semantico(
                        f"argumento {indice + 1} da funcao '{expressao.nome}' "
                        f"deve ser do tipo '{tipos_parametros[indice]}', "
                        f"mas recebeu '{tipo_argumento}'.",
                        argumento.linha
                    )

            return simbolo["tipo"]

        if isinstance(expressao, OperacaoUnaria):
            #Analisa primeiro o operando
            tipo = self._visitar_expressao(expressao.expressao)

            if tipo is None:
                return None

            if expressao.operador == "-" and tipo == "int":
                return "int"

            if expressao.operador == "!" and tipo == "bool":
                return "bool"

            self._erro_semantico(
                f"operador '{expressao.operador}' nao pode ser usado "
                f"com o tipo '{tipo}'.",
                expressao.linha)
            
            return None

        if isinstance(expressao, OperacaoBinaria):
            #Analisa os dois lados
            tipo_esquerda = self._visitar_expressao(expressao.esquerda)
            tipo_direita = self._visitar_expressao(expressao.direita)

            if tipo_esquerda is None or tipo_direita is None:
                return None

            operador = expressao.operador

            if operador in ("+", "-", "*", "/"):
                if tipo_esquerda == "int" and tipo_direita == "int":
                    return "int"

            elif operador in ("<", "<=", ">", ">="):
                if tipo_esquerda == "int" and tipo_direita == "int":
                    return "bool"

            elif operador in ("==", "!="):
                if tipo_esquerda == tipo_direita:
                    return "bool"

            elif operador in ("&&", "||"):
                if tipo_esquerda == "bool" and tipo_direita == "bool":
                    return "bool"

            self._erro_semantico(
                f"operador '{operador}' nao aceita operandos dos tipos "
                f"'{tipo_esquerda}' e '{tipo_direita}'.",
                expressao.linha)
            
            return None

    def _erro_semantico(self, mensagem, linha):
        erro = f"Erro semantico na linha {linha}: {mensagem}"
        self.erros.append(erro)
        print(erro)