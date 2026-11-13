import math
import matplotlib.pyplot as plt
import sympy as sp

# ==========================================
# 1. INTERPRETADOR DA FUNCAO
# ==========================================

def criar_funcao(expressao):

    codigo = compile(expressao, "<funcao>", "eval")

    ambiente = {
        nome: getattr(math, nome)
        for nome in dir(math)
        if not nome.startswith("_")
    }

    def f(x):
        resultado = eval(
            codigo,
            {"__builtins__": {}},
            {**ambiente, "x": x}
        )

        return float(resultado)

    return f


# ==========================================
# 2. METODO DA REGULA FALSI
# ==========================================



def regula_falsi(f, a, b, tol, max_iter):

    historico = []

    # ======================================
    # 1. VALIDACAO DOS PARAMETROS
    # ======================================

    try:
        a = float(a)
        b = float(b)
        tol = float(tol)
        max_iter = int(max_iter)

    except (ValueError, TypeError, OverflowError):
        return None, historico, "Parâmetros informados são inválidos."

    if not math.isfinite(a) or not math.isfinite(b):
        return None, historico, "Os limites precisam ser números finitos."

    if a >= b:
        return None, historico, "O limite inferior deve ser menor que o superior."

    if not math.isfinite(tol) or tol <= 0:
        return None, historico, "A tolerância precisa ser positiva e finita."

    if max_iter <= 0:
        return None, historico, "O número máximo de iterações precisa ser positivo."

    if not math.isfinite(b - a):
        return None, historico, "A largura do intervalo é numericamente inválida."

    # ======================================
    # 2. AVALIACAO DOS EXTREMOS
    # ======================================

    try:
        fa = float(f(a))
        fb = float(f(b))

    except (ValueError, TypeError, ZeroDivisionError, OverflowError):
        return None, historico, "Erro matemático ao avaliar os extremos."

    if not math.isfinite(fa) or not math.isfinite(fb):
        return None, historico, "A função produziu valores inválidos nos extremos."

    if fa == 0:
        return a, historico, "Raiz exata encontrada em a."

    if fb == 0:
        return b, historico, "Raiz exata encontrada em b."

    # Verifica mudança de sinal sem multiplicar os valores
    sinais_opostos = (fa < 0 < fb) or (fb < 0 < fa)

    if not sinais_opostos:
        return None, historico, "O intervalo não possui mudança de sinal."

    # ======================================
    # 3. CONTROLE DE ESTAGNACAO
    # ======================================

    z_anterior = None
    extremo_parado = None
    repeticoes_extremo = 0

    # ======================================
    # 4. PROCESSO ITERATIVO
    # ======================================

    for i in range(1, max_iter + 1):

        # Calcula a posição relativa usando valores escalados.
        # Isso evita multiplicações e somas desnecessariamente grandes.

        escala = max(abs(fa), abs(fb))

        peso_a = abs(fa) / escala
        peso_b = abs(fb) / escala

        proporcao = peso_a / (peso_a + peso_b)

        a_iter = a
        b_iter = b

        z = a + (b - a) * proporcao

        # Verifica se a aproximação está dentro do intervalo
        if z == a or z == b:
            return (
                z_anterior if z_anterior is not None else z,
                historico,
                "Estagnação numérica: a aproximação atingiu um extremo do intervalo."
            )

        # Avalia a função
        try:
            fz = float(f(z))

        except (ValueError, TypeError, ZeroDivisionError, OverflowError):
            return None, historico, "Erro matemático ao avaliar a aproximação."

        if not math.isfinite(fz):
            return None, historico, "A função produziu um valor inválido na aproximação."

        # Verifica raiz exata
        if fz == 0:

            historico.append({
                "iteracao": i,
                "a": a_iter,
                "b": b_iter,
                "z": z,
                "fz": fz,
                "erro_f": 0.0,
                "erro_x": 0.0,
                "extremo_parado": extremo_parado,
                "repeticoes_extremo": repeticoes_extremo
            })

            return z, historico, "Raiz exata encontrada."

        # Calcula os erros
        erro_f = abs(fz)

        if z_anterior is None:
            erro_x = None
        else:
            erro_x = abs(z - z_anterior)

        # Atualiza o intervalo preservando a mudança de sinal
        if (fa < 0 < fz) or (fz < 0 < fa):

            # O extremo a permanece fixo
            extremo_atual = "a"

            b = z
            fb = fz

        else:

            # O extremo b permanece fixo
            extremo_atual = "b"

            a = z
            fa = fz

        # Monitora quantas vezes o mesmo extremo permaneceu fixo
        if extremo_atual == extremo_parado:
            repeticoes_extremo += 1
        else:
            extremo_parado = extremo_atual
            repeticoes_extremo = 1

        # Registra o histórico
        historico.append({
            "iteracao": i,
            "a": a_iter,
            "b": b_iter,
            "z": z,
            "fz": fz,
            "erro_f": erro_f,
            "erro_x": erro_x,
            "extremo_parado": extremo_parado,
            "repeticoes_extremo": repeticoes_extremo
        })

        # Critérios de convergência
        criterio_f = erro_f < tol

        criterio_x = (
            erro_x is not None and erro_x < tol
        )

        if criterio_f and criterio_x:
            return (
                z,
                historico,
                "Convergência alcançada pelos dois critérios."
            )

        # Atualiza a aproximação anterior
        z_anterior = z

    # ======================================
    # 5. LIMITE DE ITERACOES
    # ======================================

    if repeticoes_extremo >= 5:

        mensagem = (
            "Limite máximo de iterações alcançado. "
            f"O extremo {extremo_parado} permaneceu fixo "
            f"por {repeticoes_extremo} iterações consecutivas."
        )

    else:
        mensagem = "Limite máximo de iterações alcançado sem convergência."

    return z, historico, mensagem


