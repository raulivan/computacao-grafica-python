
"""
Controles:
    1 - Superfície de revolução
    2 - Superfície de deslocamento
    3 - Superfície bilinear
    4 - Superfície de Bézier
    5 - Esfera paramétrica
    T - Demonstra interpolação trilinear no terminal
    R - Reinicia a rotação
    ESC - Encerra o programa

Requisitos:
    pip install PyOpenGL PyOpenGL_accelerate numpy
"""
import math
import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


# Variáveis global
modo = 1
rotacao = 25.0

# Resolução da amostragem paramétrica
# quanto maior mais detalhada
RES_U = 35
RES_V = 35

def superficie_revolucao(u, v):
    """
    gera um ponto de uma superfície de revolução

    u percorre a altura do perfil
    v percorre o ângulo de rotação, de 0 a 2*pi

    O perfil define o raio e a altura do vaso
    """
    angulo = 2.0 * math.pi * v

    # Perfil definido por interpolação linear entre alturas
    # Cada par contém (altura, raio)
    perfil = [
        (0.0, 0.45), (0.15, 0.65),
        (0.40, 0.85), (0.75, 0.90),
        (1.05, 0.68), (1.30, 0.48),
        (1.50, 0.55), (1.65, 0.72),
    ]

    # converte u para a posição correspondente no perfil
    posicao = u * (len(perfil) - 1)
    indice = min(int(posicao), len(perfil) - 2)
    fracao = posicao - indice

    z0, r0 = perfil[indice]
    z1, r1 = perfil[indice + 1]

    # interpolação linear do raio e da altura
    raio = r0 + fracao * (r1 - r0)
    z = z0 + fracao * (z1 - z0)

    # rotação do perfil em torno do eixo Z
    x = raio * math.cos(angulo)
    y = raio * math.sin(angulo)

    # centraliza na origem
    return (x, y, z - 0.8)
    # fim superficie_revolucao


def superficie_deslocamento(u, v):
    """
    superfície ondulada
    calcuila s x e y no plano-base
    desloca cada ponto verticalmente
    de acordo com uma função senoidal
    """
    x = 2.0 * u - 1.0
    y = 2.0 * v - 1.0

    z = (
        0.40
        * math.sin(3.0 * math.pi * x)
        * math.cos(2.0 * math.pi * y)
    )

    return (x, y, z)
    # fim superficie_deslocamento


def superficie_bilinear(u, v):
    """
    Os quatro pontos de controle definem os cantos
    do quadrilátero
    """
    p00 = np.array([-1.0, -1.0, 0.0])
    p10 = np.array([ 1.0, -1.0, 0.0])
    p01 = np.array([-1.0,  1.0, 0.0])
    p11 = np.array([ 1.0,  1.0, 1.2])

    # cada peso corresponde a um canto
    p = (
        (1-u) * (1-v) * p00
        + u * (1-v) * p10
        + (1-u) * v * p01
        + u * v * p11
    )

    return tuple(p)
    # fim superficie_bilinear   


def bernstein(i, n, t):
    """
    calcula o polinômio de Bernstein B_i^n(t)
    math.comb(n, i) calcula o coeficiente binomial
    """
    return (
        math.comb(n, i)
        * (1.0 - t) ** (n - i)
        * t ** i
    )
    # fim bernstein


def superficie_bezier(u, v):
    """
    superfície de Bézier bicúbica

    rede de controle contém 4 x 4 pontos
    cada ponto de controle é um vetor (x, y, z)
    """

    # linhas por quatro colunas
    # as alturas diferentes geram uma curvatura suave
    controle = np.array([
        [
            [-1.5, -1.5,  0.0],
            [-0.5, -1.5,  0.3],
            [ 0.5, -1.5, -0.2],
            [ 1.5, -1.5,  0.0],
        ],
        [
            [-1.5, -0.5,  0.4],
            [-0.5, -0.5,  1.1],
            [ 0.5, -0.5,  0.8],
            [ 1.5, -0.5,  0.2],
        ],
        [
            [-1.5,  0.5,  0.2],
            [-0.5,  0.5,  0.9],
            [ 0.5,  0.5,  1.3],
            [ 1.5,  0.5,  0.4],
        ],
        [
            [-1.5,  1.5,  0.0],
            [-0.5,  1.5,  0.2],
            [ 0.5,  1.5,  0.5],
            [ 1.5,  1.5,  0.0],
        ],
    ], dtype=float)

    ponto = np.zeros(3)

    # soma ponderada dos 16 pontos de controle
    for i in range(4):
        bu = bernstein(i, 3, u)

        for j in range(4):
            bv = bernstein(j, 3, v)

            ponto += bu * bv * controle[i, j]

    return tuple(ponto)
    # fim superficie_bezier


