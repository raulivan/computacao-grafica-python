
import math
import glfw

from OpenGL.GL import *
from OpenGL.GLU import *

# dEFINIÇÃO DO MODELO GEOMÉTRICO

# Cada vértice possui três coordenadas: x, y e z.
# O cubo tem lado 2 e está centralizado na origem.
vertices = [
    (-1, -1, -1),  # 0
    ( 1, -1, -1),  # 1
    ( 1,  1, -1),  # 2
    (-1,  1, -1),  # 3
    (-1, -1,  1),  # 4
    ( 1, -1,  1),  # 5
    ( 1,  1,  1),  # 6
    (-1,  1,  1)   # 7
]

# Cada face referencia quatro índices da lista de vértices.
faces = [
    (0, 3, 2, 1),  # Inferior
    (4, 5, 6, 7),  # Superior
    (0, 1, 5, 4),  # Frontal
    (3, 7, 6, 2),  # Posterior
    (0, 4, 7, 3),  # Lateral esquerda
    (1, 2, 6, 5)   # Lateral direita
]

# As doze arestas do cubo são definidas pelos pares de índices.
arestas = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

modo = 1
rotacao = 0.0


def desenhar_faces():
    # glBegin(GL_QUADS) inicia a especificação de quadriláteros.
    glBegin(GL_QUADS)

    for face in faces:
        for indice in face:
            # glVertex3fv envia um vértice com três coordenadas.
            # O OpenGL conecta os vértices na ordem fornecida.
            glVertex3fv(vertices[indice])
    # glEnd() encerra o envio desses vértices.
    glEnd()
    # FIM desenhar_faces


def desenhar_arestas():
    # GL_LINES interpreta cada par de vértices como uma linha.
    glBegin(GL_LINES)

    for a, b in arestas:
        glVertex3fv(vertices[a])
        glVertex3fv(vertices[b])

    glEnd()


def desenhar_vertices():
    # glPointSize define o tamanho dos pontos em pixels.
    glPointSize(8)

    # GL_POINTS desenha cada vértice como um ponto independente.
    glBegin(GL_POINTS)

    for vertice in vertices:
        glVertex3fv(vertice)

    glEnd()
    # FIM desenhar_vertices


def desenhar_cubo_solido():
    # Desenha primeiro as faces preenchidas e depois as arestas.
    glColor3f(0.25, 0.65, 0.95)
    desenhar_faces()

    glColor3f(0.05, 0.05, 0.05)
    glLineWidth(2)
    desenhar_arestas()
    # FIM desenhar_cubo_solido


# REPRESENTAÇÃO POR OCUPAÇÃO ESPACIAL (VOXELS)

def desenhar_voxel(x, y, z, tamanho):
    # Cria os oito vértices de um pequeno cubo.
    h = tamanho / 2
    pontos = [
        (x-h, y-h, z-h), (x+h, y-h, z-h),
        (x+h, y+h, z-h), (x-h, y+h, z-h),
        (x-h, y-h, z+h), (x+h, y-h, z+h),
        (x+h, y+h, z+h), (x-h, y+h, z+h)
    ]
    # Faces locais de cada voxel.
    faces_voxel = [
        (0, 3, 2, 1), (4, 5, 6, 7),
        (0, 1, 5, 4), (3, 7, 6, 2),
        (0, 4, 7, 3), (1, 2, 6, 5)
    ]
    glBegin(GL_QUADS)
    for face in faces_voxel:
        for indice in face:
            glVertex3fv(pontos[indice])
    glEnd()
    # FIM desenhar_voxel

def desenhar_voxels():
    # Grade 3x3x3: 
    # ocupamos as células cujos centros estão
    # dentro de uma esfera de raio 1.25.

    tamanho = 0.55
    passo = 0.65

    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                x = i * passo
                y = j * passo
                z = k * passo
                distancia = math.sqrt(x*x + y*y + z*z)

                # Uma célula é está ocupada quando
                # seu centro está dentro da esfera .
                if distancia <= 1.25:
                    glColor3f(0.25, 0.75, 0.55)
                    desenhar_voxel(x, y, z, tamanho)

                    # Contorno de cada voxel
                    glColor3f(0.05, 0.25, 0.15)

                    h = tamanho / 2
                    pontos = [
                        (x-h, y-h, z-h), (x+h, y-h, z-h),
                        (x+h, y+h, z-h), (x-h, y+h, z-h),
                        (x-h, y-h, z+h), (x+h, y-h, z+h),
                        (x+h, y+h, z+h), (x-h, y+h, z+h)
                    ]

                    glBegin(GL_LINES)

                    for a, b in arestas:
                        glVertex3fv(pontos[a])
                        glVertex3fv(pontos[b])

                    glEnd()
    # FIM desenhar_voxels

def teclado(janela, tecla, scancode, acao, mods):
    global modo
    # GLFW_PRESS indica que a tecla foi pressionada.
    if acao == glfw.PRESS:
        if tecla == glfw.KEY_1:
            modo = 1
        elif tecla == glfw.KEY_2:
            modo = 2
        elif tecla == glfw.KEY_3:
            modo = 3
        elif tecla == glfw.KEY_4:
            modo = 4
        elif tecla == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(janela, True)
    # FIM teclado


def main():
    if not glfw.init():
        raise RuntimeError("Não foi possível inicializar o GLFW.")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

    janela = glfw.create_window( 1000, 700,
        "Representacao e Modelagem", None, None
    )

    if not janela:
        glfw.terminate()
        raise RuntimeError("Não foi possível criar a janela.")

    glfw.make_context_current(janela)
    glfw.set_key_callback(janela, teclado)
    # glEnable ativa um recurso do OpenGL.
    # GL_DEPTH_TEST permite testar a profundidade dos fragmentos,
    # evitando que superfícies mais distantes ocultem as próximas.
    glEnable(GL_DEPTH_TEST)

    # glClearColor define a cor usada para limpar a janela.
    glClearColor(0.92, 0.94, 0.97, 1.0)

    # glMatrixMode seleciona qual matriz será modificada.
    # GL_PROJECTION representa a transformação de projeção.
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # gluPerspective cria uma projeção em perspectiva:
    # 45 graus de campo de visão, proporção da janela,
    # plano próximo 0.1 e plano distante 100.
    gluPerspective(45, 1000 / 700, 0.1, 100.0)

    # GL_MODELVIEW seleciona a matriz de visualização/modelagem.
    glMatrixMode(GL_MODELVIEW)

    while not glfw.window_should_close(janela):
        global rotacao

        # Limpa a imagem e o buffer de profundidade.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # O objeto é afastado da câmera para ficar visível.
        glTranslatef(0.0, 0.0, -6.0)

        # O ângulo é atualizado a cada quadro para criar animação.
        glRotatef(rotacao, 0.5, 1.0, 0.0)

        if modo == 1:
            # Representação aramada
            glColor3f(0.05, 0.25, 0.75)
            desenhar_arestas()
        elif modo == 2:
            # Representação por faces poligonais.
            glColor3f(0.25, 0.65, 0.95)
            desenhar_faces()
        elif modo == 3:
            # Representação dos vértices.
            glColor3f(0.85, 0.15, 0.15)
            desenhar_vertices()
        elif modo == 4:
            # Representação por enumeração de ocupação espacial.
            desenhar_voxels()

        glfw.swap_buffers(janela)
        glfw.poll_events()

        rotacao += 0.5

    # Libera os recursos da janela e encerra o GLFW.
    glfw.terminate()

if __name__ == "__main__":
    main()