#===========================================
# 3. METODO DE ILLINOIS
#===========================================


def metodo_illinois(f, a, b, tol, max_iter):

    historico = []

    # 1. Validação dos parâmetros
    try:
        a = float(a)
        b = float(b)
        tol = float(tol)
        max_iter = int(max_iter)
    except (ValueError, TypeError, OverflowError):
        return None, historico, "Parâmetros informados são inválidos."

    if not math.isfinite(a) or not math.isfinite(b):
        return None, historico, "Os limites precisam ser números finitos."

    if a >= b:
        return None, historico, "O limite inferior deve ser menor que o superior."

    if not math.isfinite(tol) or tol <= 0:
        return None, historico, "A tolerância precisa ser positiva e finita."

    if max_iter <= 0:
        return None, historico, "O número máximo de iterações precisa ser positivo."

    if not math.isfinite(b - a):
        return None, historico, "A largura do intervalo é numericamente inválida."

    # 2. Avaliação dos extremos
    try:
        fa = float(f(a))
        fb = float(f(b))
    except (ValueError, TypeError, ZeroDivisionError, OverflowError):
        return None, historico, "Erro matemático ao avaliar os extremos."

    if not math.isfinite(fa) or not math.isfinite(fb):
        return None, historico, "A função produziu valores inválidos nos extremos."

    if fa == 0:
        return a, historico, "Raiz exata encontrada em a."

    if fb == 0:
        return b, historico, "Raiz exata encontrada em b."

    if not ((fa < 0 < fb) or (fb < 0 < fa)):
        return None, historico, "O intervalo não possui mudança de sinal."

    # 3. Pesos iniciais
    peso_a = fa
    peso_b = fb

    extremo_retido_anterior = None
    z_anterior = None

    # 4. Iterações do método de Illinois
    for i in range(1, max_iter + 1):

        a_iter = a
        b_iter = b

        # Guarda os pesos utilizados nesta iteração
        peso_a_usado = peso_a
        peso_b_usado = peso_b

        escala = max(abs(peso_a), abs(peso_b))

        if escala == 0:
            return None, historico, "Os pesos numéricos foram reduzidos a zero."

        peso_a_normalizado = abs(peso_a) / escala
        peso_b_normalizado = abs(peso_b) / escala

        proporcao = (
            peso_a_normalizado /
            (peso_a_normalizado + peso_b_normalizado)
        )

        z = a + (b - a) * proporcao

        if z == a or z == b:
            raiz = z_anterior if z_anterior is not None else z
            return raiz, historico, "Estagnação numérica: a aproximação atingiu um extremo do intervalo."

        # Avaliação da nova aproximação
        try:
            fz = float(f(z))
        except (ValueError, TypeError, ZeroDivisionError, OverflowError):
            return None, historico, "Erro matemático ao avaliar a aproximação."

        if not math.isfinite(fz):
            return None, historico, "A função produziu um valor inválido na aproximação."

        erro_f = abs(fz)
        erro_x = None if z_anterior is None else abs(z - z_anterior)

        if fz == 0:
            historico.append({
                "iteracao": i,
                "a": a_iter,
                "b": b_iter,
                "z": z,
                "fz": fz,
                "erro_f": 0.0,
                "erro_x": 0.0,
                "extremo_retido": None,
                "peso_a_usado": peso_a_usado,
                "peso_b_usado": peso_b_usado,
                "peso_a_proximo": peso_a,
                "peso_b_proximo": peso_b,
                "peso_reduzido": False
        })

            return z, historico, "Raiz exata encontrada."


        # 5. Atualização do intervalo
        if (fa < 0 < fz) or (fz < 0 < fa):

            # O extremo a permanece fixo
            b = z
            fb = fz
            peso_b = fb
            extremo_retido = "a"

        else:

            # O extremo b permanece fixo
            a = z
            fa = fz
            peso_a = fa
            extremo_retido = "b"

        # 6. Correção de Illinois
        peso_reduzido = False

        if extremo_retido == extremo_retido_anterior:

            if extremo_retido == "a":
                peso_a *= 0.5
            else:
                peso_b *= 0.5

            peso_reduzido = True

        else:
            # Restaura os pesos reais quando muda o extremo retido
            peso_a = fa
            peso_b = fb

        historico.append({
            "iteracao": i,
            "a": a_iter,
            "b": b_iter,
            "z": z,
            "fz": fz,
            "erro_f": erro_f,
            "erro_x": erro_x,
            "extremo_retido": extremo_retido,

            # Pesos utilizados para calcular z
            "peso_a_usado": peso_a_usado,
            "peso_b_usado": peso_b_usado,

            # Pesos preparados para a próxima iteração
            "peso_a_proximo": peso_a,
            "peso_b_proximo": peso_b,

            "peso_reduzido": peso_reduzido
        })

        # 7. Critérios de convergência
        criterio_f = erro_f < tol
        criterio_x = erro_x is not None and erro_x < tol

        if criterio_f and criterio_x:
            return z, historico, "Convergência alcançada pelos dois critérios."

        extremo_retido_anterior = extremo_retido
        z_anterior = z

    return z, historico, "Limite máximo de iterações alcançado sem convergência."

