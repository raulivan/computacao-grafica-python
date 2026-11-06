
import numpy as np
import glfw

from OpenGL.GL import *
from OpenGL.GLU import *


# Cubo
def criar_cubo(subdivisoes=8):
    vertices = []
    faces = []

    # Dicionário para evitar vértices duplicados.
    mapa = {}

    # Coordenadas da grade.
    valores = np.linspace(-1, 1, subdivisoes + 1)

    def adicionar_vertice(ponto):
        chave = tuple(np.round(ponto, 6))

        if chave not in mapa:
            mapa[chave] = len(vertices)
            vertices.append(ponto)

        return mapa[chave]

    #  faces do cubo.
    for eixo in range(3):
        outros = [i for i in range(3) if i != eixo]

        for sinal in [-1, 1]:
            for i in range(subdivisoes):
                for j in range(subdivisoes):

                    pontos = []

                    coordenadas = [
                        (valores[i], valores[j]),
                        (valores[i+1], valores[j]),
                        (valores[i+1], valores[j+1]),
                        (valores[i], valores[j+1])
                    ]

                    for a, b in coordenadas:

                        ponto = [0.0, 0.0, 0.0]

                        ponto[eixo] = sinal
                        ponto[outros[0]] = a
                        ponto[outros[1]] = b

                        pontos.append(adicionar_vertice(ponto))

                    faces.append(pontos)

    return np.array(vertices), faces


# BEND - CURVATURA
def bend(vertices, intensidade):

    resultado = vertices.copy()
    k = intensidade

    if abs(k) < 0.00001:
        return resultado

    x = vertices[:, 0]

    #  curvatura no plano XY.
    resultado[:, 0] = np.sin(k * x) / k
    resultado[:, 1] += (
        1 - np.cos(k * x)
    ) / k

    return resultado

# LATTICE - DEFORMAÇÃO POR GRADE DE CONTROLE
def lattice(vertices, intensidade):
    resultado = vertices.copy()

    # Normaliza as coordenadas para [0, 1].
    u = (vertices[:, 0] + 1) / 2
    v = (vertices[:, 1] + 1) / 2
    w = (vertices[:, 2] + 1) / 2

    # deslocamento de um ponto de controle
    # próximo ao canto superior do cubo.
    deslocamento = intensidade * u * v * w

    resultado[:, 0] += deslocamento
    resultado[:, 1] += deslocamento * 0.5

    return resultado


# MESHSMOOTH - SUAVIZAÇÃO
def mesh_smooth(vertices, faces, intensidade):

    resultado = vertices.copy()

    # lista de vértices vizinhos.
    vizinhos = [set() for _ in vertices]

    for face in faces:
        for i in range(len(face)):

            atual = face[i]
            proximo = face[(i + 1) % len(face)]

            vizinhos[atual].add(proximo)
            vizinhos[proximo].add(atual)

    # executa três iterações de suavização.
    for _ in range(3):
        novo = resultado.copy()

        for i, lista in enumerate(vizinhos):

            if not lista:
                continue

            media = resultado[list(lista)].mean(axis=0)
            novo[i] = resultado[i] + intensidade * (
                media - resultado[i]
            )

        resultado = novo

    return resultado


# OPTIMIZE - REDUÇÃO DA COMPLEXIDADE DA MALHA
def optimize(intensidade):
    # Quanto maior a intensidade, menor a subdivisão
    subdivisoes = max(
        1,
        int(round(8 * (1 - intensidade)))
    )
    return criar_cubo(subdivisoes)


# BEVEL - CHANFRAMENTO DAS ARESTAS
def bevel(vertices, intensidade):

    resultado = vertices.copy()

    # Limita a largura para manter uma geometria válida
    raio = np.clip(intensidade, 0.02, 0.45)

    limite = 1 - raio

    for i, p in enumerate(vertices):
        #  a face mais próxima.
        eixo = np.argmax(np.abs(p))
        q = p.copy()
        # cria um ponto na região interna do cubo.
        q[eixo] = np.sign(p[eixo]) * limite

        # limita as outras coordenadas.
        for j in range(3):

            if j != eixo:
                q[j] = np.clip(
                    p[j],
                    -limite,
                    limite
                )

        # calcula a direção do arredondamento.
        direcao = p - q
        norma = np.linalg.norm(direcao)

        if norma > 0:

            resultado[i] = (
                q + raio * direcao / norma
            )

    return resultado

