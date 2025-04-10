import math
import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# configura estilo geral da plotagem
rcParams.update({
    "font.family": "sans-serif",
    "font.size": 12,
    "axes.edgecolor": "#333",
    "axes.linewidth": 1.2,
    "axes.labelsize": 14,
    "axes.titlesize": 16,
    "legend.frameon": False
})

# função do terreno com picos e vales
def f(x):
    return math.sin(5 * x) * (1 - math.tanh(x ** 2))

# função de vizinhança — gera x' próximo de x
def get_neighbor(x):
    delta = random.uniform(-0.1, 0.1)
    x_new = x + delta
    return min(2, max(-2, x_new))

# algoritmo simulated annealing
def simulated_annealing(f, x_start, T0=1.0, alpha=0.95, max_iter=100):
    x = x_start
    T = T0
    history = [(x, f(x))]
    best_x, best_fx = x, f(x)

    while T > 1e-3:
        for _ in range(max_iter):
            x_new = get_neighbor(x)
            fx, fx_new = f(x), f(x_new)
            delta = fx_new - fx
            if delta > 0 or random.random() < math.exp(delta / T):
                x = x_new
                history.append((x, fx_new))
                if fx_new > best_fx:
                    best_x, best_fx = x_new, fx_new
        T *= alpha
    return best_x, best_fx, history

# função chamada ao clicar
def onclick(event):
    if event.xdata is None:
        print("⛔ clique dentro do gráfico")
        return
    x_start = event.xdata
    if not -2 <= x_start <= 2:
        print("⛔ escolha dentro do intervalo [-2, 2]")
        return

    # carregando...
    ax.cla()
    ax.plot(x_vals, y_vals, color='#004080', linewidth=2.5, zorder=2)
    ax.set_title("🔎 explorando terreno...")
    ax.set_xlim([-2.2, 2.2])
    ax.set_ylim([min(y_vals) - 0.2, max(y_vals) + 0.4])
    ax.grid(True, linestyle='--', alpha=0.3)
    plt.pause(0.01)

    # executa o algoritmo
    best_x, best_fx, history = simulated_annealing(f, x_start)
    xs, ys = zip(*history)

    # redesenha gráfico final
    ax.cla()
    ax.plot(x_vals, y_vals, color='#004080', linewidth=2.5, label='função f(x)', zorder=2)
    ax.plot(xs, ys, color='red', linewidth=1.2, alpha=0.4, zorder=1)
    ax.scatter(xs, ys, color='red', s=12, alpha=0.8, zorder=3, label='pontos visitados')
    ax.scatter(xs[-1], ys[-1], color='gold', edgecolor='black', s=90, zorder=4, label='ponto final ⭐')
    ax.scatter(best_x, best_fx, color='#002288', s=120, marker='X', zorder=5, label='ponto mais alto ⛰️')
    ax.text(best_x, best_fx + 0.08, f"x = {best_x:.3f}\nf(x) = {best_fx:.3f}",
            color='#002288', fontsize=11, ha='center', zorder=6)

    ax.set_title('🧠 simulated annealing: ponto mais alto encontrado')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_xlim([-2.2, 2.2])
    ax.set_ylim([min(y_vals) - 0.2, max(y_vals) + 0.4])
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(loc='upper right')
    plt.draw()

# domínio da função
x_vals = np.linspace(-2, 2, 1000)
y_vals = [f(x) for x in x_vals]

# interface inicial
fig, ax = plt.subplots(figsize=(11, 6))
ax.plot(x_vals, y_vals, color='#004080', linewidth=2.5, label='função f(x)', zorder=2)
ax.set_title('🖱️ clique onde o drone deve começar a busca')
ax.set_xlabel('x')
ax.set_ylabel('f(x)')
ax.set_xlim([-2.2, 2.2])
ax.set_ylim([min(y_vals) - 0.2, max(y_vals) + 0.4])
ax.grid(True, linestyle='--', alpha=0.3)
ax.legend(loc='upper right')

# ativa clique do mouse
fig.canvas.mpl_connect('button_press_event', onclick)
plt.tight_layout()
plt.show()