# ==========================================
# 4. METODO DA SECANTE
# ==========================================

def secante(f, x0, x1, tol, max_iter):

    historico = []

    # 1. Validação dos parâmetros
    try:
        x0 = float(x0)
        x1 = float(x1)
        tol = float(tol)
        max_iter = int(max_iter)

    except (ValueError, TypeError, OverflowError):
        return None, historico, "Parâmetros informados são inválidos."

    if not math.isfinite(x0) or not math.isfinite(x1):
        return None, historico, "As aproximações precisam ser números finitos."

    if x0 == x1:
        return None, historico, "As aproximações iniciais precisam ser diferentes."

    if not math.isfinite(tol) or tol <= 0:
        return None, historico, "A tolerância precisa ser positiva e finita."

    if max_iter <= 0:
        return None, historico, "O número máximo de iterações precisa ser positivo."

    # 2. Avaliação das aproximações iniciais
    try:
        fx0 = float(f(x0))
        fx1 = float(f(x1))

    except (ValueError, TypeError, ZeroDivisionError, OverflowError):
        return None, historico, "Erro matemático ao avaliar as aproximações iniciais."

    if not math.isfinite(fx0) or not math.isfinite(fx1):
        return None, historico, "A função produziu valores inválidos."

    if fx0 == 0:
        return x0, historico, "Raiz exata encontrada na primeira aproximação."

    if fx1 == 0:
        return x1, historico, "Raiz exata encontrada na segunda aproximação."

    # 3. Iterações do método da Secante
    limite_denominador = 1e-15

    for i in range(1, max_iter + 1):

        denominador = fx1 - fx0
        escala = max(abs(fx0), abs(fx1))

        if escala == 0 or abs(denominador) <= limite_denominador * escala:
            return None, historico, "Denominador nulo ou numericamente muito próximo de zero."

        # Cálculo da próxima aproximação
        try:
            razao = (fx1 / denominador) * (x1 - x0)
            x2 = x1 - razao

        except (ValueError, TypeError, ZeroDivisionError, OverflowError):
            return None, historico, "Não foi possível calcular a próxima aproximação."

        if not math.isfinite(x2):
            return None, historico, "A próxima aproximação gerou um valor inválido."

        # Avaliação da nova aproximação
        try:
            fx2 = float(f(x2))

        except (ValueError, TypeError, ZeroDivisionError, OverflowError):
            return None, historico, "Erro matemático ao avaliar a nova aproximação."

        if not math.isfinite(fx2):
            return None, historico, "A função produziu um valor inválido na nova aproximação."

        # 4. Cálculo dos erros
        erro_f = abs(fx2)
        erro_x = abs(x2 - x1)

        # 5. Registro do histórico
        historico.append({
            "iteracao": i,
            "x0": x0,
            "x1": x1,
            "x2": x2,
            "fx0": fx0,
            "fx1": fx1,
            "fx2": fx2,
            "erro_f": erro_f,
            "erro_x": erro_x
        })

        # 6. Critérios de convergência
        criterio_f = erro_f < tol
        criterio_x = erro_x < tol

        if criterio_f and criterio_x:
            return x2, historico, "Convergência alcançada pelos dois critérios."

        # 7. Detecção de estagnação numérica
        if x2 == x1:
            return x2, historico, "Estagnação numérica: a aproximação não apresentou mudança."

        # 8. Atualização das aproximações
        x0 = x1
        fx0 = fx1

        x1 = x2
        fx1 = fx2

    return x1, historico, "Limite máximo de iterações alcançado sem convergência."


