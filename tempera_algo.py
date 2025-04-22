from random import randint, random
from math import exp
from caixeiro_instance import TSP_instance as TSP
import time
import csv
import os

class TemperaSimulada:
    passo = 1
    melhores = []
    distancias = []
    melhor_estado = None
    t_max = None
    t_min = None
    iter_max = None
    melhor_dist = None
    params_log = None

    def setParams(self, param):
        self.t_max = param['temp_max']
        self.t_min = param['temp_min']
        self.iter_max = param['iter_max']
        self.params_log = param

    # T(t) <- Tmax + (T0-Tmax) * (1 - t/n)²
    def schedule(self):
        return self.t_min + (self.t_max - self.t_min) * (1 - (self.passo / self.iter_max))**2

    def main(self, estado_inicial, dist_total):
        estado_atual = estado_inicial
        distancia_atual = dist_total
        t_atual = self.t_max
        melhot_dist = dist_total
        self.melhor_estado = estado_inicial

        start_time = time.time_ns()
        while(t_atual > self.t_min and t_atual <= self.t_max):
            # next <- a randomly selected successor of current
            estado = TSP.geraEstado(estado_atual)
            dist_estado = TSP.calculaDistancias(estado)

            # deltaE <- value(next) - value(current) - TSP value: distance
            dist_diff = dist_estado - distancia_atual

            try:
                if dist_estado < melhot_dist:
                    melhot_dist, distancia_atual  = [dist_estado, dist_estado]
                    self.melhores.append(melhot_dist)
                    self.melhor_estado = estado.copy()
                    estado_atual = estado.copy()

                # if small random probability, takes a bad choice
                elif random() < exp(-dist_diff / t_atual):
                    distancia_atual = dist_estado
                    estado_atual = estado.copy()
            except:
                print("Error")
                
            t_atual = self.schedule()

            self.distancias.append(distancia_atual)
            self.passo += 1
        end_time = time.time_ns()

        self.melhor_dist = melhot_dist
        file_exists = os.path.isfile('tempera_results.csv')

        with open('tempera_results.csv', mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=';')

            if not file_exists:
                writer.writerow(['melhor_dist', 'T_max', 'T_0', 'N', 'num_pontos', 'execution_time'])

            writer.writerow([self.melhor_dist, self.t_max, self.t_min, self.iter_max, self.params_log["num_pontos"], f"{(end_time - start_time)/1000}"])
