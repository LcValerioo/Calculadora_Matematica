# 🧮 Calculadora Matemática

Uma aplicação desenvolvida em Python para resolução numérica de equações não lineares, com métodos iterativos, análise de convergência, histórico de aproximações e visualização gráfica de funções.

O projeto foi desenvolvido como parte dos estudos de **Modelagem Matemática**, com o objetivo de aplicar conceitos de métodos numéricos e construir uma ferramenta capaz de resolver problemas matemáticos de maneira interativa e didática.

---

## 📌 Sobre o projeto

A Calculadora Matemática permite que o usuário informe uma função matemática, defina parâmetros de precisão e selecione um método numérico para aproximar suas raízes.

Durante a execução, a aplicação realiza os cálculos iterativos, acompanha os critérios de convergência, registra o histórico das aproximações e apresenta os resultados obtidos.

Além dos resultados numéricos, o projeto também utiliza recursos gráficos para facilitar a interpretação do comportamento das funções.

## ⚙️ Funcionalidades implementadas

### Métodos numéricos

Atualmente, a aplicação conta com cinco métodos para resolução de equações não lineares:

| Método | Descrição |
|---|---|
| Regula Falsi | Método da falsa posição, baseado em um intervalo com mudança de sinal. |
| Bisseção | Método de subdivisão sucessiva do intervalo para aproximação da raiz. |
| Newton-Raphson | Método iterativo que utiliza a derivada da função. |
| Illinois | Variante da Regula Falsi que ajusta os pesos dos extremos para melhorar a convergência. |
| Secante | Método que utiliza duas aproximações anteriores para estimar a próxima aproximação, sem calcular explicitamente a derivada. |

### Análise numérica

- Entrada interativa de funções matemáticas.
- Definição da tolerância desejada.
- Configuração do número máximo de iterações.
- Registro do histórico de aproximações.
- Cálculo dos erros absoluto da função e da aproximação.
- Verificação dos critérios de convergência.
- Tratamento de situações como divisão por zero, valores não finitos, derivadas próximas de zero e estagnação numérica.
- Mensagens informativas sobre o resultado da execução.

### Visualização gráfica

- Plotagem de funções matemáticas.
- Visualização dos resultados dos métodos numéricos.
- Exibição dos gráficos em uma janela separada.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal do projeto. |
| SymPy | Manipulação simbólica e cálculo de derivadas. |
| Matplotlib | Construção e exibição dos gráficos. |
| Math | Operações e funções matemáticas. |

## 📦 Requisitos

Para executar o projeto, é necessário ter:

- Python 3 instalado.
- pip para instalação de dependências.
- Um editor ou ambiente de desenvolvimento Python, como Visual Studio Code.

### Instalação das dependências

No terminal, execute:

```bash
pip install sympy matplotlib
```

## ▶️ Como executar

1. Clone este repositório:

```bash
gh repo clone LcValerioo/Calculadora_Matematica
```

2. Acesse a pasta do projeto:

```bash
cd github.com/LcValerioo/Calculadora_Matematica
```

3. Instale as dependências:

```bash
pip install sympy matplotlib
```

4. Execute o arquivo principal:

```bash
python calculadora_matematica.py
```

---

## 🧪 Exemplo de utilização

Considere a função:

\[
f(x)=x^2-2
\]

O objetivo é encontrar uma aproximação para sua raiz positiva.

Parâmetros utilizados:

```text
Função: x**2 - 2
Tolerância: 0.000001
Número máximo de iterações: 100
Método: Secante
Aproximação inicial x0: 1
Aproximação inicial x1: 2
```

Resultado obtido:

```text
Resultado: Convergência alcançada pelos dois critérios.

Raiz aproximada: 1.4142135624
f(raiz): 8.881784197001e-16
Iterações realizadas: 6
```

A raiz encontrada é uma aproximação de:

\[
\sqrt{2}\approx 1.414213562373095
\]

O exemplo demonstra a capacidade da aplicação de aproximar numericamente uma raiz com elevada precisão.

---

## 📊 Critérios de convergência

Os métodos iterativos utilizam critérios numéricos para determinar quando uma aproximação pode ser considerada suficientemente precisa.

Entre os critérios utilizados estão:

**Erro da função:**

\[
E_f=|f(x_n)|
\]

**Erro entre aproximações consecutivas:**

\[
E_x=|x_n-x_{n-1}|
\]

Nas implementações que utilizam os dois critérios, a convergência é reconhecida quando ambos são inferiores à tolerância estabelecida:

\[
E_f<\varepsilon
\]

\[
E_x<\varepsilon
\]

Essa abordagem permite avaliar tanto a proximidade da aproximação em relação à raiz quanto a estabilidade entre iterações sucessivas.

**Observação:** métodos numéricos não garantem convergência para qualquer função ou escolha de parâmetros. O comportamento depende das características matemáticas do problema e das aproximações iniciais.

---

## 🗺️ Roadmap de desenvolvimento

O desenvolvimento foi organizado em quatro etapas principais.

### Etapa 1 — Métodos numéricos

- [x] Regula Falsi
- [x] Bisseção
- [x] Newton-Raphson
- [x] Illinois
- [x] Secante

### Etapa 2 — Visualização matemática

- [x] Gráficos de funções
- [x] Exibição gráfica em janela separada
- [ ] Identificação visual das raízes
- [ ] Marcação dos intervalos e aproximações iniciais
- [x] Histórico das iterações
- [ ] Aprimoramento da apresentação visual dos históricos

### Etapa 3 — Cálculo II

- [ ] Cálculo de limites
- [ ] Cálculo de derivadas
- [ ] Integrais definidas
- [ ] Integrais indefinidas
- [ ] Aplicações de integrais

### Etapa 4 — Interface gráfica

- [ ] Menu de navegação
- [ ] Entrada de funções
- [ ] Seleção dos métodos
- [ ] Apresentação organizada dos resultados
- [ ] Desenvolvimento de interface gráfica interativa

---

## 🎯 Objetivos acadêmicos e técnicos

Além da construção de uma ferramenta funcional, o projeto busca consolidar conhecimentos relacionados a:

- Métodos numéricos e análise de convergência.
- Cálculo diferencial e integral.
- Manipulação de expressões matemáticas.
- Programação estruturada em Python.
- Tratamento de exceções e validação de dados.
- Visualização e interpretação de resultados matemáticos.

## 👨‍💻 Autor

**Lucas Valério**

Estudante de Ciência da Computação.

GitHub: [@LcValerioo](https://github.com/LcValerioo)

---

*Projeto acadêmico em desenvolvimento — Modelagem Matemática.*