# ==========================================
# 5. METODO DA BISSECAO
# ==========================================


def bissecao(f, a, b, tol, max_iter):

    historico = []

    # ======================================
    # 1. VALIDACAO DOS PARAMETROS
    # ======================================

    try:
        a = float(a)
        b = float(b)
        tol = float(tol)
        max_iter = int(max_iter)

    except (ValueError, TypeError, OverflowError):
        return None, historico, "Parâmetros informados são inválidos."

    if not math.isfinite(a) or not math.isfinite(b):
        return None, historico, "Os limites precisam ser números finitos."

    if a >= b:
        return None, historico, "O limite inferior deve ser menor que o superior."

    if not math.isfinite(tol) or tol <= 0:
        return None, historico, "A tolerância precisa ser positiva e finita."

    if max_iter <= 0:
        return None, historico, "O número máximo de iterações precisa ser positivo."

    if not math.isfinite(b - a):
        return None, historico, "A largura do intervalo é numericamente inválida."

    # ======================================
    # 2. AVALIACAO DOS EXTREMOS
    # ======================================

    try:
        fa = float(f(a))
        fb = float(f(b))

    except (ValueError, TypeError, ZeroDivisionError, OverflowError):
        return None, historico, "Erro matemático ao avaliar os extremos."

    if not math.isfinite(fa) or not math.isfinite(fb):
        return None, historico, "A função produziu valores inválidos nos extremos."

    # Verifica raízes exatas nos extremos
    if fa == 0:
        return a, historico, "Raiz exata encontrada em a."

    if fb == 0:
        return b, historico, "Raiz exata encontrada em b."

    # Verifica mudança de sinal sem multiplicar os valores
    sinais_opostos = (fa < 0 < fb) or (fb < 0 < fa)

    if not sinais_opostos:
        return None, historico, "O intervalo não possui mudança de sinal."

    # ======================================
    # 3. PROCESSO ITERATIVO
    # ======================================

    for i in range(1, max_iter + 1):

        # Calcula o ponto médio
        z = a + (b - a) / 2

        # Detecta estagnação numérica
        if z == a or z == b:
            return (
                z,
                historico,
                "Estagnação numérica: não foi possível dividir mais o intervalo."
            )

        # Avalia a função no ponto médio
        try:
            fz = float(f(z))

        except (ValueError, TypeError, ZeroDivisionError, OverflowError):
            return None, historico, "Erro matemático ao avaliar o ponto médio."

        if not math.isfinite(fz):
            return None, historico, "A função produziu um valor inválido no ponto médio."

        # Verifica raiz exata
        if fz == 0:

            historico.append({
                "iteracao": i,
                "a": a,
                "b": b,
                "z": z,
                "fz": fz,
                "erro_f": 0.0,
                "erro_x": 0.0
            })

            return z, historico, "Raiz exata encontrada."

        # Erro limitado pela metade da largura do intervalo atual
        erro_x = (b - a) / 2

        # Resíduo da função
        erro_f = abs(fz)

        # Registra a iteração
        historico.append({
            "iteracao": i,
            "a": a,
            "b": b,
            "z": z,
            "fz": fz,
            "erro_f": erro_f,
            "erro_x": erro_x
        })

        # Verifica os critérios de convergência
        criterio_f = erro_f < tol
        criterio_x = erro_x < tol

        if criterio_f and criterio_x:
            return (
                z,
                historico,
                "Convergência alcançada pelos dois critérios."
            )

        # Atualiza o intervalo preservando a mudança de sinal
        if (fa < 0 < fz) or (fz < 0 < fa):
            b = z
            fb = fz

        else:
            a = z
            fa = fz

    # ======================================
    # 4. LIMITE DE ITERACOES
    # ======================================

    return (
        z,
        historico,
        "Limite máximo de iterações alcançado sem convergência."
    )




