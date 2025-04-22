import matplotlib.pyplot as plt
from params import *
from caixeiro_instance import CaixeiroViajante, TSP_instance
from tempera_algo import TemperaSimulada
import pandas as pd
import numpy as np

def main():
    tempera_params = params.copy()
    i = 1
    melhores = []
    tsp_instance_inicial = TSP_instance.geraInstancia(num_pontos=params['num_pontos'], grid_size=100)
    Tempera = TemperaSimulada()
    for p, v in tempera_params.items():
        x_param = []
        y_param = []
        
        while(tempera_params[p] < variacoes_parametros[p]["max"]):
            tempera_params[p] = mudaParam(tempera_params[p], variacoes_parametros[p])
            if(p == "num_pontos"):
                tsp_instance = TSP_instance.geraInstancia(num_pontos=tempera_params['num_pontos'], grid_size=100)
            else:
                tsp_instance = tsp_instance_inicial
            Tempera.setParams(tempera_params)
            estado_inicial = tsp_instance.estado_inicial_rand
            dist_total = tsp_instance.distancias
            
            Tempera.main(estado_inicial, dist_total)
            x_param.append(tempera_params[p])
            y_param.append(Tempera.melhor_dist)

        tempera_params = params.copy()

        melhores.append(Tempera.melhores[0])

        plt.figure(i)
        if p == "temp_min" or p == "iter_max":
            plt.plot(x_param, y_param, marker='.', linestyle='-', color='b', linewidth=0.5)
        else:
            plt.bar(x_param, y_param, width=0.2)
        plt.xlabel(param_labels[p])
        plt.ylabel('Menor Distância Encontrada')
        plt.title(f"Menor distância encontrada para variações de {param_labels[p]}")

        i += 1

def tempera_unica():
    tempera_params = params.copy()
    tempera_params["num_pontos"] += 10
    tsp_instance = TSP_instance.geraInstancia(num_pontos=tempera_params['num_pontos'], grid_size=100)
    Tempera = TemperaSimulada()
    Tempera.setParams(tempera_params)
    estado_inicial = tsp_instance.estado_inicial_rand
    dist_total = tsp_instance.distancias
    
    Tempera.main(estado_inicial, dist_total)
    
    estado_inicial.append(estado_inicial[0])
    xs, ys = zip(*estado_inicial)
    plt.figure(5)
    plt.subplot(2, 2, 1)
    plt.scatter(xs, ys, color = 'black')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title("Instância da codificação da entrada")

    plt.subplot(2, 2, 2)
    plt.plot(xs, ys)
    plt.scatter(xs, ys, color = 'black')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title("Estado Inicial")
    
    melhor = Tempera.melhor_estado
    melhor.append(melhor[0])
    xb, yb = zip(*melhor)
    plt.subplot(2, 1, 2)
    plt.plot(xb, yb)
    plt.scatter(xb, yb, color = 'black')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title("Melhor estado encontrado")
    plt.subplots_adjust(hspace=0.5)

def plot_csv_graph(csv_file):
    # Load the CSV file
    data = pd.read_csv(csv_file, delimiter=';')

    # Plot execution time vs melhor_dist for each parameter
    parameters = ['T_max', 'T_0', 'N', 'num_pontos']
    labels = {
        'T_max' : "temp. máxima", 'T_0': "temp. mínima", 'N': "max. de iterações", 'num_pontos': "n° de cidades"
    }
    alias = {
        'T_max' : "temp_max", 'T_0': "temp_min", 'N': "iter_max", 'num_pontos': "num_pontos"
    }
    plt.figure()
    i = 1
    for param in parameters:
        plt.subplot(2,2,i)
        plt.scatter(data['execution_time'], data['melhor_dist'], c=data[param], cmap='viridis', edgecolor='k')
        cbar = plt.colorbar(label=labels[param].capitalize())
        cbar.mappable.set_clim(vmin=variacoes_parametros[alias[param]]["min"], vmax=variacoes_parametros[alias[param]]["max"])
        plt.xlabel('Tempo de execução (ms)')
        plt.ylabel('Melhor Distância')

        plt.xticks(ticks=np.linspace(data['execution_time'].min(), data['execution_time'].max(), 10))
        plt.title(f'Tempo de execução vs Melhor Distância (Variando {labels[param]})')
        plt.subplots_adjust(hspace=0.5)
        plt.grid(True)
        i+=1

    plt.show()

if __name__ == "__main__":
    tempera_unica()
    main()
    plot_csv_graph('tempera_results.csv')