
import pygame
import random
import math

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

LARGURA = 1000
ALTURA = 700

QUANTIDADE_PARTICULAS = 700

FPS = 60

# Localizacao do emissor
EMISSOR_X = 0.0
EMISSOR_Y = -4.0
EMISSOR_Z = 0.0

# Limites da regiao de emissao
LARGURA_EMISSAO = 1.5

# Intensidade da forca que impulsiona as particulas para cima
ACELERACAO_VERTICAL = 1.5

# Gravidade visual simplificada
GRAVIDADE = -1.5

class Particula:

    def __init__(self):
        self.reiniciar()

        # Distribui as idades iniciais
        self.idade = random.uniform(0, self.vida)

        # Recalcula a posicao inicial conforme a idade
        self.calcular_estado()


    def reiniciar(self):
        # Posicao inicial.
        self.x = EMISSOR_X + random.uniform(
            -LARGURA_EMISSAO / 2,
            LARGURA_EMISSAO / 2
        )

        self.y = EMISSOR_Y
        self.z = random.uniform(-0.3, 0.3)

        # Velocidades iniciais
        self.vx = random.uniform(-0.7, 0.7)
        self.vy = random.uniform(2.5, 5.5)
        self.vz = random.uniform(-0.3, 0.3)

        # Aceleracoes
        self.ax = random.uniform(-0.5, 0.5)
        self.ay = random.uniform(
            GRAVIDADE,
            ACELERACAO_VERTICAL
        )
        self.az = 0.0

        # Tempo de vida
        self.vida = random.uniform(1.0, 2.2)

        # Idade inicial
        self.idade = 0.0

        # Tamanho inicial
        self.tamanho_inicial = random.uniform(4.0, 8.0)


    def calcular_estado(self):
        # Calcula a posicao da particula para uma idade
        # especifica, considerando aceleracao constante

        t = self.idade
        self.x += self.vx * t + 0.5 * self.ax * t ** 2
        self.y += self.vy * t + 0.5 * self.ay * t ** 2
        self.z += self.vz * t

    # ATUALIZACAO FISICA
    def atualizar(self, dt):
        self.idade += dt

        # Verifica se a particula terminou sua vida
        if self.idade >= self.vida:
            self.reiniciar()
            return

        # Atualiza velocidade
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.vz += self.az * dt

        # Pequena oscilacao horizontal
        # Ajuda a produzir um movimento semelhante ao das chamas
        oscilacao = math.sin(self.idade * 8.0) * 0.4

        # Atualiza posicao
        self.x += (self.vx + oscilacao) * dt
        self.y += self.vy * dt
        self.z += self.vz * dt

    # CALCULO DA COR
    def obter_cor(self):
        progresso = self.idade / self.vida

        # Inicio: amarelo intenso
        if progresso < 0.25:

            vermelho = 1.0
            verde = 0.95
            azul = 0.2

        # Meio: amarelo para laranja
        elif progresso < 0.60:
            t = (progresso - 0.25) / 0.35

            vermelho = 1.0
            verde = 0.95 - 0.55 * t
            azul = 0.05

        # Final: laranja para vermelho
        else:
            t = (progresso - 0.60) / 0.40

            vermelho = 1.0
            verde = 0.40 * (1.0 - t)
            azul = 0.0

        # Transparencia diminui com a idade
        alpha = 1.0 - progresso

        return vermelho, verde, azul, alpha

    # TAMANHO DA PARTICULA
    def obter_tamanho(self):
        progresso = self.idade / self.vida

        # A particula aumenta ligeiramente de tamanho
        return self.tamanho_inicial * (1.0 + progresso)


# CRIACAO DAS PARTICULAS
particulas = []

for i in range(QUANTIDADE_PARTICULAS):
    particulas.append(Particula())

def configurar_opengl():

    # Define a area de renderizacao
    glViewport(0, 0, LARGURA, ALTURA)

    # Seleciona a matriz de projecao
    glMatrixMode(GL_PROJECTION)

    # Reinicializa a matriz
    glLoadIdentity()

    # Configura projecao em perspectiva
    gluPerspective(
        45,
        LARGURA / ALTURA,
        0.1,
        100
    )

    # Seleciona a matriz de modelo e visualizacao
    glMatrixMode(GL_MODELVIEW)

    # Habilita teste de profundidade
    glEnable(GL_DEPTH_TEST)

    # Habilita mistura de cores
    glEnable(GL_BLEND)

    # Mistura aditiva para produzir aparencia luminosa
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)

    # Suaviza os pontos, quando suportado
    glEnable(GL_POINT_SMOOTH)

    # Define tamanho dos pontos
    glPointSize(6)

    # Fundo preto
    glClearColor(0, 0, 0, 1)


# ATUALIZACAO DO SISTEMA
def atualizar_sistema(dt):
    for particula in particulas:
        particula.atualizar(dt)


# RENDERIZACAO
def desenhar_particulas():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Posicionamento da camera
    gluLookAt(
        0, 1, 16,
        0, 1, 0,
        0, 1, 0
    )

    for particula in particulas:
        r, g, b, alpha = particula.obter_cor()

        glPointSize(particula.obter_tamanho())

        glBegin(GL_POINTS)
        
        glColor4f(r, g, b, alpha)
        glVertex3f(particula.x, particula.y, particula.z)

        glEnd()

def main():

    pygame.init()

    pygame.display.set_mode(
        (LARGURA, ALTURA),
        DOUBLEBUF | OPENGL
    )

    pygame.display.set_caption(
        "Sistema de Particulas - Simulacao de Fogo"
    )

    configurar_opengl()

    relogio = pygame.time.Clock()

    executando = True

    while executando:

        # Calcula o tempo entre os quadros
        dt = relogio.tick(FPS) / 1000.0

        # Limita o intervalo
        dt = min(dt, 0.05)

        # Eventos
        for evento in pygame.event.get():

            if evento.type == QUIT:
                executando = False

            if evento.type == KEYDOWN:

                if evento.key == K_ESCAPE:
                    executando = False

        # Atualiza fisica
        atualizar_sistema(dt)

        # Limpa os buffers
        glClear(
            GL_COLOR_BUFFER_BIT |
            GL_DEPTH_BUFFER_BIT
        )

        # Renderiza
        desenhar_particulas()

        # Apresenta a imagem
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
