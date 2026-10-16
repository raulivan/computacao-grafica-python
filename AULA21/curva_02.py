import glfw
from OpenGL.GL import *
import numpy as np
import math

def desenhar_conjunto_pontos():
    """ 
    conjuto de potnos
    """
    glColor3f(1.0, 0.5, 0.0) # Laranja
    pontos = [
        (-4.0, -2.0), (-2.0, 1.0), (0.0, 0.0), 
        (1.5, 2.5), (3.0, -1.0), (4.0, 3.0)
    ]
    
    # conecta todos os vértices em uma linha contínua
    glBegin(GL_LINE_STRIP)
    for p in pontos:
        glVertex2f(p[0], p[1])
    glEnd()

    # Desenhando bolinhas brancas mostrar pontos conectados
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(5.0)
    glBegin(GL_POINTS)
    for p in pontos:
        glVertex2f(p[0], p[1])
    glEnd()

def desenhar_explicita():
    """
    y = f(x)
    função Seno: y = sin(x) * amplitude
    """
    glColor3f(0.0, 1.0, 0.0) # Verde
    
    glBegin(GL_LINE_STRIP)
    # avança no eixo X 
    for x in np.arange(-4.0, 4.0, 0.1):
        y = math.sin(x * 1.5) * 2.0 # f(x)
        glVertex2f(x, y)
    glEnd()

def desenhar_implicita():
    """
    x² + y² - r² = 0 (Círculo)
    """
    glColor3f(1.0, 0.0, 0.0) # Vermelho
    raio_quadrado = 3.0 ** 2
    tolerancia = 0.5 # margem de erro
    
    glPointSize(2.0)
    glBegin(GL_POINTS)
    
    # Varremos chutando valores
    for x in np.arange(-4.0, 4.0, 0.1):
        for y in np.arange(-4.0, 4.0, 0.1):
            equacao = (x**2) + (y**2) - raio_quadrado
            # Se o resultado for muito próximo de ZERO
            if abs(equacao) < tolerancia:
                glVertex2f(x, y)
    glEnd()

def desenhar_parametrica():
    """
    x = f(t), y = g(t)
    uma Espiral
    """
    glColor3f(0.0, 0.8, 1.0) 
    
    glBegin(GL_LINE_STRIP)
    # t representa o ângulo variando de 0 a 6*PI (3 voltas completas)
    for t in np.arange(0.0, 6 * math.pi, 0.1):
        raio_crescente = 0.2 * t
        x = raio_crescente * math.cos(t)
        y = raio_crescente * math.sin(t)
        
        glVertex2f(x, y)
    glEnd()


def desenhar_eixos():
    """Desenha a cruz central dividindo os 4 quadrantes"""
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_LINES)
    glVertex2f(-10, 0); glVertex2f(10, 0)
    glVertex2f(0, -10); glVertex2f(0, 10)
    glEnd()

def main():
    if not glfw.init(): return
    janela = glfw.create_window(800, 800, "Representações de Curvas", None, None)
    if not janela: return glfw.terminate()
    glfw.make_context_current(janela)
    glfw.swap_interval(1)

    print("iniciado...")

    while not glfw.window_should_close(janela):
        glfw.poll_events()
        glClearColor(0.05, 0.05, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Câmera 2D Ortográfica (-10 a 10)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-10, 10, -10, 10, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        desenhar_eixos()

        # Topo Direito: Paramétrica (Espiral)
        glPushMatrix()
        glTranslatef(5.0, 5.0, 0.0)
        desenhar_parametrica()
        glPopMatrix()

        # Topo Esquerdo: Explícita (Seno Verde)
        glPushMatrix()
        glTranslatef(-5.0, 5.0, 0.0)
        desenhar_explicita()
        glPopMatrix()

        # Inferior Esquerdo: Implícita (Círculo Vermelho)
        glPushMatrix()
        glTranslatef(-5.0, -5.0, 0.0)
        desenhar_implicita()
        glPopMatrix()

        # Inferior Direito: Conjunto de Pontos (Laranja)
        glPushMatrix()
        glTranslatef(5.0, -5.0, 0.0)
        desenhar_conjunto_pontos()
        glPopMatrix()

        glfw.swap_buffers(janela)
        # fim while not glfw.window_should_close(janela):

    glfw.terminate()
    # fim main

if __name__ == "__main__":
    main()