def superficie_esfera(u, v):
    """
    paramétrica de raio 1
    u percorre a latitude
    v percorre a longitude
    """
    latitude = math.pi * (u - 0.5)
    longitude = 2.0 * math.pi * v

    x = math.cos(latitude) * math.cos(longitude)
    y = math.cos(latitude) * math.sin(longitude)
    z = math.sin(latitude)

    return (x, y, z)
    # superficie_esfera


def interpolacao_trilinear(u, v, w, valores):
    """
    Interpola um escalar dentro de um cubo unitário
    'valores' é um dicionário com as oito chaves:
        (0,0,0), (1,0,0), ..., (1,1,1)
    u, v e w devem pertencer ao intervalo [0, 1]
    """
    resultado = 0.0

    for i in (0, 1):
        for j in (0, 1):
            for k in (0, 1):

                # peso de cada vértice nas três dimensões
                wi = u if i == 1 else (1.0 - u)
                wj = v if j == 1 else (1.0 - v)
                wk = w if k == 1 else (1.0 - w)

                resultado += valores[(i, j, k)] * wi * wj * wk

    return resultado
    # interpolacao_trilinear


def demonstrar_trilinear():
    """
    exemplo de interpolação no centro do cubo.
    """
    valores = {
        (0, 0, 0): 0.0,
        (1, 0, 0): 1.0,
        (0, 1, 0): 2.0,
        (1, 1, 0): 3.0,
        (0, 0, 1): 4.0,
        (1, 0, 1): 5.0,
        (0, 1, 1): 6.0,
        (1, 1, 1): 8.0,
    }

    valor = interpolacao_trilinear(0.5, 0.5, 0.5, valores)

    print("\nInterpolação trilinear")
    print("Posição: u=0.5, v=0.5, w=0.5")
    print(f"Valor interpolado: {valor:.4f}")
    print("O resultado é a média ponderada dos oito vértices")


def desenhar_superficie(funcao, cor):
    """
    função S(u,v) e desenha sua malha parametrica
    """

    glColor3f(*cor)

    # linhas que percorrem a direção v
    for i in range(RES_U + 1):
        u = i / RES_U

        glBegin(GL_LINE_STRIP)

        for j in range(RES_V + 1):
            v = j / RES_V
            x, y, z = funcao(u, v)
            glVertex3f(x, y, z)

        glEnd()

    # linhas que percorrem a direção u
    for j in range(RES_V + 1):
        v = j / RES_V

        glBegin(GL_LINE_STRIP)

        for i in range(RES_U + 1):
            u = i / RES_U
            x, y, z = funcao(u, v)
            glVertex3f(x, y, z)

        glEnd()
    # fim desenhar_superficie


def inicializar():

    # glClearColor define a cor usada ao limpar o fundo
    glClearColor(0.08, 0.09, 0.13, 1.0)

    # glEnable(GL_DEPTH_TEST) ativa o teste de profundidade
    # Assim, superfícies mais próximas ocultam as mais distantes
    glEnable(GL_DEPTH_TEST)

    # glPointSize define o tamanho dos pontos, se forem desenhados
    glPointSize(5.0)


def desenhar_eixos():
    """
    Desenha os eixos cartesianos 
    """
    glBegin(GL_LINES)

    # Eixo X
    glColor3f(1.0, 0.2, 0.2)
    glVertex3f(-2.0, 0.0, 0.0)
    glVertex3f( 2.0, 0.0, 0.0)

    # Eixo Y
    glColor3f(0.2, 1.0, 0.2)
    glVertex3f(0.0, -2.0, 0.0)
    glVertex3f(0.0,  2.0, 0.0)

    # Eixo Z
    glColor3f(0.2, 0.5, 1.0)
    glVertex3f(0.0, 0.0, -1.5)
    glVertex3f(0.0, 0.0,  1.5)

    glEnd()


