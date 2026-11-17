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
class GeradorCodigo:
    def __init__(self):
        self.codigo = [] #Guarda instruções geradas
        self.contador_rotulos = 0

#Adiciona instrucao ao codigo gerado ficando na ordem que foram mandadas
    def emitir(self, instrucao):
        self.codigo.append(instrucao)

    def novo_rotulo(self):
        rotulo = f"L{self.contador_rotulos}"
        self.contador_rotulos += 1
        return rotulo
    
    def _buscar(self,nome):
    #Procurea do escopo mais interno para o mais externo
        for escopo in reversed(self.escopos):
            if nome in escopo:
                return escopo[nome]
        return None

#INPP - inicia a primeira linha e prepara a pilha de dados
#PARA - interrompe a execucao
#FIM - Marca o fim
    def gerar(self, programa):
        self.emitir("INPP")
        self.emitir("PARA")
        self.emitir("FIM")
        return "\n".join(self.codigo) # adiciona uma quebra de linha em cada item na lista