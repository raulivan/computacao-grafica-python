import glfw
from OpenGL.GL import *
import math

def desenhar_chao():
    """GL_QUADS: 
       Conecta 4 vértices para formar um quadrado/retângulo
    """
    glColor3f(0.1, 0.6, 0.2) # Verde escuro
    
    glBegin(GL_QUADS)
    glVertex2f(-1.0, -1.0) # Canto inferior esquerdo
    glVertex2f( 1.0, -1.0) # Canto inferior direito
    glVertex2f( 1.0, -0.2) # Canto superior direito
    glVertex2f(-1.0, -0.2) # Canto superior esquerdo
    glEnd()

def desenhar_montanhas():
    """GL_TRIANGLES: 
    Conecta vértices de 3 em 3 para formar triângulos independentes"""
    glColor3f(0.5, 0.5, 0.5) # Cinza
    
    glBegin(GL_TRIANGLES)
    # Montanha Esquerda (Vértices 1, 2 e 3)
    glVertex2f(-1.0, -0.2)
    glVertex2f(-0.5,  0.5)
    glVertex2f( 0.0, -0.2)
    
    # Montanha Direita (Vértices 4, 5 e 6)
    glColor3f(0.4, 0.4, 0.4) 
    glVertex2f(-0.2, -0.2)
    glVertex2f( 0.4,  0.4)
    glVertex2f( 1.0, -0.2)
    glEnd()

def desenhar_sol(centro_x, centro_y, raio):
    """GL_POLYGON: 
    Conecta dezenas de vértices em um círculo fechado"""
    glColor3f(1.0, 0.8, 0.1) # Amarelo
    
    glBegin(GL_POLYGON)
    # gerar 30 vértices em formato de círculo
    segmentos = 30
    for i in range(segmentos):
        angulo = 2.0 * math.pi * i / segmentos
        x = centro_x + (math.cos(angulo) * raio)
        # multiplicamos por 1.3 no Y para corrigir a distorção da tela retangular 
        y = centro_y + (math.sin(angulo) * raio * 1.3)
        glVertex2f(x, y)
    glEnd()

def desenhar_passaros():
    """GL_LINES: 
    Conecta vértices de 2 em 2 para formar linhas retas"""
    glColor3f(0.0, 0.0, 0.0) # Preto
    glLineWidth(2.0) # Aumenta a espessura da linha
    
    glBegin(GL_LINES)
    # Pássaro 1 (Esquerda)
    glVertex2f(-0.5, 0.7);  glVertex2f(-0.4, 0.8)
    # Pássaro 1 (Esquerda)
    glVertex2f(-0.4, 0.8);  glVertex2f(-0.3, 0.7)
    
    # Pássaro 2 (Direita)
    glVertex2f(0.2, 0.6);   glVertex2f(0.3, 0.7)
    # Pássaro 2 (Direita)
    glVertex2f(0.3, 0.7);   glVertex2f(0.4, 0.6)
    glEnd()

def desenhar_estrelas():
    """GL_POINTS"""
    glColor3f(1.0, 1.0, 1.0) # Branco
    glPointSize(3.0) # Faz o ponto ter 3x3 pixels de tamanho
    
    glBegin(GL_POINTS)
    glVertex2f(-0.8, 0.9)
    glVertex2f(-0.6, 0.7)
    glVertex2f( 0.0, 0.85)
    glVertex2f( 0.8, 0.9)
    glVertex2f( 0.6, 0.7)
    glEnd()

def main():
    if not glfw.init(): return
    
    janela = glfw.create_window(800, 600, "Dicionário de Funções OpenGL"
                                , None, None)
    if not janela: return glfw.terminate()
    glfw.make_context_current(janela)
    glfw.swap_interval(1)

    # Função de Configuração de Estado
    glClearColor(0.1, 0.2, 0.4, 1.0)

    print("paisagem usando 5 primitivas diferentes.")

    while not glfw.window_should_close(janela):
        glfw.poll_events()
        
        # Limpa o framebuffer com a cor que definimos acima
        glClear(GL_COLOR_BUFFER_BIT)

        # Ordem de desenho importa 
        # O que é desenhado primeiro fica no fundo
        desenhar_estrelas()   # 1º Plano mais profundo
        desenhar_sol(0.5, 0.6, 0.15) # 2º
        desenhar_montanhas()  # 3º
        desenhar_chao()       # 4º
        desenhar_passaros()   # 5º Fica na frente de tudo

        glfw.swap_buffers(janela)

    glfw.terminate()

if __name__ == "__main__":
    main()