def exibir():
    """
    Callback desenhar cada quadro
    """
    global rotacao

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # glMatrixMode seleciona qual matriz será modificada
    # GL_MODELVIEW representa transformações e visualização
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # gluLookAt posiciona a câmera e define a direção de visão
    gluLookAt(
        4.0, 5.0, 3.5,  # posição da câmera
        0.0, 0.0, 0.0,  # ponto observado
        0.0, 0.0, 1.0   # direção vertical da cena
    )

    # glRotatef aplica uma rotação em torno de um eixo
    glRotatef(rotacao, 0.0, 0.0, 1.0)

    desenhar_eixos()

    if modo == 1:
        desenhar_superficie(
            superficie_revolucao,
            (0.3, 0.9, 1.0))
    elif modo == 2:
        desenhar_superficie(
            superficie_deslocamento,
            (1.0, 0.7, 0.2))
    elif modo == 3:
        desenhar_superficie(
            superficie_bilinear,
            (0.5, 1.0, 0.5))
    elif modo == 4:
        desenhar_superficie(
            superficie_bezier,
            (1.0, 0.4, 0.8))
    elif modo == 5:
        desenhar_superficie(
            superficie_esfera,
            (0.5, 0.8, 1.0))

    # glutSwapBuffers apresenta o quadro desenhado quando
    # a janela foi criada com GLUT_DOUBLE
    glutSwapBuffers()
    # fim exibir

def redimensionar(largura, altura):
    """
    janela muda de tamanho.
    """

    altura = max(altura, 1)

    # glViewport define a região da janela em que se desenha
    glViewport(0, 0, largura, altura)

    # GL_PROJECTION seleciona a matriz de projeção
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # gluPerspective cria uma projeção em perspectiva
    gluPerspective(
        45.0,                  # campo de visão vertical
        largura / float(altura),
        0.1,                   # plano próximo
        100.0                  # plano distante
    )
    glMatrixMode(GL_MODELVIEW)
    # fim redimensionar


def teclado(tecla, x, y):
    global modo, rotacao
    # GLUT entrega a tecla como bytes
    if tecla == b'\x1b':
        sys.exit(0)
    if tecla in (b'1', b'2', b'3', b'4', b'5'):
        modo = int(tecla.decode("ascii"))

        nomes = {
            1: "Superfície de revolução",
            2: "Superfície de deslocamento",
            3: "Superfície bilinear",
            4: "Superfície de Bézier",
            5: "Esfera paramétrica",
        }
        print("Modelo selecionado:", nomes[modo])

    elif tecla in (b't', b'T'):
        demonstrar_trilinear()
    elif tecla in (b'r', b'R'):
        rotacao = 25.0

    glutPostRedisplay()
    # fim teclado


def animar():
    global rotacao

    rotacao += 0.15

    if rotacao >= 360.0:
        rotacao -= 360.0

    glutPostRedisplay()


def main():
    glutInit(sys.argv)

    # GLUT_DOUBLE usa buffers duplos para reduzir falhas .
    # GLUT_RGB seleciona o modo de cores RGB.
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 750)
    glutInitWindowPosition(100, 80)

    glutCreateWindow(b"Superficies 3D")
    inicializar()

    # Callbacks: desenho, redimensionamento e teclado
    glutDisplayFunc(exibir)
    glutReshapeFunc(redimensionar)
    glutKeyboardFunc(teclado)

    # glutIdleFunc registra uma função executada quando
    # o GLUT está ocioso; aqui ela anima a rotação
    glutIdleFunc(animar)

    print("\nMENU")
    print("1 - Revolucao")
    print("2 - Deslocamento")
    print("3 - Interpolacao bilinear")
    print("4 - Bezier")
    print("5 - Esfera parametrica")
    print("T - Interpolacao trilinear no terminal")
    print("R - Reiniciar rotacao")
    print("ESC - Sair\n")

    # glutMainLoop inicia o ciclo de eventos da janela.
    glutMainLoop()
    # fim main

if __name__ == "__main__":
    main()
