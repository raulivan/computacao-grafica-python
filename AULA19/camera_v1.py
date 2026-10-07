"""
Casa 3D utilizando Python + OpenGL

Instalação:

    pip install PyOpenGL PyOpenGL_accelerate
"""
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

# configurações da tela
LARGURA = 1000
ALTURA = 700

# localização da camera
camera_x = 10.0
camera_y = 7.0
camera_z = 12.0

# pra onde a câmera está olhando.
# aproximadamente para o centro da casa.
target_x = 0.0
target_y = 2.0
target_z = 0.0

# vetor UP.
up_x = 0.0
up_y = 1.0
up_z = 0.0

# Velocidade da câmera
CAMERA_SPEED = 0.5

def inicializar():
    """
    características básicas da cena.
    """
    #  limpar a tela.cor do céu.
    glClearColor(
        0.45,  # Red
        0.70,  # Green
        1.00,  # Blue
        1.00   # Alpha
    )

    # Ativa o Depth Buffer.
    glEnable(GL_DEPTH_TEST)

    # Define o modo de sombreamento.
    glShadeModel(GL_SMOOTH)
    # fim inicializar

def desenhar_cubo():
    """
    Desenha um cubo centrado na origem.
    """
    glBegin(GL_QUADS)

    # Frente
    glNormal3f(0, 0, 1)
    glVertex3f(-1, -1, 1)
    glVertex3f( 1, -1, 1)
    glVertex3f( 1,  1, 1)
    glVertex3f(-1,  1, 1)

    # traz
    glNormal3f(0, 0, -1)
    glVertex3f( 1, -1, -1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1,  1, -1)
    glVertex3f( 1,  1, -1)

    # direita
    glNormal3f(1, 0, 0)
    glVertex3f(1, -1, 1)
    glVertex3f(1, -1, -1)
    glVertex3f(1,  1, -1)
    glVertex3f(1,  1, 1)

    # esquerda
    glNormal3f(-1, 0, 0)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1, 1)
    glVertex3f(-1,  1, 1)
    glVertex3f(-1,  1, -1)

    # superior
    glNormal3f(0, 1, 0)
    glVertex3f(-1, 1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)

    # inferior
    glNormal3f(0, -1, 0)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)

    glEnd()
    # fim desenhar_cubo

def desenhar_telhado():
    """
    telhado  formato de prisma.
    """
    # Cor do telhado.
    glColor3f(0.65, 0.08, 0.05)

    glBegin(GL_TRIANGLES)

    # frente
    glVertex3f(-4.2, 4.0, 3.2)
    glVertex3f( 4.2, 4.0, 3.2)
    glVertex3f( 0.0, 7.0, 3.2)

    # costas
    glVertex3f( 4.2, 4.0, -3.2)
    glVertex3f(-4.2, 4.0, -3.2)
    glVertex3f( 0.0, 7.0, -3.2)

    glEnd()


    # lados
    glBegin(GL_QUADS)

    # esquerdo
    glVertex3f(-4.2, 4.0, 3.2)
    glVertex3f(-4.2, 4.0, -3.2)
    glVertex3f(0.0, 7.0, -3.2)
    glVertex3f(0.0, 7.0, 3.2)

    # direito
    glVertex3f(4.2, 4.0, -3.2)
    glVertex3f(4.2, 4.0, 3.2)
    glVertex3f(0.0, 7.0, 3.2)
    glVertex3f(0.0, 7.0, -3.2)

    glEnd()
    # fim  desenhar_telhado

def desenhar_casa():
    """
    casa 3D
    """
    glPushMatrix()
    # translação 
    glTranslatef(0, 2, 0)
    # escala:
    glScalef(4, 2, 3)
    # Cor das paredes
    glColor3f(0.75, 0.45, 0.25)
    # parede
    desenhar_cubo()
    glPopMatrix()

    # teto
    glPushMatrix()
    desenhar_telhado()
    glPopMatrix()

    # porta
    glPushMatrix()
    glTranslatef(0, 1.3, 3.05)
    glScalef(0.9, 1.3, 0.15)
    glColor3f(0.25, 0.12, 0.05)
    desenhar_cubo()
    glPopMatrix()


    # janela esquerda
    glPushMatrix()
    glTranslatef(-2.3, 2.3, 3.05)
    glScalef(0.8, 0.8, 0.15)
    glColor3f(0.20, 0.70, 0.90)
    desenhar_cubo()
    glPopMatrix()

    # janela direita
    glPushMatrix()
    glTranslatef(2.3, 2.3, 3.05)
    glScalef(0.8, 0.8, 0.15)
    glColor3f(0.20, 0.70, 0.90)
    desenhar_cubo()
    glPopMatrix()
    # fim desenhar_casa

