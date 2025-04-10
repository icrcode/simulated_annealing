import math
import random
import matplotlib.pyplot as plt
import numpy as np

# função que representa o terreno montanhoso
def f(x):
    return math.sin(5 * x) * (1 - math.tanh(x ** 2))

# função de vizinhança (gera um novo ponto pertinho do atual)
def get_neighbor(x):
    delta = random.uniform(-0.1, 0.1)
    x_new = x + delta
    return min(2, max(-2, x_new))  # mantém dentro do domínio [-2, 2]

# algoritmo simulated annealing com debug detalhado
def simulated_annealing(f, x_start, T0=1.0, alpha=0.95, max_iter=100):
    x = x_start
    T = T0
    history = [(x, f(x))]
    best_x = x
    best_fx = f(x)
    step = 1

    print(f"\n🚀 começando busca a partir de x = {x:.4f} com f(x) = {f(x):.4f}\n")

    while T > 1e-3:
        print(f"\n🔥 temperatura atual: T = {T:.5f}")
        for _ in range(max_iter):
            x_new = get_neighbor(x)
            fx = f(x)
            fx_new = f(x_new)
            delta = fx_new - fx

            accept = False
            if delta > 0:
                accept = True
                reason = "melhor ponto 🎯"
            else:
                prob = math.exp(delta / T)
                rand_val = random.random()
                accept = rand_val < prob
                reason = f"pior ponto, mas aceito com probabilidade {prob:.4f} (sorteio = {rand_val:.4f})" if accept else "recusado 😅"

            if accept:
                x = x_new
                history.append((x, fx_new))
                if fx_new > best_fx:
                    best_fx = fx_new
                    best_x = x_new

            print(f"passo {step:03d}: x = {x_new:.4f}, f(x) = {fx_new:.4f}, delta = {delta:.4f} → {reason}")
            step += 1

        T *= alpha

    print(f"\n✅ ponto mais alto encontrado: x = {best_x:.4f}, f(x) = {best_fx:.4f}")
    return best_x, best_fx, history

# função chamada ao clicar no gráfico
def onclick(event):
    if event.xdata is None or event.ydata is None:
        print("⚠️ clique dentro do gráfico, por favor")
        return

    x_start = event.xdata
    if x_start < -2 or x_start > 2:
        print("⚠️ escolha um ponto dentro de [-2, 2]")
        return

    # mostra mensagem de carregamento
    plt.cla()
    ax.plot(x_vals, y_vals, label='f(x)', linewidth=2)
    ax.set_title('🔍 buscando o ponto mais alto...')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.grid(True)
    ax.set_xlim([-2.2, 2.2])
    ax.set_ylim([min(y_vals) - 0.2, max(y_vals) + 0.2])
    plt.pause(0.01)

    # executa o algoritmo
    best_x, best_fx, history = simulated_annealing(f, x_start)

    # separa pontos
    xs, ys = zip(*history)

    # redesenha gráfico com caminho
    plt.cla()
    ax.plot(x_vals, y_vals, label='f(x)', linewidth=2)
    ax.plot(xs, ys, 'ro-', markersize=4, label='caminho do drone')
    ax.scatter(xs[-1], ys[-1], color='gold', edgecolor='black', s=100, label='ponto final ⭐')
    ax.scatter(best_x, best_fx, color='blue', s=120, marker='X', label='ponto mais alto ⛰️')
    ax.text(best_x, best_fx + 0.05, f"x = {best_x:.3f}\nf(x) = {best_fx:.3f}", color='blue', fontsize=9, ha='center')

    ax.set_title('simulated annealing - ponto mais alto encontrado')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.grid(True)
    ax.set_xlim([-2.2, 2.2])
    ax.set_ylim([min(y_vals) - 0.2, max(y_vals) + 0.2])
    ax.legend()
    plt.draw()

# define o domínio da função
x_vals = np.linspace(-2, 2, 1000)
y_vals = [f(x) for x in x_vals]

# mostra gráfico inicial
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x_vals, y_vals, label='f(x)', linewidth=2)
ax.set_title('🖱️ clique onde o drone começa a busca')
ax.set_xlabel('x')
ax.set_ylabel('f(x)')
ax.grid(True)
ax.set_xlim([-2.2, 2.2])
ax.set_ylim([min(y_vals) - 0.2, max(y_vals) + 0.2])
ax.legend()

# conecta clique do mouse ao algoritmo
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