# ==========================================
# 6. METODO NEWTON-RAPHSON
# ==========================================


def newton_raphson(expressao, x0, tol, max_iter):

    # Preparação da função e da derivada
    x = sp.Symbol("x")

    try:
        funcao_simbolica = sp.sympify(expressao)
        derivada_simbolica = sp.diff(funcao_simbolica, x)

        f = sp.lambdify(x, funcao_simbolica, modules="math")
        df = sp.lambdify(x, derivada_simbolica, modules="math")

    except (sp.SympifyError, TypeError, ValueError, SyntaxError) as erro:
        return None, [], f"Erro ao interpretar a função: {erro}"

    # Validação dos parâmetros
    try:
        x0 = float(x0)
        tol = float(tol)
        max_iter = int(max_iter)

    except (ValueError, TypeError, OverflowError):
        return None, [], "Os parâmetros informados são inválidos."

    if not math.isfinite(x0):
        return None, [], "A aproximação inicial precisa ser um número finito."

    if not math.isfinite(tol) or tol <= 0:
        return None, [], "A tolerância precisa ser positiva e finita."

    if max_iter <= 0:
        return None, [], "O número máximo de iterações precisa ser positivo."

    historico = []
    aproximacoes_visitadas = [x0]

    # Limite para identificar derivadas muito pequenas
    limite_derivada = 1e-12

    for i in range(1, max_iter + 1):

        # Avaliação da função e da derivada
        try:
            fx = float(f(x0))
            dfx = float(df(x0))

        except (ValueError, TypeError, ZeroDivisionError, OverflowError):
            return None, historico, "Erro matemático ao avaliar a função ou derivada."

        # Verificação de valores inválidos
        if not math.isfinite(fx) or not math.isfinite(dfx):
            return None, historico, "A função ou derivada produziu um valor inválido."

        # Verifica se a aproximação atual já é uma raiz exata
        if fx == 0:
            return x0, historico, "A aproximação atual já é uma raiz exata."

        # Verifica se a derivada é muito pequena
        if abs(dfx) <= limite_derivada:
            return None, historico, "Derivada nula ou muito próxima de zero. Método interrompido."

        # Calcula a próxima aproximação
        try:
            x1 = x0 - (fx / dfx)

        except (ZeroDivisionError, OverflowError):
            return None, historico, "Não foi possível calcular a próxima aproximação."

        if not math.isfinite(x1):
            return None, historico, "A próxima aproximação gerou um valor inválido."

        # Avalia a função na nova aproximação
        try:
            fx1 = float(f(x1))

        except (ValueError, TypeError, ZeroDivisionError, OverflowError):
            return None, historico, "Erro matemático ao avaliar a nova aproximação."

        if not math.isfinite(fx1):
            return None, historico, "A nova aproximação produziu um resultado inválido."

        # Calcula os erros
        erro_f = abs(fx1)
        erro_x = abs(x1 - x0)

        # Registra a iteração
        historico.append({
            "iteracao": i,
            "x_atual": x0,
            "derivada": dfx,
            "x_proximo": x1,
            "f_x_proximo": fx1,
            "erro_f": erro_f,
            "erro_x": erro_x
        })

        # Verifica os critérios de convergência
        criterio_f = erro_f < tol
        criterio_x = erro_x < tol

        if criterio_f and criterio_x:
            return x1, historico, "Convergência alcançada pelos dois critérios."

        # Verifica se a aproximação está se repetindo
        for valor_anterior in aproximacoes_visitadas:

            if math.isclose(
                x1,
                valor_anterior,
                rel_tol=1e-12,
                abs_tol=1e-12
            ):
                return (
                    x1,
                    historico,
                    "Ciclo detectado: o método está repetindo aproximações."
                )

        # Armazena a nova aproximação
        aproximacoes_visitadas.append(x1)

        # Atualiza a aproximação
        x0 = x1

    return x0, historico, "Limite máximo de iterações alcançado sem convergência."


# ==========================================
# 7. EXIBICAO DO HISTORICO
# ==========================================


