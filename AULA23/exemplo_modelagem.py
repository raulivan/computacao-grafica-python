import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

#  ESTRUTURA DE DADOS (Baseada em Índices/Vértices)

# Lista de vértices no espaço 3D
vertices = (
    ( 1, -1, -1), ( 1,  1, -1), (-1,  1, -1), (-1, -1, -1), # Face traseira
    ( 1, -1,  1), ( 1,  1,  1), (-1, -1,  1), (-1,  1,  1)  # Face frontal
)

# Lista de arestas: cada tupla contém os índices dos vértices que a formam.
# representação Aramada (Wireframe).
arestas = (
    (0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
    (6,3), (6,4), (6,7), (5,1), (5,4), (5,7)
)

# Lista de faces: cada tupla contém os índices dos vértices formando um polígono (quad).
# Representação por Faces. Note a ordem (sentido anti-horário).
faces = (
    (0,1,2,3), # Trás
    (3,2,7,6), # Esquerda
    (6,7,5,4), # Frente
    (4,5,1,0), # Direita
    (1,5,7,2), # Topo
    (4,0,3,6)  # Base
)

# cores para cada face
cores = (
    (1,0,0), (0,1,0), (0,0,1), (1,1,0), (1,0,1), (0,1,1)
)

# alternar os modos de representação
modo_wireframe = False

def desenha_cubo():
    global modo_wireframe
    
    if modo_wireframe:
        # glPolygonMode: Define como os polígonos serão renderizados.
        # GL_FRONT_AND_BACK: Aplica à frente e atrás das faces.
        # GL_LINE: Desenha apenas as bordas (Wireframe).
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        
        # glBegin: Inicia a definição de primitivas geométricas. 
        # GL_LINES diz ao OpenGL para tratar cada par de vértices como uma linha independente.
        glBegin(GL_LINES)
        glColor3fv((1, 1, 1)) # cor branca para as linhas
        for aresta in arestas:
            for vertice in aresta:
                # glVertex3fv: Define um vértice no espaço 3D usando um array/tupla de 3 floats.
                glVertex3fv(vertices[vertice])
        # glEnd: Encerra a definição geométrica iniciada pelo glBegin.
        glEnd()
        
    else:
        # GL_FILL: Preenche o interior do polígono (Representação por Faces/Superfícies)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        # GL_QUADS: Trata cada conjunto de 4 vértices como um quadrilátero isolado.
        glBegin(GL_QUADS)
        for i, face in enumerate(faces):
            # glColor3fv: Define a cor atual da máquina de estados do OpenGL.
            glColor3fv(cores[i])
            for vertice in face:
                glVertex3fv(vertices[vertice])
        glEnd()

# Função para alternar a representação
def key_callback(window, key, scancode, action, mods):
    global modo_wireframe
    # quando a barra de espaço for pressionada, inverte o modo
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        modo_wireframe = not modo_wireframe

def main():
    # Inicializa a biblioteca GLFW
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 600, "Sólido vs Wireframe (Espaço para trocar)", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    # Configuração de perspectiva da câmera
    gluPerspective(45, (800/600), 0.1, 50.0)
    # glTranslatef: Multiplica a matriz atual por uma matriz de translação. 
    glTranslatef(0.0, 0.0, -5)

    # Habilita o teste de profundidade para que faces de trás não desenhem por cima das da frente
    glEnable(GL_DEPTH_TEST)

    rotacao = 0

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # glPushMatrix: Salva o estado atual da matriz de transformação na pilha.
        glPushMatrix()
        
        # glRotatef: Rotaciona o objeto. Parâmetros: ângulo, vetor eixo x, y, z.
        # Aqui giramos nos eixos X e Y simultaneamente para ver todas as faces.
        glRotatef(rotacao, 1, 1, 0)
        
        desenha_cubo()
        
        # glPopMatrix: Restaura a matriz salva pelo glPushMatrix.
        glPopMatrix()
        
        rotacao += 1 # Incrementa a rotação para o próximo frame
        
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()