import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

rotacao_objeto = 0.0
modo_sombra = 1  # 1: Dura (Hard), 2: Suave (Soft)

def calcular_matriz_sombra(plano, luz_pos):
    """
    Calcula a Matriz 4x4 que projeta vértices em um plano a partir 
    de um ponto de luz. (Projeção Planar)
    """
    # Produto escalar entre o plano (A, B, C, D) 
    # e a posição da luz (X, Y, Z, W)
    dot = plano[0]*luz_pos[0] + plano[1]*luz_pos[1] + plano[2]*luz_pos[2] + plano[3]*luz_pos[3]
    
    # Construção da Matriz 4x4 em formato "Coluna" (Exigência do OpenGL)
    matriz = [
        dot - luz_pos[0]*plano[0], -luz_pos[1]*plano[0],      -luz_pos[2]*plano[0],      -luz_pos[3]*plano[0],
        -luz_pos[0]*plano[1],      dot - luz_pos[1]*plano[1], -luz_pos[2]*plano[1],      -luz_pos[3]*plano[1],
        -luz_pos[0]*plano[2],      -luz_pos[1]*plano[2],      dot - luz_pos[2]*plano[2], -luz_pos[3]*plano[2],
        -luz_pos[0]*plano[3],      -luz_pos[1]*plano[3],      -luz_pos[2]*plano[3],      dot - luz_pos[3]*plano[3]
    ]
    return matriz

def desenhar_cubo():
    # Desenhando um cubo de forma direta para manter o foco na iluminação
    glBegin(GL_QUADS)
    # Frente
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(-0.5, -0.5,  0.5); glVertex3f( 0.5, -0.5,  0.5)
    glVertex3f( 0.5,  0.5,  0.5); glVertex3f(-0.5,  0.5,  0.5)
    # Trás
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(-0.5, -0.5, -0.5); glVertex3f(-0.5,  0.5, -0.5)
    glVertex3f( 0.5,  0.5, -0.5); glVertex3f( 0.5, -0.5, -0.5)
    # Topo
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-0.5,  0.5, -0.5); glVertex3f(-0.5,  0.5,  0.5)
    glVertex3f( 0.5,  0.5,  0.5); glVertex3f( 0.5,  0.5, -0.5)
    # Base
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-0.5, -0.5, -0.5); glVertex3f( 0.5, -0.5, -0.5)
    glVertex3f( 0.5, -0.5,  0.5); glVertex3f(-0.5, -0.5,  0.5)
    # Direita
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f( 0.5, -0.5, -0.5); glVertex3f( 0.5,  0.5, -0.5)
    glVertex3f( 0.5,  0.5,  0.5); glVertex3f( 0.5, -0.5,  0.5)
    # Esquerda
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(-0.5, -0.5, -0.5); glVertex3f(-0.5, -0.5,  0.5)
    glVertex3f(-0.5,  0.5,  0.5); glVertex3f(-0.5,  0.5, -0.5)
    glEnd()

def desenhar_chao():
    # O chão é um grande plano. Coordenada Y = -1.0
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0) # Aponta para cima
    glVertex3f(-10.0, -1.0,  10.0)
    glVertex3f( 10.0, -1.0,  10.0)
    glVertex3f( 10.0, -1.0, -10.0)
    glVertex3f(-10.0, -1.0, -10.0)
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global modo_sombra
    if action == glfw.PRESS:
        if key == glfw.KEY_1:
            modo_sombra = 1
            print("Modo: Sombra Dura (1 Amostra)")
        elif key == glfw.KEY_2:
            modo_sombra = 2
            print("Modo: Sombra Suave (Múltiplas Amostras - Luz de Área)")

def main():
    global rotacao_objeto

    if not glfw.init(): return
    window = glfw.create_window(800, 600, 
                                "1: Sombra Dura | 2: Sombra Suave",
                                  None, None)
    if not window: glfw.terminate(); return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glEnable(GL_DEPTH_TEST)
    
    # Configuração da Câmera
    gluPerspective(45, (800/600), 0.1, 50.0)
    gluLookAt(0, 3, 6, 0, 0, 0, 0, 1, 0)

    # Equação do Plano de Sombra: Ax + By + Cz + D = 0
    # 0x + 1y + 0z + 0.99 = 0 => Plano = [0, 1, 0, 0.99]
    plano_sombra = [0.0, 1.0, 0.0, 0.99]
    posicao_luz_base = [0.0, 4.0, 2.0, 1.0]

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz_base)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        desenhar_chao()

        glPushMatrix()
        glTranslatef(0.0, 1.0, 0.0) # Levanta o cubo do chão
        glRotatef(rotacao_objeto, 1, 1, 0)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.1, 0.6, 0.9, 1.0]) # Cor Azul
        desenhar_cubo()
        glPopMatrix()

        # desliga a iluminação para que a sombra seja totalmente escura
        glDisable(GL_LIGHTING)
        
        # Habilitamos Blending para criar transparência 
        # (necessário para a sombra suave e realista)
        glEnable(GL_BLEND)
        # glBlendFunc: Define como misturar a cor que estamos desenhando com o que já está na tela
        # GL_SRC_ALPHA e GL_ONE_MINUS_SRC_ALPHA é a fórmula clássica para transparência
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        if modo_sombra == 1:
            # SOMBRA DURA: Desenhamos 1 única sombra bem escura
            amostras = 1
            alpha = 0.7 # 70% opaco
        else:
            # SOMBRA SUAVE: Simulamos uma Area Light desenhando 25 sombras suaves 
            amostras = 25
            alpha = 0.04 # 4% opaco por sombra

        glColor4f(0.0, 0.0, 0.0, alpha)

        for i in range(amostras):
            pos_luz_atual = posicao_luz_base[:]
            
            if modo_sombra == 2:
                raio_luz = 1.0 # O "tamanho" físico da nossa luz de área
                pos_luz_atual[0] += random.uniform(-raio_luz, raio_luz)
                pos_luz_atual[2] += random.uniform(-raio_luz, raio_luz)

            # Matriz que projeta os vértices
            matriz_sombra = calcular_matriz_sombra(plano_sombra, pos_luz_atual)

            glPushMatrix()
            # glMultMatrixf: Multiplica a matriz atual pela nossa matriz de esmagamento
            glMultMatrixf(matriz_sombra)
            
            # as exatas mesmas transformações do objeto real
            glTranslatef(0.0, 1.0, 0.0)
            glRotatef(rotacao_objeto, 1, 1, 0)
            
            desenhar_cubo()
            glPopMatrix()

        # Restaura o estado normal para o próximo frame
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)

        rotacao_objeto += 1.0
        
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()