def mostrar_historico(historico):

    print("\n" + "=" * 100)
    print("                         HISTORICO DE ITERACOES")
    print("=" * 100)

    print(
        f"{'Iter.':<7}"
        f"{'a':<13}"
        f"{'b':<13}"
        f"{'z':<15}"
        f"{'f(z)':<17}"
        f"{'Erro f':<17}"
        f"{'Erro x':<17}"
    )

    print("-" * 100)

    for item in historico:

        erro_x = (
            f"{item['erro_x']:.8e}"
            if item["erro_x"] is not None
            else "---"
        )

        print(
            f"{item['iteracao']:<7}"
            f"{item['a']:<13.6f}"
            f"{item['b']:<13.6f}"
            f"{item['z']:<15.8f}"
            f"{item['fz']:<17.8e}"
            f"{item['erro_f']:<17.8e}"
            f"{erro_x:<17}"
        )

    print("=" * 100)


def mostrar_historico_newton(historico):

    print("\n" + "=" * 115)
    print("             HISTORICO DE ITERACOES - NEWTON-RAPHSON")
    print("=" * 115)

    print(
        f"{'Iter.':<7}"
        f"{'x atual':<15}"
        f"{"f'(x atual)":<15}"
        f"{'x proximo':<17}"
        f"{'f(x proximo)':<17}"
        f"{'Erro f':<17}"
        f"{'Erro x':<17}"
    )

    print("-" * 115)

    for item in historico:
        print(
            f"{item['iteracao']:<7}"
            f"{item['x_atual']:<15.8f}"
            f"{item['derivada']:<15.8f}"
            f"{item['x_proximo']:<17.8f}"
            f"{item['f_x_proximo']:<17.8e}"
            f"{item['erro_f']:<17.8e}"
            f"{item['erro_x']:<17.8e}"
        )

    print("=" * 115)


def mostrar_historico_illinois(historico):

    print("\n" + "=" * 145)
    print("                         HISTÓRICO DE ITERAÇÕES - MÉTODO DE ILLINOIS")
    print("=" * 145)

    print(
        f"{'Iter':<5}"
        f"{'a':<13}"
        f"{'b':<13}"
        f"{'z':<15}"
        f"{'f(z)':<15}"
        f"{'Erro f':<13}"
        f"{'Erro x':<13}"
        f"{'Retido':<10}"
        f"{'Peso reduzido':<15}"
    )

    print("-" * 145)

    for item in historico:

        erro_x = item["erro_x"]

        if erro_x is None:
            erro_x = "-"
        else:
            erro_x = f"{erro_x:.6e}"
        retido = item["extremo_retido"] or "-"

        reduzido = "Sim" if item["peso_reduzido"] else "Não"

        print(
            f"{item['iteracao']:<5}"
            f"{item['a']:<13.7f}"
            f"{item['b']:<13.7f}"
            f"{item['z']:<15.9f}"
            f"{item['fz']:<15.6e}"
            f"{item['erro_f']:<13.6e}"
            f"{str(erro_x):<13}"
            f"{retido:<10}"
            f"{reduzido:<15}"
        )

    print("-" * 145)

    print("\nPESOS UTILIZADOS E PREPARADOS PARA A PRÓXIMA ITERAÇÃO:")
    print("-" * 100)

    print(
        f"{'Iter':<8}"
        f"{'Peso A usado':<20}"
        f"{'Peso B usado':<20}"
        f"{'Peso A próximo':<25}"
        f"{'Peso B próximo':<25}"
    )

    print("-" * 100)

    for item in historico:

        print(
            f"{item['iteracao']:<8}"
            f"{item['peso_a_usado']:<20.8e}"
            f"{item['peso_b_usado']:<20.8e}"
            f"{item['peso_a_proximo']:<25.8e}"
            f"{item['peso_b_proximo']:<25.8e}"
        )

    print("-" * 100)


def mostrar_historico_secante(historico):

    print("\n" + "=" * 130)
    print("                    HISTÓRICO DE ITERAÇÕES - MÉTODO DA SECANTE")
    print("=" * 130)

    print(
        f"{'Iter':<6}"
        f"{'x0':<15}"
        f"{'x1':<15}"
        f"{'x2':<15}"
        f"{'f(x2)':<18}"
        f"{'Erro f':<18}"
        f"{'Erro x':<18}"
    )

    print("-" * 130)

    for item in historico:

        print(
            f"{item['iteracao']:<6}"
            f"{item['x0']:<15.8f}"
            f"{item['x1']:<15.8f}"
            f"{item['x2']:<15.10f}"
            f"{item['fx2']:<18.6e}"
            f"{item['erro_f']:<18.6e}"
            f"{item['erro_x']:<18.6e}"
        )

    print("-" * 130)


