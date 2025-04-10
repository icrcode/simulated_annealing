# problema 1: achar o ponto mais alto de uma cadeia de montanhas fictícia
# a missão aqui é usar o algoritmo de simulated annealing pra simular um drone explorador
# voando por um terreno cheio de picos e vales, tentando encontrar a melhor vista possível 🏔️🛸

import math
import random
import matplotlib.pyplot as plt
import numpy as np

# essa é a função do terreno
# ela tem vários picos e vales, perfeita pra gente testar o algoritmo
def f(x):
    return math.sin(5 * x) * (1 - math.tanh(x ** 2))

# função de vizinhança
# dado um ponto x, ela gera um novo ponto x' pertinho do original (dentro de um range de -0.1 a 0.1)
def get_neighbor(x):
    delta = random.uniform(-0.1, 0.1)
    x_new = x + delta

    # aqui a gente garante que o novo ponto continua dentro do mapa [-2, 2]
    return min(2, max(-2, x_new))

# o coração da parada: algoritmo de simulated annealing 💓🔥❄️
def simulated_annealing(f, x_start, T0=1.0, alpha=0.95, max_iter=100):
    x = x_start  # ponto inicial escolhido pelo usuário (clique no gráfico)
    T = T0  # temperatura inicial, ou seja, o quanto o drone ainda tá “animado” pra arriscar
    history = [x]  # pra guardar todo o caminho que o drone percorreu

    while T > 1e-3:  # enquanto ainda tiver “calor” pra explorar
        for _ in range(max_iter):
            x_new = get_neighbor(x)  # gera um ponto vizinho
            delta = f(x_new) - f(x)  # compara a altura entre o novo e o atual

            # se for melhor, aceita na hora. se for pior, pode aceitar com uma chance (pra evitar cair num pico qualquer)
            if delta > 0 or random.random() < math.exp(delta / T):
                x = x_new
                history.append(x)

        # agora a temperatura esfria um pouco — o drone vai ficando mais seletivo
        T *= alpha

    return x, history  # retorna o melhor x encontrado e o caminho inteiro

# função que responde ao clique no gráfico
# aqui o usuário escolhe onde o drone começa a busca
def onclick(event):
    if event.xdata is None or event.ydata is None:
        print("clique dentro do gráfico, por favor 🫣")
        return

    x_start = event.xdata
    if x_start < -2 or x_start > 2:
        print("opa! escolhe um ponto dentro do intervalo [-2, 2] 😅")
        return

    print(f"voando a partir de x = {x_start:.4f} 🚁")
    best_x, history = simulated_annealing(f, x_start)

    path_y = [f(x) for x in history]

    # limpa o gráfico anterior e desenha tudo de novo
    plt.cla()
    plt.plot(x_vals, y_vals, label='f(x)', linewidth=2)
    plt.scatter(history, path_y, c='red', s=10, label='caminho do drone')
    plt.title('simulated annealing - busca do ponto mais alto')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)
    plt.draw()

    print(f"🔥 melhor ponto encontrado: x = {best_x:.4f}, f(x) = {f(best_x):.4f}")

# cria os dados do gráfico: pontos de -2 até 2, bem densinho
x_vals = np.linspace(-2, 2, 1000)
y_vals = [f(x) for x in x_vals]

# desenha o gráfico inicial
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x_vals, y_vals, label='f(x)', linewidth=2)
ax.set_title('🖱️ clique em um ponto para começar a busca')
ax.set_xlabel('x')
ax.set_ylabel('f(x)')
ax.grid(True)
ax.set_xlim([-2.2, 2.2])
ax.set_ylim([min(y_vals) - 0.2, max(y_vals) + 0.2])
ax.legend()

# conecta o clique do mouse à função onclick
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
