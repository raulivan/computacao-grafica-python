import glfw
from OpenGL.GL import *
import numpy as np

def desenhar_letra_F(r, g, b):
    """Desenha letra F na origem"""
    glColor3f(r, g, b) # Define a cor do objeto
    glBegin(GL_QUADS)
    
    # Tronco vertical
    glVertex2f(0.0, 0.0);  glVertex2f(1.0, 0.0)
    glVertex2f(1.0, 4.0);  glVertex2f(0.0, 4.0)
    
    # Traço superior
    glVertex2f(1.0, 3.0);  glVertex2f(3.0, 3.0)
    glVertex2f(3.0, 4.0);  glVertex2f(1.0, 4.0)
    
    # Traço do meio
    glVertex2f(1.0, 1.5);  glVertex2f(2.0, 1.5)
    glVertex2f(2.0, 2.5);  glVertex2f(1.0, 2.5)
    
    glEnd()

def desenhar_eixos_globais():
    """desenha um plano no fundo para marcar o X=0 e Y=0 do Universo"""
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_LINES)
    glVertex2f(-10, 0); glVertex2f(10, 0) # Eixo X
    glVertex2f(0, -10); glVertex2f(0, 10) # Eixo Y
    glEnd()

def main():
    if not glfw.init(): return
    
    janela = glfw.create_window(800, 800, "Transformações com OpenGL"
                                , None, None)
    if not janela: return glfw.terminate()
    
    glfw.make_context_current(janela)
    glfw.swap_interval(1)

    print("transformações geométricas...")

    while not glfw.window_should_close(janela):
        glfw.poll_events()
        
        # Fundo cinza escuro
        glClearColor(0.1, 0.1, 0.15, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Configuração da Visão Ortográfica
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Define que a janela vai do X(-10 a 10) e Y(-10 a 10)
        glOrtho(-10, 10, -10, 10, -1, 1)

        # Volta para a matriz de Modelagem
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        desenhar_eixos_globais()

        # Original
        glPushMatrix() # Salva a matriz limpa (origem)
        # Nenhuma transformação aplicada.
        desenhar_letra_F(0.5, 0.5, 0.5)
        glPopMatrix()  # Restaura a matriz limpa

        # Translação
        glPushMatrix()
        # Movemos o eixo para X=5, Y=5
        glTranslatef(5.0, 5.0, 0.0) 
        desenhar_letra_F(0.2, 0.6, 1.0)
        glPopMatrix()

        # Escala
        glPushMatrix()
        # Primeiro movemos para o quadrante inferior, DEPOIS escalamos.
        glTranslatef(5.0, -5.0, 0.0)
        glScalef(1.5, 0.5, 1.0) # Estica o X, achata o Y
        desenhar_letra_F(0.2, 1.0, 0.2)
        glPopMatrix()

        # Rotação
        glPushMatrix()
        glTranslatef(-5.0, 5.0, 0.0)
        # Gira 45 graus ao redor do eixo Z (0, 0, 1)
        glRotatef(45.0, 0.0, 0.0, 1.0)
        desenhar_letra_F(1.0, 0.8, 0.1)
        glPopMatrix()

        # REFLEXÃO / ESPELHAMENTO
        glPushMatrix()
        glTranslatef(-5.0, -5.0, 0.0)
        # X negativa espelha o objeto!
        glScalef(-1.0, 1.0, 1.0)
        desenhar_letra_F(1.0, 0.2, 0.2)
        glPopMatrix()

        # CISALHAMENTO / SHEAR
        glPushMatrix()
        glTranslatef(0.0, -8.0, 0.0)
        
        # matriz 4x4 (Array Linear de 16 posições)
        fator_cisalhamento_x = 1.2
        matriz_shear = np.array([
            1.0, 0.0, 0.0, 0.0, # Coluna 1
            fator_cisalhamento_x, 1.0, 0.0, 0.0, # Coluna 2 
            0.0, 0.0, 1.0, 0.0, # Coluna 3
            0.0, 0.0, 0.0, 1.0  # Coluna 4
        ], dtype=np.float32)
        
        # passa a matriz para placa de video
        glMultMatrixf(matriz_shear)
        
        desenhar_letra_F(0.8, 0.2, 1.0)
        glPopMatrix()

        glfw.swap_buffers(janela)

    glfw.terminate()

if __name__ == "__main__":
    main()