# MELT - EFEITO DE DERRETIMENTO
def melt(vertices, intensidade):
    resultado = vertices.copy()

    x = vertices[:, 0]
    y = vertices[:, 1]
    z = vertices[:, 2]

    # normaliza a altura
    altura = (z + 1) / 2

    # a deformação aumenta em direção ao topo
    deformacao = intensidade * altura ** 2

    # cria pequenas irregularidades
    irregularidade = (
        1
        + 0.25 * np.sin(4 * x)
        * np.cos(4 * y)
    )

    # deslocamento vertical
    resultado[:, 2] -= deformacao * irregularidade

    # deslocamento lateral
    resultado[:, 0] += (
        intensidade * 0.15 * altura ** 2
        * np.sin(3 * y)
    )

    return resultado

# SKEW - INCLINAÇÃO
def skew(vertices, intensidade):
    resultado = vertices.copy()

    # Desloca X proporcionalmente à altura
    resultado[:, 0] += intensidade * vertices[:, 2]

    return resultado


# SQUEEZE - COMPRESSÃO
def squeeze(vertices, intensidade):
    resultado = vertices.copy()
    fator = np.clip(intensidade, 0.1, 1.0)

    # Comprime no eixo Z.
    resultado[:, 2] *= fator
    # Compensa nas dimensões horizontais.
    compensacao = 1 / np.sqrt(fator)

    resultado[:, 0] *= compensacao
    resultado[:, 1] *= compensacao

    return resultado


# STRETCH - ALONGAMENTO
def stretch(vertices, intensidade):
    resultado = vertices.copy()
    fator = max(0.1, 1 + intensidade)
    # Alongamento vertical.
    resultado[:, 2] *= fator

    # Compensação horizontal.
    compensacao = 1 / np.sqrt(fator)

    resultado[:, 0] *= compensacao
    resultado[:, 1] *= compensacao

    return resultado


# TAPER - AFUNILAMENTO
def taper(vertices, intensidade):
    resultado = vertices.copy()

    # Normaliza a altura
    altura = (vertices[:, 2] + 1) / 2
    # Calcula a escala progressiva
    escala = 1 + intensidade * altura
    # Modifica largura e profundidade
    resultado[:, 0] *= escala
    resultado[:, 1] *= escala

    return resultado


# TWIST - TORÇÃO
def twist(vertices, intensidade):

    resultado = vertices.copy()
    # O ângulo de rotação depende da altura
    angulo = intensidade * vertices[:, 2]

    cos_a = np.cos(angulo)
    sin_a = np.sin(angulo)

    x = vertices[:, 0]
    y = vertices[:, 1]

    # Rotação progressiva ao redor do eixo Z
    resultado[:, 0] = (
        x * cos_a - y * sin_a
    )

    resultado[:, 1] = (
        x * sin_a + y * cos_a
    )

    return resultado


# modificaroes
modificadores = {
    "BEND": 1,
    "LATTICE": 2,
    "MESHSMOOTH": 3,
    "OPTIMIZE": 4,
    "BEVEL": 5,
    "MELT": 6,
    "SKEW": 7,
    "SQUEEZE": 8,
    "STRETCH": 9,
    "TAPER": 10,
    "TWIST": 11
}

selecionado = "BEND"
intensidade = 0.6

def aplicar_modificador(nome, vertices, faces, valor):

    if nome == "BEND":
        return bend(vertices, valor), faces

    if nome == "LATTICE":
        return lattice(vertices, valor), faces

    if nome == "MESHSMOOTH":
        return mesh_smooth(vertices, faces, valor), faces

    if nome == "OPTIMIZE":
        return optimize(valor)

    if nome == "BEVEL":
        return bevel(vertices, valor), faces

    if nome == "MELT":
        return melt(vertices, valor), faces

    if nome == "SKEW":
        return skew(vertices, valor), faces

    if nome == "SQUEEZE":
        return squeeze(vertices, valor), faces

    if nome == "STRETCH":
        return stretch(vertices, valor), faces

    if nome == "TAPER":
        return taper(vertices, valor), faces

    if nome == "TWIST":
        return twist(vertices, valor), faces

    return vertices.copy(), faces


