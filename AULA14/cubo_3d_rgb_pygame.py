import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def main():
    print("=== Laboratório de Hardware: Cubo RGB em OpenGL ===\n")
    
    #  Contexto Gráfico
    pygame.init()
    resolucao = (800, 600)
    
    pygame.display.set_mode(resolucao, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Motor 3D: Cubo RGB")

    # Configuração da Matriz de Projeção (A Câmera 3D)
    # gluPerspective(angulo_visao, proporcao_tela, distancia_minima, distancia_maxima)
    gluPerspective(45, (resolucao[0] / resolucao[1]), 0.1, 50.0)

    # Configuração do Z-Buffer (Teste de Profundidade) - NÃO desenhar faces de trás por cima das da frente
    glEnable(GL_DEPTH_TEST)

    # Movemos a "Câmera" 3 unidades para trás no eixo Z para enxergarmos o cubo
    glTranslatef(0.0, 0.0, -3)

    # Definição da Geometria e Cor (SRO - Espaço do Objeto)
    #  os 8 vértices de um cubo unitário (de 0.0 a 1.0)
    # A magia aqui é que as coordenadas (X, Y, Z) SÃO os valores (R, G, B)!
    vertices_e_cores = (
        (0, 0, 0), # 0: Preto (Origem)
        (1, 0, 0), # 1: Vermelho
        (1, 1, 0), # 2: Amarelo
        (0, 1, 0), # 3: Verde
        (0, 0, 1), # 4: Azul
        (1, 0, 1), # 5: Magenta
        (1, 1, 1), # 6: Branco
        (0, 1, 1)  # 7: Ciano
    )

    # os vértices se ligam para formar as 6 faces quadradas (Quads)
    faces = (
        (0, 1, 2, 3), # Face Z- (Traseira)
        (3, 2, 6, 7), # Face Y+ (Topo)
        (7, 6, 5, 4), # Face Z+ (Frontal)
        (4, 5, 1, 0), # Face Y- (Base)
        (1, 5, 6, 2), # Face X+ (Direita)
        (4, 0, 3, 7)  # Face X- (Esquerda)
    )

   
    rodando = True
    while rodando:
        # Verifica se o usuário clicou no X para fechar a janela
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        # Limpa a memória de cor (Framebuffer) e a memória de profundidade (Z-Buffer)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Aplica a Rotação Contínua na Matriz Global
        # Gira 1 grau por frame em torno de um vetor diagonal (1, 1, 1)
        glRotatef(1, 1, 1, 1)

        # Isolamento de Matriz (Push / Pop)
        # Salvamos o estado atual, movemos o cubo para que seu centro de gravidade (0.5, 0.5, 0.5)
        # vá para a origem, forçando a rotação a ocorrer no PRÓPRIO EIXO (como vimos na aula passada).
        glPushMatrix()
        glTranslatef(-0.5, -0.5, -0.5)

        # Envio de Dados para a GPU (Desenho)
        glBegin(GL_QUADS) # Avisamos a GPU que enviaremos quadrados
        for face in faces:
            for vertice_id in face:
                # Extraímos os dados da nossa tupla
                dados = vertices_e_cores[vertice_id]
                
                # Injetamos a cor (R, G, B) e logo em seguida a coordenada (X, Y, Z)
                glColor3fv(dados)
                glVertex3fv(dados)
        glEnd() # Fim da transmissão geométrica

        glPopMatrix() # Restauramos a matriz original

        # Swap Buffers
        # Troca a tela que estava sendo desenhada em segundo plano pela tela visível
        pygame.display.flip()
        
        # Limita a 60 FPS 
        pygame.time.wait(16)

    pygame.quit()

if __name__ == "__main__":
    main()