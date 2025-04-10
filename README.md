# Inteligência Artificial

## Prof. Claudinei Dias (Ney)

## Atividade - Simulated Annealing

### Problema 1: Achar o Melhor Ponto de Vista em uma Montanha

Aplicar o algoritmo de Simulated Annealing para encontrar o ponto mais alto (máximo) em um terreno simulado. O terreno é representado por uma função matemática simples, com vários picos e vales. Considere que você é um drone explorador tentando encontrar o ponto mais alto em uma cadeia de montanhas fictícia.

### Orientações

1. **Considere a função abaixo:**
    - O domínio da função é 𝑥 ∈ [−2, 2].
    - Essa função possui vários picos (máximos locais).
    - Seu objetivo é encontrar o ponto mais alto utilizando o algoritmo de Simulated Annealing.

2. **Implemente o algoritmo de Simulated Annealing em Python.**

3. **Defina os seguintes parâmetros:**
    - Temperatura inicial: 𝑇₀ = 1.
    - Taxa de resfriamento: α = 0.
    - Número máximo de iterações por temperatura: 100.

4. **Crie uma função de vizinhança:**
    - Dado um ponto 𝑥, gere 𝑥′ = 𝑥 + 𝜖, onde 𝜖 ∈ [−0.1, 0.1].

5. **Plote os seguintes gráficos:**
    - A função 𝑓(𝑥).
    - O caminho percorrido pelo algoritmo (para visualizar a busca pelo máximo).

### Dicas

- Use `random.uniform(-0.1, 0.1)` para gerar 𝜖.
- Use `math.exp(-delta/T)` para a aceitação probabilística.
- Guarde o histórico dos pontos visitados para plotar depois.

### Raciocínio Intuitivo

Imagine que você está explorando montanhas (função 𝑓) tentando achar o vale mais fundo (mínimo global). No início (alta temperatura), você aceita subir montanhas (soluções piores) porque está animado (com energia). Conforme "esfria" (T diminui), você se torna mais seletivo e só aceita descidas ou pequenas subidas. Assim, você evita cair em mínimos rasos (mínimos locais) e tem chance de achar o melhor caminho até o vale profundo (mínimo global).