def teclado(janela, tecla, scancode, acao, mods):

    global selecionado, intensidade

    if acao != glfw.PRESS:
        return

    teclas = {
        glfw.KEY_1: "BEND",
        glfw.KEY_2: "LATTICE",
        glfw.KEY_3: "MESHSMOOTH",
        glfw.KEY_4: "OPTIMIZE",
        glfw.KEY_5: "BEVEL",
        glfw.KEY_6: "MELT",
        glfw.KEY_7: "SKEW",
        glfw.KEY_8: "SQUEEZE",
        glfw.KEY_9: "STRETCH",
        glfw.KEY_0: "TAPER",
        glfw.KEY_M: "TWIST"
    }

    if tecla in teclas:

        selecionado = teclas[tecla]

        print("\nModificador:", selecionado)
        print("Intensidade:", intensidade)

    # Aumenta a intensidade
    elif tecla in [glfw.KEY_EQUAL, glfw.KEY_KP_ADD]:

        intensidade = min(2.0, intensidade + 0.1)

        print("Intensidade:", round(intensidade, 2))

    # Diminui a intensidade
    elif tecla in [glfw.KEY_MINUS, glfw.KEY_KP_SUBTRACT]:

        intensidade = max(0.0, intensidade - 0.1)

        print("Intensidade:", round(intensidade, 2))

    # Restaura os valores
    elif tecla == glfw.KEY_R:

        intensidade = 0.6
        selecionado = "BEND"

        print("Geometria original restaurada.")

    elif tecla == glfw.KEY_ESCAPE:

        glfw.set_window_should_close(janela, True)


def desenhar_malha(vertices, faces):

    # Desenha as faces preenchidas
    glColor3f(0.2, 0.55, 0.85)

    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0, 1.0)

    for face in faces:

        glBegin(GL_QUADS)

        for indice in face:

            glVertex3fv(vertices[indice])

        glEnd()

    glDisable(GL_POLYGON_OFFSET_FILL)

    # Desenha as arestas.
    glColor3f(0.05, 0.05, 0.05)
    glLineWidth(1.2)

    for face in faces:

        glBegin(GL_LINE_LOOP)

        for indice in face:

            glVertex3fv(vertices[indice])

        glEnd()

def main():
    global selecionado, intensidade

    if not glfw.init():
        raise Exception("Erro ao inicializar GLFW")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

    janela = glfw.create_window(
        900, 700,
        "Laboratório de Modificadores 3D", None, None
    )

    if not janela:
        glfw.terminate()
        raise Exception("Erro ao criar janela")

    glfw.make_context_current(janela)
    glfw.set_key_callback(janela, teclado)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.12, 0.12, 0.16, 1.0)

    # Cria a geometria original
    vertices_originais, faces_originais = criar_cubo(8)

    angulo = 0

    print("MODIFICADORES 3D")

    for nome, tecla in modificadores.items():
        print(f"{tecla} - {nome}")

    print("\n+/- : Alterar intensidade")
    print("R   : Restaurar")
    print("ESC : Sair")


    while not glfw.window_should_close(janela):
        largura, altura = glfw.get_framebuffer_size(janela)
        if altura == 0:
            glfw.poll_events()
            continue

        glViewport(0, 0, largura, altura)

        glClear(
            GL_COLOR_BUFFER_BIT |
            GL_DEPTH_BUFFER_BIT
        )

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(
            45,
            largura / altura,
            0.1,
            100
        )

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glTranslatef(0, 0, -5)

        glRotatef(angulo, 0, 1, 0)
        glRotatef(20, 1, 0, 0)

        # Obtém uma cópia da geometria original
        vertices = vertices_originais.copy()
        faces = faces_originais.copy()

        # Aplica o modificador selecionado
        vertices, faces = aplicar_modificador(
            selecionado,
            vertices,
            faces,
            intensidade
        )

        # Desenha a geometria modificada
        desenhar_malha(vertices, faces)

        glfw.set_window_title(
            janela, f"Modificador: {selecionado} | " f"Intensidade: {intensidade:.2f}"
        )

        angulo += 0.3

        if angulo >= 360:
            angulo = 0

        glfw.swap_buffers(janela)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