# ==========================================
# 7. GRAFICO DA FUNCAO
# ==========================================


def mostrar_grafico(f, a, b, raiz, nome_metodo):

    # Define uma margem para visualizar a curva
    margem = (b - a) * 0.15

    inicio = a - margem
    fim = b + margem

    # Gera os pontos do gráfico
    pontos = [
        inicio + i * (fim - inicio) / 499
        for i in range(500)
    ]

    valores = []

    # Avalia a função tratando possíveis erros
    for ponto in pontos:

        try:
            valor = float(f(ponto))

            if math.isfinite(valor):
                valores.append(valor)
            else:
                valores.append(float("nan"))

        except (ValueError, TypeError, ZeroDivisionError, OverflowError):
            valores.append(float("nan"))

    plt.figure(figsize=(10, 6))

    # Desenha a função
    plt.plot(
        pontos,
        valores,
        label="f(x)",
        color="blue"
    )

    # Desenha os eixos
    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="black", linewidth=0.8)

    # Marca a raiz ou última aproximação
    if raiz is not None:

        try:
            valor_raiz = float(f(raiz))

            if math.isfinite(valor_raiz):

                plt.scatter(
                    raiz,
                    valor_raiz,
                    color="red",
                    s=70,
                    label=f"Aproximação: {raiz:.6f}",
                    zorder=5
                )

        except (ValueError, TypeError, ZeroDivisionError, OverflowError):
            pass

    plt.title(f"Método da {nome_metodo}")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.show()


#==========================================
# 7.1 GRAFICO DO METODO DE NEWTON-RAPHSON
#==========================================

def mostrar_grafico_newton(f, historico, x0, raiz, mensagem):

    # Define os limites do gráfico a partir das aproximações
    aproximacoes = [x0]

    for item in historico:
        aproximacoes.append(item["x_proximo"])

    inicio = min(aproximacoes)
    fim = max(aproximacoes)

    # Evita uma janela de visualização com largura zero
    if inicio == fim:
        margem = max(1, abs(inicio) * 0.2)
    else:
        margem = (fim - inicio) * 0.25

    inicio -= margem
    fim += margem

    # Calcula os pontos da curva
    pontos = [
        inicio + i * (fim - inicio) / 499
        for i in range(500)
    ]

    valores = []

    for ponto in pontos:
        try:
            valor = f(ponto)

            if math.isfinite(valor):
                valores.append(valor)
            else:
                valores.append(float("nan"))

        except (ValueError, TypeError, ZeroDivisionError, OverflowError):
            valores.append(float("nan"))

    plt.figure(figsize=(11, 7))

    # Desenha a função
    plt.plot(
        pontos,
        valores,
        label="f(x)",
        color="blue"
    )

    # Desenha os eixos
    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="black", linewidth=0.8)

    # Desenha as tangentes de cada iteração
    for i, item in enumerate(historico):

        xn = item["x_atual"]
        xn1 = item["x_proximo"]
        derivada = item["derivada"]

        fxn = f(xn)

        # Equação da reta tangente
        x_tangente = [xn, xn1]

        y_tangente = [
            fxn,
            fxn + derivada * (xn1 - xn)
        ]

        plt.plot(
            x_tangente,
            y_tangente,
            linestyle="--",
            label="Tangente" if i == 0 else None
        )

        # Marca o ponto atual na curva
        plt.scatter(
            xn,
            fxn,
            color="green",
            zorder=5
        )

        # Marca a próxima aproximação no eixo x
        plt.scatter(
            xn1,
            0,
            color="orange",
            zorder=5
        )

        plt.annotate(
            f"x{i + 1}",
            (xn1, 0),
            xytext=(5, 10),
            textcoords="offset points"
        )

    # Verifica se o método convergiu
    convergiu = (
        "Convergência alcançada" in mensagem
        or "raiz exata" in mensagem.lower()
    )

    if raiz is not None:

        if convergiu:
            plt.scatter(
                raiz,
                f(raiz),
                color="red",
                s=70,
                label="Raiz aproximada",
                zorder=6
            )
        else:
            plt.scatter(
                raiz,
                f(raiz),
                color="red",
                s=70,
                label="Última aproximação",
                zorder=6
            )

    plt.title("Método de Newton-Raphson")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.show()



# ==========================================
# 8. PROGRAMA PRINCIPAL
# ==========================================

print("=" * 45)
print("       CALCULADORA MATEMATICA")
print("=" * 45)

