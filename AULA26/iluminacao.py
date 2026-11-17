
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

LARGURA = 900
ALTURA = 650

POSICAO_LUZ = [3.0, 5.0, 4.0, 1.0]

def configurar_iluminacao():
    # Ativa o sistema de iluminação do OpenGL
    glEnable(GL_LIGHTING)

    # Ativa a primeira fonte luminosa
    glEnable(GL_LIGHT0)

    # Ativa o cálculo correto das normais após transformações
    glEnable(GL_NORMALIZE)

    # iluminação ambiente global da cena
    glLightModelfv(
        GL_LIGHT_MODEL_AMBIENT,
        [0.20, 0.20, 0.20, 1.0]
    )

    # posição da fonte luminosa
    glLightfv(
        GL_LIGHT0,
        GL_POSITION,
        POSICAO_LUZ
    )

    # componente ambiente da fonte luminosa
    glLightfv(
        GL_LIGHT0,
        GL_AMBIENT,
        [0.25, 0.25, 0.25, 1.0]
    )

    # componente difusa da fonte luminosa
    glLightfv(
        GL_LIGHT0,
        GL_DIFFUSE,
        [1.0, 1.0, 1.0, 1.0]
    )

    # componente especular da fonte luminosa
    glLightfv(
        GL_LIGHT0,
        GL_SPECULAR,
        [1.0, 1.0, 1.0, 1.0]
    )

    # cálculo de iluminação considerando
    # o observador como uma posição local
    glLightModeli(
        GL_LIGHT_MODEL_LOCAL_VIEWER,
        GL_TRUE
    )

def configurar_material():
    # Reflexão ambiente: contribuição básica de luz
    glMaterialfv(
        GL_FRONT,
        GL_AMBIENT,
        [0.20, 0.02, 0.02, 1.0]
    )

    # Reflexão difusa: determina a cor principal
    glMaterialfv(
        GL_FRONT,
        GL_DIFFUSE,
        [0.85, 0.08, 0.05, 1.0]
    )

    # Reflexão especular: intensidade do brilho
    glMaterialfv(
        GL_FRONT,
        GL_SPECULAR,
        [1.0, 1.0, 1.0, 1.0]
    )

    # Concentração do brilho especular
    glMaterialf(
        GL_FRONT,
        GL_SHININESS,
        80.0
    )

def desenhar_chao():
    # Desabilita a iluminação para definir uma cor
    # constante para o chão neste exemplo
    glDisable(GL_LIGHTING)
    glColor3f(0.65, 0.65, 0.65)

    glBegin(GL_QUADS)
    # Normal apontando para cima
    glNormal3f(0.0, 1.0, 0.0)

    glVertex3f(-6.0, -1.0, -6.0)
    glVertex3f(-6.0, -1.0,  6.0)
    glVertex3f( 6.0, -1.0,  6.0)
    glVertex3f( 6.0, -1.0, -6.0)

    glEnd()

    # Reativa a iluminação
    glEnable(GL_LIGHTING)

def desenhar_esfera():
    configurar_material()

    # Cria um objeto auxiliar para desenhar uma esfera
    quadric = gluNewQuadric()

    # Define normais suaves para a superfície
    gluQuadricNormals(quadric, GLU_SMOOTH)

    # Desenha uma esfera de raio 1
    # Os parâmetros seguintes definem a quantidade
    # de divisões longitudinais e latitudinais
    gluSphere(quadric, 1.0, 60, 60)

    # Libera o objeto auxiliar
    gluDeleteQuadric(quadric)

def desenhar_referencia_luz():
    glDisable(GL_LIGHTING)
    glPushMatrix()

    glTranslatef(
        POSICAO_LUZ[0],
        POSICAO_LUZ[1],
        POSICAO_LUZ[2]
    )

    glColor3f(1.0, 1.0, 0.0)

    quadric = gluNewQuadric()
    gluSphere(quadric, 0.12, 20, 20)
    gluDeleteQuadric(quadric)

    glPopMatrix()

    glEnable(GL_LIGHTING)

def main():

    if not glfw.init():
        raise RuntimeError("Não foi possível inicializar GLFW.")

    # Solicita um contexto OpenGL compatível com a API clássica.
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

    janela = glfw.create_window(
        LARGURA,
        ALTURA,
        "Computacao Grafica - Iluminacao Phong",
        None,
        None
    )

    if not janela:
        glfw.terminate()
        raise RuntimeError("Não foi possível criar a janela.")

    glfw.make_context_current(janela)

    # Ativa o teste de profundidade
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.08, 0.08, 0.12, 1.0)

    # Configura a iluminação
    configurar_iluminacao()

    while not glfw.window_should_close(janela):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Configuração da projeção
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(
            45.0,
            LARGURA / ALTURA,
            0.1,
            100.0
        )

        # Configuração da câmera
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        gluLookAt(
            6.0, 4.0, 7.0,
            0.0, 0.0, 0.0,
            0.0, 1.0, 0.0
        )

        desenhar_chao()

        # Posiciona a esfera acima do chão
        glPushMatrix()
        glTranslatef(0.0, 0.0, 0.0)
        desenhar_esfera()
        glPopMatrix()

        # Mostra visualmente a posição da luz
        desenhar_referencia_luz()

        glfw.swap_buffers(janela)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()