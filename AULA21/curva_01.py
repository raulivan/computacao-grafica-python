import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

LARGURA = 800
ALTURA = 600

# Representação que será exibida.
# 1 = conjunto de pontos
# 2 = representação explícita
# 3 = representação implícita
# 4 = representação paramétrica
modo = 1


# modo=1 curva representada por conjunto de pontos
pontos = [
    (-0.90, -0.50),
    (-0.70, -0.10),
    (-0.45,  0.25),
    (-0.15,  0.40),
    ( 0.15,  0.30),
    ( 0.45,  0.55),
    ( 0.75,  0.35),
    ( 0.90,  0.65),
]


# modo=2 representação explicita da curva
def curva_explicita(x):
    """
    Recebe x e retorna y = x².
    """
    return x ** 2


# modo=3 representação implicita da curva
def pertence_circunferencia(x, y, tolerancia=0.02):
    """
    Verifica aproximadamente se o ponto está na circunferência
    unitária x² + y² - 1 = 0.
    """
    resultado = x**2 + y**2 - 1
    return abs(resultado) < tolerancia


# modo=4 representação paramétrica da curva
def curva_parametrica(t):
    """
    Calcula um ponto da circunferência a partir do parâmetro t.
    x(t) = cos(t)
    y(t) = sin(t)
    O parâmetro t varia de 0 a 2*pi.
    """
    x = math.cos(t)
    y = math.sin(t)
    return x, y


def desenhar_eixos():
    """
    Desenha os eixos cartesianos.
    """
    glColor3f(0.45, 0.45, 0.45)
    glBegin(GL_LINES)

    # Eixo horizontal: X
    glVertex2f(-2.0, 0.0)
    glVertex2f( 2.0, 0.0)

    # Eixo vertical: Y
    glVertex2f(0.0, -1.5)
    glVertex2f(0.0,  2.0)

    glEnd()


def desenhar_pontos():
    """
    Desenha a curva fornecida por um conjunto de pontos.
    GL_LINE_STRIP conecta os vértices consecutivos.
    GL_POINTS desenha os vértices como pontos isolados.
    """
    # Desenha os segmentos que conectam os pontos.
    glColor3f(0.0, 0.75, 0.55)
    glLineWidth(3.0)

    # glBegin(GL_LINE_STRIP):
    # inicia uma linha poligonal contínua.
    # Cada vértice novo é conectado ao anterior.
    glBegin(GL_LINE_STRIP)

    for x, y in pontos:
        glVertex2f(x, y)

    glEnd()

    # Desenha os pontos originais para destacar a amostragem.
    glColor3f(1.0, 0.35, 0.10)
    glPointSize(8.0)

    # glBegin(GL_POINTS):
    # interpreta cada vértice como um ponto independente.
    glBegin(GL_POINTS)

    for x, y in pontos:
        glVertex2f(x, y)

    glEnd()
    # fim desenhar_pontos


def desenhar_curva_explicita():
    """
    Desenha y = x² 
    """
    glColor3f(0.15, 0.45, 1.0)
    glLineWidth(3.0)

    glBegin(GL_LINE_STRIP)

    # Intervalo de -1.3 até 1.3.
    # Passo de 0.01 (visual mais suave)
    x = -1.3

    while x <= 1.3001:
        y = curva_explicita(x)
        glVertex2f(x, y)
        x += 0.01

    glEnd()


def desenhar_curva_implicita():
    """
    Desenha x² + y² - 1 = 0
    este exemplo não é um algoritmo eficiente
    para desenhar curvas complexas.
    """
    glColor3f(0.75, 0.25, 0.85)
    glPointSize(3.0)
    passo = 0.01

    glBegin(GL_POINTS)
    x = -1.1
    while x <= 1.1001:
        y = -1.1
        while y <= 1.1001:
            if pertence_circunferencia(x, y):
                glVertex2f(x, y)
            y += passo
        x += passo
    glEnd()


def desenhar_curva_parametrica():
    """
    os pontos são gerados na ordem de percurso,
    iremos conectá-los diretamente.
    """
    glColor3f(1.0, 0.55, 0.05)
    glLineWidth(3.0)
    glBegin(GL_LINE_STRIP)

    quantidade_segmentos = 360
    for i in range(quantidade_segmentos + 1):
        # Converte o índice em um ângulo de 0 a 2*pi.
        t = (2.0 * math.pi * i) / quantidade_segmentos
        x, y = curva_parametrica(t)
        glVertex2f(x, y)
    glEnd()


def desenhar():
    """
    redesenhar a janela.
    """
    glClear(GL_COLOR_BUFFER_BIT)
    desenhar_eixos()

    if modo == 1:
        desenhar_pontos()
    elif modo == 2:
        desenhar_curva_explicita()
    elif modo == 3:
        desenhar_curva_implicita()
    elif modo == 4:
        desenhar_curva_parametrica()

    glutSwapBuffers()


def redimensionar(largura, altura):
    if altura == 0:
        altura = 1

    glViewport(0, 0, largura, altura)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # projeção ortográfica bidimensional.
    gluOrtho2D(-2.0, 2.0, -1.5, 2.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def teclado(tecla, x, y):
    """
    escolher a representação pressionando 1, 2, 3 ou 4.
    Pressione ESC para encerrar.
    """
    global modo

    if tecla == b'1':
        modo = 1
    elif tecla == b'2':
        modo = 2
    elif tecla == b'3':
        modo = 3
    elif tecla == b'4':
        modo = 4
    elif tecla == b'\x1b':
        # glutLeaveMainLoop encerra o loop principal do GLUT.
        try:
            glutLeaveMainLoop()
        except Exception:
            raise SystemExit
    # janela seja redesenhada.
    glutPostRedisplay()

def main():
    glutInit()
    # Define o uso de cores RGB e buffer duplo.
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    # posição inicial da janela na tela.
    glutInitWindowPosition(100, 100)
    glutInitWindowSize(LARGURA, ALTURA)

    glutCreateWindow(
        b"Representacao de Curvas"
    )
    glClearColor(0.08, 0.08, 0.10, 1.0)

    # Registra as funções que o GLUT chamará.
    glutDisplayFunc(desenhar)
    glutReshapeFunc(redimensionar)
    glutKeyboardFunc(teclado)

    # inicia o loop de eventos. 
    glutMainLoop()

if __name__ == "__main__":
    main()