try:

    expressao = input("\nDigite a funcao f(x): ")

    f = criar_funcao(expressao)

    tol = float(input("Digite a tolerancia: "))
    max_iter = int(input("Digite o numero maximo de iteracoes: "))

    if tol <= 0 or max_iter <= 0:
        raise ValueError("Tolerancia e iteracoes devem ser positivas.")

    # Menu de metodos
    print("\n======================================")
    print("          ESCOLHA DO METODO")
    print("======================================")
    print("1 - Regula Falsi")
    print("2 - Bissecao")
    print("3 - Newton-Raphson")
    print("4 - Método de Illinois")
    print("5 - Método da Secante")

    opcao = input("\nEscolha o metodo: ")

    if opcao == "1":

        a = float(input("Digite o limite inferior (a): "))
        b = float(input("Digite o limite superior (b): "))

        if a >= b:
            raise ValueError("O limite inferior deve ser menor que o superior.")

        raiz, historico, mensagem = regula_falsi(
            f, a, b, tol, max_iter
        )

        nome_metodo = "REGULA FALSI"

    elif opcao == "2":

        a = float(input("Digite o limite inferior (a): "))
        b = float(input("Digite o limite superior (b): "))

        if a >= b:
            raise ValueError("O limite inferior deve ser menor que o superior.")

        raiz, historico, mensagem = bissecao(
            f, a, b, tol, max_iter
        )

        nome_metodo = "BISSECAO"

    elif opcao == "3":

        x0 = float(input("Digite a aproximacao inicial (x0): "))

        raiz, historico, mensagem = newton_raphson(
            expressao, x0, tol, max_iter
        )

        nome_metodo = "NEWTON-RAPHSON"

        # Define uma janela para o grafico
        a = x0 - 2
        b = x0 + 2
    elif opcao == "4":

        a = float(input("Digite o limite inferior (a): "))
        b = float(input("Digite o limite superior (b): "))

        if a >= b:
            raise ValueError("O limite inferior deve ser menor que o superior.")

        raiz, historico, mensagem = metodo_illinois(
            f, a, b, tol, max_iter
        )

        nome_metodo = "ILLINOIS"
    elif opcao == "5":

        nome_metodo = "Método da Secante"

        print("\nMetodo selecionado: SECANTE")

        x0 = float(input("Digite a primeira aproximação (x0): "))
        x1 = float(input("Digite a segunda aproximação (x1): "))

        raiz, historico, mensagem = secante(
            f,
            x0,
            x1,
            tol,
            max_iter
        )

    else:
        raise ValueError("Opcao de metodo invalida.")

    
    # ======================================
    # EXIBICAO DOS RESULTADOS
    # ======================================

    print(f"\nMetodo selecionado: {nome_metodo}")
    print(f"Resultado: {mensagem}")

    # Exibe o histórico somente quando existem iterações
    if historico:

        if opcao == "3":
            mostrar_historico_newton(historico)

        elif opcao == "4":
            mostrar_historico_illinois(historico)

        elif opcao == "5":
            mostrar_historico_secante(historico)

        else:
            mostrar_historico(historico)
    # Identifica se o método encontrou uma raiz
    convergiu = (
        "convergência alcançada" in mensagem.lower()
        or "raiz exata" in mensagem.lower()
        or "raiz encontrada" in mensagem.lower()
    )

    if raiz is not None:

        if convergiu:
            print(f"\nRaiz aproximada: {raiz:.10f}")
            print(f"f(raiz): {f(raiz):.12e}")
            print(f"Iteracoes realizadas: {len(historico)}")

        else:
            print("\nO metodo nao convergiu.")
            print(f"Ultima aproximacao: {raiz:.10f}")
            print(f"f(ultima aproximacao): {f(raiz):.12e}")
            print(f"Iteracoes realizadas: {len(historico)}")

    else:
        print("\nNao foi possivel encontrar uma raiz.")
        print(f"Motivo: {mensagem}")

    # ======================================
    # EXIBICAO DOS GRAFICOS
    # ======================================

    if opcao in ("1", "2", "4"):
        mostrar_grafico(
            f, a, b, raiz, nome_metodo
        )
    elif opcao == "5":
        mostrar_grafico(
            f,
            min(x0, x1),
            max(x0, x1),
            raiz,
            nome_metodo
        )
    elif opcao == "3":
        mostrar_grafico_newton(
            f, historico, x0, raiz, mensagem
        )

except (ValueError, TypeError, NameError, SyntaxError,
        ZeroDivisionError, OverflowError) as erro:

    print(f"\nErro: {erro}")
