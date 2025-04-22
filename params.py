
def mudaParam(paramVal, variacao):
    return min(paramVal + variacao["step"], variacao["max"])
    
def getVariacoesParam(min, max, step):
    return {
        "min": min,
        "max": max,
        "step": step
    }

params = {
    "num_pontos": 10, # numero de pontos gerados na grid
    "temp_max": 10.0,
    "temp_min": 0.001,
    "iter_max": 1000
}

variacoes_parametros = {
    "num_pontos": getVariacoesParam(10, 100, 1), # 90 iterações
    "temp_max":  getVariacoesParam(10.0, 50.0, 0.5), # 80 iterações
    "temp_min": getVariacoesParam(0.001, 0.1, 0.001), # 99 iterações
    "iter_max": getVariacoesParam(1000, 4000, 50) # 70 iterações
}

param_labels = {
    "num_pontos": "Número de cidades",
    "temp_max": "Temperatura máxima",
    "temp_min": "Temperatura mínima",
    "iter_max": "Iteração Final para a Têmpera",
}
