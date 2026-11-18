import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

rotacao_y = 0.0
def configurar_iluminacao():
    # GL_LIGHTING avisa o OpenGL para ignorar o glColor simples e calcular 
    # as cores baseadas nas equações de luz, normais e materiais
    glEnable(GL_LIGHTING)
    
    # Habilita a luz de índice 0 (O OpenGL permite de GL_LIGHT0 até GL_LIGHT7)
    glEnable(GL_LIGHT0)
    
    glEnable(GL_DEPTH_TEST)
    
    # Define como a cor base do objeto interage com a luz (Gouraud Shading por padrão)
    glShadeModel(GL_SMOOTH)

    # Configurando a Fonte de Luz (GL_LIGHT0)    
    # Luz ambiente: Luz fraca que preenche a cena (Cinza escuro)
    luz_ambiente = [0.2, 0.2, 0.2, 1.0]
    
    # Luz difusa: A cor principal da luz batendo no objeto (Branca)
    luz_difusa = [0.8, 0.8, 0.8, 1.0]
    
    # Luz especular: A cor do "brilho" refletido (Branco puro)
    luz_especular = [1.0, 1.0, 1.0, 1.0]
    
    # Posição da luz: (X, Y, Z, W). 
    # Se W=1.0, é uma luz pontual (como lâmpada)
    # Se W=0.0, é uma luz direcional (como o Sol, vindo do infinito)
    posicao_luz = [2.0, 2.0, 2.0, 1.0]

    # glLightfv: Envia vetores (f de float, v de vector) 
    # para configurar propriedades de uma luz.
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
    glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)
    glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)


def configurar_material():
    # Material reage à luz. Vamos criar um tipo de plástico vermelho que brilha
    
    mat_ambiente = [0.2, 0.0, 0.0, 1.0]   # Como ele reflete a luz ambiente
    mat_difuso = [0.8, 0.0, 0.0, 1.0]     # A cor fosca predominante (Vermelho)
    mat_especular = [1.0, 1.0, 1.0, 1.0]  # O material reflete brilho branco
    
    # Shininess (Brilho): Vai de 0 a 128 no OpenGL fixo.
    # Valores altos = reflexo pequeno e concentrado (como metal/vidro)
    # Valores baixos = reflexo espalhado (como plástico fosco)
    mat_shininess = [50.0]

    # glMaterialfv: Define como os próximos vértices desenhados vão reagir à luz
    # GL_FRONT aplica o material apenas às faces viradas para a câmera
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambiente)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_difuso)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_especular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)

def desenhar_esfera():
    # Para interagir com a luz, todo vértice DEVE ter um Vetor Normal associado
    # A normal aponta para onde a face "olha"
    # O utilitário GLU já calcula as normais de uma esfera automaticamente
    
    # gluNewQuadric: Cria um objeto auxiliar do GLU para desenhar formas curvas
    quadric = gluNewQuadric()
    
    # gluQuadricNormals: Diz ao GLU para gerar normais suaves (Gouraud)
    gluQuadricNormals(quadric, GLU_SMOOTH)
    
    # gluSphere: Desenha a esfera
    # quadric, raio (1.0), fatias horizontais (32), fatias verticais (32).
    # Quanto mais fatias, mais redondo fica
    gluSphere(quadric, 1.0, 32, 32)
    
    gluDeleteQuadric(quadric)

def main():
    global rotacao_y

    if not glfw.init():
        return
    
    window = glfw.create_window(800, 600, 
                                "Modelo de Iluminação de Phong (PyOpenGL)"
                                , None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Configuração de perspectiva
    gluPerspective(45, (800/600), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -4.0) # Afasta a câmera

    # Inicializa luzes e propriedades da cena
    configurar_iluminacao()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        
        # Rotaciona a esfera no eixo Y
        # Ao girar, você notará que o brilho especular (ponto branco) permanece 
        # voltado para a luz estática
        glRotatef(rotacao_y, 0, 1, 0)
        
        configurar_material()
        desenhar_esfera()
        
        glPopMatrix()
        
        rotacao_y += 0.5
        
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()