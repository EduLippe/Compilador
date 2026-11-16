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
    
