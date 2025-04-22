from math import dist
from numpy import random
from random import randint

class CaixeiroViajante:
    estado_inicial_rand = None
    distancias = None

    # Gera n pontos aleatórios em uma grid de tamanho grid_size
    # - UMA INSTANCIA CODIFICAÇÃO DA ENTRADA
    def geraPontos(self, n, grid_size):
        return [((randint(0, grid_size), randint(0, grid_size))) for _ in range (n)] 

    # Gera um estado aleatório a partir do estado atual
    def geraEstado(self, estado_base):
        i, j = random.choice(len(estado_base), 2, replace=False)
        estado = estado_base.copy()
        estado[i], estado[j] = estado[j], estado[i]
        return estado

    # Calcula distâncias entre vertices adjacentes no array de um estado
    def calculaDistancias(self, estado):
        total = dist(estado[0], estado[-1])
        for i in range (len(estado) - 1):
            total += dist(estado[i], estado[i + 1])
        
        return total
    
    # Gera instância e calcula distancias para a instância gerada
    def geraInstancia(self, num_pontos, grid_size):
        self.estado_inicial_rand = self.geraPontos(num_pontos, grid_size)
        self.distancias = self.calculaDistancias(self.estado_inicial_rand)
        return self
    
TSP_instance = CaixeiroViajante()