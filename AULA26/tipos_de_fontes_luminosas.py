import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

rotacao_y = 0.0
modo_luz = 1 # 1: Direcional, 2: Pontual, 3: Spot

def aplicar_luz():
    # Luz base para o ambiente não ficar no breu total kkk
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    
    if modo_luz == 1:
        # LUZ DIRECIONAL (Teclado 1)
        # O valor 0.0 no final (W) indica que é uma luz do infinito
        # Os valores (1.0, 1.0, 1.0) formam o vetor de onde a luz VEM
        posicao_direcional = [1.0, 1.0, 1.0, 0.0]
        glLightfv(GL_LIGHT0, GL_POSITION, posicao_direcional)
        
        # Desliga o efeito Spot atribuindo o ângulo de corte máximo (180)
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 180.0)
        
    elif modo_luz == 2:
        # LUZ PONTUAL (Teclado 2)
        # O valor 1.0 no final (W) fixa a luz na coordenada (0.0, 2.0, 0.0)
        # Ela está posicionada acima do objeto e emite para todos os lados
        posicao_pontual = [0.0, 2.0, 0.0, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, posicao_pontual)
        
        # Desliga o efeito Spot
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 180.0)
        
        # Atenuação: Reduz a força da luz conforme a distância
        # Equação: 1 / (c + l*d + q*d^2) onde d é a distância
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.5)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.1)
        
    elif modo_luz == 3:
        # LUZ SPOT (Teclado 3)
        # Primeiro, define-se como uma luz pontual (W=1.0)
        posicao_spot = [0.0, 3.0, 0.0, 1.0] 
        glLightfv(GL_LIGHT0, GL_POSITION, posicao_spot)
        
        # GL_SPOT_DIRECTION: Vetor apontando para baixo (Eixo Y negativo)
        direcao_spot = [0.0, -1.0, 0.0]
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, direcao_spot)
        
        # GL_SPOT_CUTOFF: Ângulo do cone a partir do centro (ex: 20 graus gera um cone de 40 graus totais)
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 20.0)
        
        # GL_SPOT_EXPONENT: Suavidade da borda do feixe de luz (quanto maior, mais focado o centro)
        glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 15.0)

def desenhar_chao():
    # Material do chão (Azul fosco)
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0, 0.1, 0.2, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.0, 0.3, 0.6, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, [0.0])

    # Tesselando o chão: Dividindo um grande plano em vários pequenos quadrados
    glBegin(GL_QUADS)
    
    # glNormal3f:O chão aponta para cima (Eixo Y)
    glNormal3f(0.0, 1.0, 0.0) 
    
    tamanho = 10
    passo = 0.5 # Tamanho de cada subdivisão
    x = -tamanho
    while x < tamanho:
        z = -tamanho
        while z < tamanho:
            glVertex3f(x, -1.0, z)
            glVertex3f(x + passo, -1.0, z)
            glVertex3f(x + passo, -1.0, z + passo)
            glVertex3f(x, -1.0, z + passo)
            z += passo
        x += passo
    glEnd()

def desenhar_esfera():
    # Material da esfera (Vermelho brilhante)
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.1, 0.1, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, [50.0])

    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.0) # Centro da cena
    gluSphere(quadric, 1.0, 32, 32)
    glPopMatrix()
    
    gluDeleteQuadric(quadric)

def key_callback(window, key, scancode, action, mods):
    global modo_luz
    if action == glfw.PRESS:
        if key == glfw.KEY_1:
            modo_luz = 1
            print("Modo: Luz Direcional")
        elif key == glfw.KEY_2:
            modo_luz = 2
            print("Modo: Luz Pontual (Atenuada)")
        elif key == glfw.KEY_3:
            modo_luz = 3
            print("Modo: Luz Spot (Cone focado)")

def main():
    global rotacao_y

    if not glfw.init():
        return
    
    window = glfw.create_window(800, 600, "1: Direcional | 2: Pontual | 3: Spot", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    # Configuração de câmera
    gluPerspective(45, (800/600), 0.1, 50.0)
    
    # Facilita posicionar a câmera
    # Pos (x,y,z), Alvo (x,y,z), Cima (x,y,z)
    gluLookAt(0, 4, 8,   # Câmera um pouco alta e afastada
              0, 0, 0,   # Olhando para o centro
              0, 1, 0)   # Eixo Y é "para cima"

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Aplica a luz escolhida no frame atual
        aplicar_luz()
        
        # Desenha cenário estático
        desenhar_chao()
        
        # Desenha a esfera rotacionando para ver o brilho especular se movendo
        glPushMatrix()
        glRotatef(rotacao_y, 0, 1, 0)
        desenhar_esfera()
        glPopMatrix()
        
        rotacao_y += 0.5
        
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()