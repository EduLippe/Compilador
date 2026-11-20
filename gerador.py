'''
1	Inicialização e finalização	(INPP, PARA, FIM)
2	Alocação de variáveis	(AMEM, DMEM)
3	Constantes e variáveis	(CRCT, CRVL, ARMZ)
4	Operações aritméticas	(SOMA, SUBT, MULT, DIVI, INVR)
5	Operações lógicas e relacionais	(CONJ, DISJ, NEGA, CMME, CMMA etc.)
6	Condicionais	(DSVF, DSVS, NADA)
7	Repetições	(DSVF, DSVS, NADA)
8	Funções e procedimentos	(CHPR, ENPR, RTPR)
9	Retorno de funções	ARMZ e gerenciamento do valor de retorno
10	Integração	Geração do arquivo MEPA

'''

from nosAst import (Programa, Funcao, Atribuicao, Leitura, Escrita, Condicional, Repeticao,
                    Retorno, Numero, Booleano, Variavel, OperacaoBinaria, OperacaoUnaria, Chamada)

class GeradorCodigo:
    INSTRUCOES_BINARIAS = {
        "+": "SOMA",
        "-": "SUBT",
        "*": "MULT",
        "/": "DIVI",
        "<": "CMME",
        "<=": "CMEG",
        ">": "CMMA",
        ">=": "CMAG",
        "==": "CMIG",
        "!=": "CMDG",
        "&&": "CONJ",
        "||": "DISJ",
    }

    def __init__(self, analisador_semantico):
        self.codigo = [] #Guarda instruções geradas
        self.contador_rotulos = 0

        #Aproveita a tabela da Analise semantica
        self.tabela = analisador_semantico.tabela

        # Guarda os escopos locais
        self.escopos_funcoes = analisador_semantico.escopos_funcoes

        #guarda a quantidade de variaveis globais
        self.quantidade_globais = (analisador_semantico.proximo_deslocamento_global)

        #Indica qual furcao esta sendo gerada no momento
        self.funcao_atual = None
        self.rotulos_funcoes = {}

#Adiciona instrucao ao codigo gerado ficando na ordem que foram mandadas
    def emitir(self, instrucao):
        self.codigo.append(instrucao)

    def novo_rotulo(self):
        rotulo = f"L{self.contador_rotulos}"
        self.contador_rotulos += 1
        return rotulo
    
    def _buscar(self, nome):

        # Se estiver dentro de uma funcao, procura primeiro
        # nos parametros e nas variaveis locais dela
        if self.funcao_atual is not None:

            escopo_local = self.escopos_funcoes.get(
                self.funcao_atual, {}
            )

            if nome in escopo_local:
                return escopo_local[nome]

        # se nao achar dentro procura no escopo de fora
        return self.tabela.escopos[0].get(nome)