def desenhar_chao():
    """
    chão.
    """
    glColor3f(0.25, 0.55, 0.25)

    glBegin(GL_QUADS)
    glVertex3f(-30, 0, -30)
    glVertex3f( 30, 0, -30)
    glVertex3f( 30, 0,  30)
    glVertex3f(-30, 0,  30)
    glEnd()
    # FIM desenhar_chao


def configurar_projecao(largura, altura):
    """
    matriz de projeção.
    FOV   = 60 graus
    Aspect = largura / altura
    Near   = 0.1
    Far    = 100
    """

    if altura == 0:
        altura = 1

    aspect = largura / altura

    # Selecionamos a matriz de PROJEÇÃO.
    glMatrixMode(GL_PROJECTION)
    # var para matriz identidade.
    glLoadIdentity()

    # projeção perspectiva.
    gluPerspective(
        60.0,
        aspect,
        0.1,
        100.0
    )
    # volta para MODELVIEW.
    glMatrixMode(GL_MODELVIEW)
    # fim configurar_projecao


def desenhar():
    """
    desenhar tudo.
    """
    glClear(
        GL_COLOR_BUFFER_BIT |
        GL_DEPTH_BUFFER_BIT
    )

    # MODELVIEW
    glMatrixMode(GL_MODELVIEW)

    #  matriz identidade.
    glLoadIdentity()

    # VIEW MATRIX
    gluLookAt(
        camera_x,
        camera_y,
        camera_z,

        target_x,
        target_y,
        target_z,

        up_x,
        up_y,
        up_z
    )

    # WORLD
    desenhar_chao()
    desenhar_casa()

    # EXIBIÇÃO
    glutSwapBuffers()
    # fim desenhar


def redimensionar(largura, altura):
    """
    janela é redimensionada.
    """
    if altura == 0: altura = 1
    # janela onde o OpenGL irá desenhar.
    glViewport(
        0,
        0,
        largura,
        altura
    )
    # Atualiza a projeção.
    configurar_projecao(
        largura,
        altura
    )
    # fim redimensionar


def teclado(tecla, x, y):
    """
    controla a câmera utilizando o teclado.
    W -> aproxima a câmera
    S -> afasta a câmera
    A -> esquerda
    D -> direita
    Q -> sobe
    E -> desce
    ESC -> sair
    """

    global camera_x
    global camera_y
    global camera_z

    tecla = tecla.decode("utf-8").lower()

    if tecla == "w":
        camera_z -= CAMERA_SPEED
    elif tecla == "s":
        camera_z += CAMERA_SPEED
    elif tecla == "a":
        camera_x -= CAMERA_SPEED
    elif tecla == "d":
        camera_x += CAMERA_SPEED
    elif tecla == "q":
        camera_y += CAMERA_SPEED
    elif tecla == "e":
        camera_y -= CAMERA_SPEED
    elif tecla == "\x1b":
        raise SystemExit

    # desenhada novamente.
    glutPostRedisplay()
    # fim teclado

def teclas_especiais(tecla, x, y):
    """
    movimentar a câmera.
    """
    global camera_x
    global camera_y

    if tecla == GLUT_KEY_LEFT:
        camera_x -= CAMERA_SPEED
    elif tecla == GLUT_KEY_RIGHT:
        camera_x += CAMERA_SPEED
    elif tecla == GLUT_KEY_UP:
        camera_y += CAMERA_SPEED
    elif tecla == GLUT_KEY_DOWN:
        camera_y -= CAMERA_SPEED

    glutPostRedisplay()
    # fim teclas_especiais


def main():
    # Inicializa o GLUT.
    glutInit()

    glutInitDisplayMode(
        GLUT_DOUBLE |
        GLUT_RGB |
        GLUT_DEPTH
    )
    # tamanho inicial da janela.
    glutInitWindowSize(
        LARGURA,
        ALTURA
    )
    # Cria a janela.
    glutCreateWindow(
        b"Casa 3D - Camera Virtual"
    )

    # inicializa o OpenGL.
    inicializar()
    # registra a função responsável pelo desenho.
    glutDisplayFunc(desenhar)
    # registra a função de redimensionamento.
    glutReshapeFunc(redimensionar)
    # registra o teclado.
    glutKeyboardFunc(teclado)
    # registra as teclas especiais.
    glutSpecialFunc(teclas_especiais)
    # Define a projeção inicial.
    configurar_projecao(
        LARGURA,
        ALTURA
    )
    # Inicia o loop principal do GLUT.
    glutMainLoop()
    # fim main

if __name__ == "__main__":
    main()
