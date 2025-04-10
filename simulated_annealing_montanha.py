# esse código resolve o problema 1: encontrar o ponto mais alto (máximo global) de uma cadeia de montanhas fictícia
# representada por uma função matemática com vários picos e vales. a ideia é simular um drone explorador voando
# por esse terreno tentando encontrar o ponto com a melhor vista (o valor máximo da função).
# para isso, usamos o algoritmo de simulated annealing, que tenta fugir de máximos locais aceitando piores soluções
# no começo (quando a "temperatura" está alta) e depois vai ficando mais exigente com o tempo (à medida que a temperatura esfria).
# o algoritmo repete várias tentativas em cada temperatura, explora vizinhos próximos, e guarda os melhores pontos.
# no final, a gente plota o gráfico da função e o caminho que o drone percorreu.

import math
import random
import matplotlib.pyplot as plt
import numpy as np

# função que representa o "terreno" da montanha
# tem vários picos (máximos locais), ideal para esse tipo de busca
def f(x):
    return math.sin(5 * x) * (1 - math.tanh(x ** 2))

# função que gera um ponto vizinho
# ela recebe um x atual e retorna um novo x que está até 0.1 de distância
def get_neighbor(x):
    delta = random.uniform(-0.1, 0.1)
    x_new = x + delta

    # garante que o novo x fique dentro do domínio permitido [-2, 2]
    return min(2, max(-2, x_new))

# aqui é o coração do algoritmo simulated annealing
def simulated_annealing(f, x_start, T0=1.0, alpha=0.95, max_iter=100):
    x = x_start  # ponto inicial aleatório
    T = T0  # temperatura inicial
    history = [x]  # lista para guardar os pontos visitados

    # continua enquanto a temperatura for maior que um limite mínimo (esfriou o suficiente)
    while T > 1e-3:
        for _ in range(max_iter):
            x_new = get_neighbor(x)  # gera vizinho
            delta = f(x_new) - f(x)  # diferença entre o valor novo e o atual

            # se o novo for melhor, aceita. se for pior, aceita com uma certa probabilidade
            if delta > 0 or random.random() < math.exp(delta / T):
                x = x_new
                history.append(x)  # guarda o ponto aceito

        # resfria a temperatura
        T *= alpha

    return x, history  # retorna o melhor x encontrado e o caminho feito

# executa o algoritmo
x_start = random.uniform(-2, 2)  # começa em um ponto aleatório dentro do domínio
best_x, history = simulated_annealing(f, x_start)

# cria os dados para desenhar o gráfico da função
x_vals = np.linspace(-2, 2, 1000)
y_vals = [f(x) for x in x_vals]

# pega os valores de f(x) do caminho percorrido
path_y = [f(x) for x in history]

# desenha o gráfico
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, label='f(x)', linewidth=2)  # linha azul da função
plt.scatter(history, path_y, c='red', s=10, label='caminho do algoritmo')  # pontos vermelhos do caminho
plt.title('simulated annealing - busca do ponto mais alto')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True)
plt.show()

# imprime o melhor ponto encontrado
print(f"melhor ponto encontrado: x = {best_x:.4f}, f(x) = {f(best_x):.4f}")