#INPP - inicia a primeira linha e prepara a pilha de dados
#PARA - interrompe a execucao
#FIM - Marca o fim
    def _gerar_expressao(self, expressao):
        if isinstance(expressao, Numero):
            self.emitir(f"CRCT {expressao.valor}")

        elif isinstance(expressao, Booleano):
            valor = 1 if expressao.valor else 0
            self.emitir(f"CRCT {valor}")

        elif isinstance(expressao, Variavel):
            simbolo = self._buscar(expressao.nome)
            self.emitir(f"CRVL {simbolo['nivel']},{simbolo['deslocamento']}")

        elif isinstance(expressao, OperacaoBinaria):
            self._gerar_expressao(expressao.esquerda)
            self._gerar_expressao(expressao.direita)
            self.emitir(self.INSTRUCOES_BINARIAS[expressao.operador])

        elif isinstance(expressao, OperacaoUnaria):
                    self._gerar_expressao(expressao.expressao)
                    if expressao.operador == "-":
                        self.emitir("INVR")
                    elif expressao.operador == "!":
                        self.emitir("NEGA")

    def _gerar_comandos(self, comandos):
        for comando in comandos:
            if isinstance(comando, Atribuicao):
                self._gerar_expressao(comando.expressao)
                simbolo = self._buscar(comando.nome)
                self.emitir(f"ARMZ {simbolo['nivel']},{simbolo['deslocamento']}")

            elif isinstance(comando, Condicional):
                self._gerar_expressao(comando.condicao)
                rotulo_senao = self.novo_rotulo()
                self.emitir(f"DSVF {rotulo_senao}")
                self._gerar_comandos(comando.comandos_se)

                if comando.comandos_senao is None:
                    self.emitir(f"{rotulo_senao}: NADA")
                else:
                    rotulo_fim = self.novo_rotulo()
                    self.emitir(f"DSVS {rotulo_fim}")
                    self.emitir(f"{rotulo_senao}: NADA")
                    self._gerar_comandos(comando.comandos_senao)
                    self.emitir(f"{rotulo_fim}: NADA")

            #Guarda uma lista de nomes, para cada nome o _buscar descobre o nível 
            #e o deslocamento
            elif isinstance(comando, Leitura):
                for nome in comando.identificadores:
                    simbolo = self._buscar(nome)
                    self.emitir("LEIT")
                    self.emitir(f"ARMZ {simbolo['nivel']},{simbolo['deslocamento']}")

            elif isinstance(comando, Escrita):
                for expressao in comando.expressoes:
                    self._gerar_expressao(expressao)
                    self.emitir("IMPR")

            elif isinstance(comando, Chamada):
                self._gerar_chamada(comando)
            
            elif isinstance(comando, Repeticao):
                rotulo_inicio = self.novo_rotulo()
                rotulo_fim = self.novo_rotulo()
                self.emitir(f"{rotulo_inicio}: NADA")
                self._gerar_expressao(comando.condicao)
                self.emitir(f"DSVF {rotulo_fim}")
                self._gerar_comandos(comando.comandos)
                self.emitir(f"DSVS {rotulo_inicio}")
                self.emitir(f"{rotulo_fim}: NADA")

    def _gerar_chamada(self, chamada):
        for argumento in reversed(chamada.argumentos):
            self._gerar_expressao(argumento)

        rotulo = self.rotulos_funcoes[chamada.nome]
        nivel_atual = 0 if self.funcao_atual is None else 1
        self.emitir(f"CHPR {rotulo},{nivel_atual}")

    def _gerar_funcao(self, funcao):
        simbolo = self.tabela.escopos[0][funcao.nome]
        locais = simbolo["quantidade_locais"]
        self.funcao_atual = funcao.nome

        self.emitir(f"{self.rotulos_funcoes[funcao.nome]}: NADA")
        self.emitir("ENPR 1")

        if locais > 0:
            self.emitir(f"AMEM {locais}")

        self._gerar_comandos(funcao.comandos)

        if locais > 0:
            self.emitir(f"DMEM {locais}")

        self.emitir(f"RTPR {simbolo['quantidade_parametros']}")
        self.funcao_atual = None

    def gerar(self, programa):

        self.codigo = []
        self.contador_rotulos = 0
        self.rotulos_funcoes = {}

        #Inicia
        self.emitir("INPP")

        #reserva espaco apra variaveis globais
        if self.quantidade_globais > 0:
            self.emitir(f"AMEM {self.quantidade_globais}")

        if programa.declaracoes_funcoes:
            rotulo_principal = self.novo_rotulo()

            for funcao in programa.declaracoes_funcoes:
                self.rotulos_funcoes[funcao.nome] = self.novo_rotulo()

            self.emitir(f"DSVS {rotulo_principal}")

            for funcao in programa.declaracoes_funcoes:
                self._gerar_funcao(funcao)

            self.emitir(f"{rotulo_principal}: NADA")

        self._gerar_comandos(programa.comandos)

        #livera espaco apra variaveis globais
        if self.quantidade_globais > 0:
            self.emitir(f"DMEM {self.quantidade_globais}")

        # Finaliza a execução.
        self.emitir("PARA")
        self.emitir("FIM")

        return "\n".join(self.codigo)