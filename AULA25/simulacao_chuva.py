
import pygame
import random

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


LARGURA = 1000
ALTURA = 700

QUANTIDADE_PARTICULAS = 800

FPS = 60

# Limites do emissor
EMISSOR_X_MIN = -10.0
EMISSOR_X_MAX = 10.0

EMISSOR_Y = 10.0

EMISSOR_Z_MIN = -5.0
EMISSOR_Z_MAX = 5.0

# Limite inferior da cena
LIMITE_INFERIOR = -10.0

# Gravidade
GRAVIDADE = -9.8

# Vento horizontal
VENTO = 0.8

class Particula:

    def __init__(self):
        self.reiniciar()

        # Distribui as gotas em diferentes alturas
        self.y = random.uniform(
            LIMITE_INFERIOR,
            EMISSOR_Y
        )


    def reiniciar(self):
        # Posicao inicial aleatoria
        self.x = random.uniform(
            EMISSOR_X_MIN,
            EMISSOR_X_MAX
        )

        self.y = EMISSOR_Y

        self.z = random.uniform(
            EMISSOR_Z_MIN,
            EMISSOR_Z_MAX
        )

        # Velocidade inicial
        self.vx = random.uniform(-0.3, 0.3)
        self.vy = random.uniform(-12.0, -8.0)
        self.vz = random.uniform(-0.1, 0.1)

        # Aceleracao
        self.ax = VENTO
        self.ay = GRAVIDADE
        self.az = 0.0

        # Comprimento da gota
        self.comprimento = random.uniform(0.2, 0.5)

        # Variacao de intensidade visual
        self.alpha = random.uniform(0.5, 1.0)

    # ATUALIZACAO DA PARTICULA
    def atualizar(self, dt):

        # Atualiza velocidades
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.vz += self.az * dt

        # Atualiza posicoes
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt

        # Verifica se a gota atingiu o limite inferior
        if self.y < LIMITE_INFERIOR:
            self.reiniciar()


    # EXTREMIDADES DO SEGMENTO DE CHUVA
    def obter_extremidades(self):
        # Quanto maior a velocidade, maior o rastro visual
        tamanho = self.comprimento * abs(self.vy) / 12.0

        # A extremidade superior
        inicio = (
            self.x,
            self.y,
            self.z
        )

        # A extremidade inferior
        fim = (
            self.x - self.vx * 0.015,
            self.y - tamanho,
            self.z
        )

        return inicio, fim

# CRIACAO DAS PARTICULAS
particulas = []

for i in range(QUANTIDADE_PARTICULAS):
    particulas.append(Particula())


def configurar_opengl():
    # Define a regiao de renderizacao
    glViewport(0, 0, LARGURA, ALTURA)

    # Matriz de projecao
    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    # Projecao em perspectiva
    gluPerspective(
        45,
        LARGURA / ALTURA,
        0.1,
        100
    )

    # Matriz de modelo e visualizacao
    glMatrixMode(GL_MODELVIEW)

    # Ativa teste de profundidade
    glEnable(GL_DEPTH_TEST)

    # Ativa mistura de cores
    glEnable(GL_BLEND)

    # Mistura convencional com transparencia
    glBlendFunc(
        GL_SRC_ALPHA,
        GL_ONE_MINUS_SRC_ALPHA
    )

    # Cor de fundo
    glClearColor(
        0.01,
        0.02,
        0.05,
        1.0
    )

    # Espessura dos segmentos
    glLineWidth(2.0)


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
        0, 0, 22,
        0, 0, 0,
        0, 1, 0
    )

    # Inicia o desenho de segmentos de reta
    glBegin(GL_LINES)

    for particula in particulas:
        # Cor azul clara
        glColor4f(
            0.65,
            0.80,
            1.0,
            particula.alpha
        )

        inicio, fim = particula.obter_extremidades()

        # Primeiro vertice
        glVertex3f(
            inicio[0],
            inicio[1],
            inicio[2]
        )

        # Segundo vertice
        glVertex3f(
            fim[0],
            fim[1],
            fim[2]
        )

    glEnd()


def main():

    pygame.init()

    pygame.display.set_mode(
        (LARGURA, ALTURA),
        DOUBLEBUF | OPENGL
    )

    pygame.display.set_caption(
        "Sistema de Particulas - Simulacao de Chuva"
    )

    configurar_opengl()

    relogio = pygame.time.Clock()

    executando = True

    while executando:

        # Tempo entre quadros
        dt = relogio.tick(FPS) / 1000.0

        dt = min(dt, 0.05)

        # Eventos
        for evento in pygame.event.get():

            if evento.type == QUIT:
                executando = False

            if evento.type == KEYDOWN:

                if evento.key == K_ESCAPE:
                    executando = False

        # Atualizacao fisica
        atualizar_sistema(dt)

        # Limpeza dos buffers
        glClear(
            GL_COLOR_BUFFER_BIT |
            GL_DEPTH_BUFFER_BIT
        )

        # Desenho
        desenhar_particulas()

        # Apresentacao da imagem
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
