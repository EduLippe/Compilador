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
            self.emitir(f"CRVL {simbolo['nivel']}, {simbolo['deslocamento']}")

    def _gerar_comandos(self, comandos):
        for comando in comandos:
            if isinstance(comando, Atribuicao):
                self._gerar_expressao(comando.expressao)
                simbolo = self._buscar(comando.nome)
                self.emitir(f"ARMZ {simbolo['nivel']}, {simbolo['deslocamento']}")

    def gerar(self, programa):

        self.codigo = []
        self.contador_rotulos = 0

        #Inicia
        self.emitir("INPP")

        #reserva espaco apra variaveis globais
        if self.quantidade_globais > 0:
            self.emitir(f"AMEM {self.quantidade_globais}")

        self._gerar_comandos(programa.comandos)

        #livera espaco apra variaveis globais
        if self.quantidade_globais > 0:
            self.emitir(f"DMEM {self.quantidade_globais}")

        # Finaliza a execução.
        self.emitir("PARA")
        self.emitir("FIM")

        return "\n".join(self.codigo)